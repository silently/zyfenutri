"""What happens to a nutrient at each step of making tempeh.

Each transform takes a sheet and returns a sheet, both per 100 g of RAW
ingredient: no transform touches water or knows the product's mass. Hydration
is carried by the final division in `mixing.mix`, once. That single rule is
what keeps water from being counted twice.

Where the coefficients come from, and what they are worth: `refs/methode.md`.
"""
from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field, replace
from itertools import pairwise
from math import exp
from typing import Protocol, runtime_checkable

from zyfenutri.nutrients import NUTRIENTS, SUBSET_OF, NutritionFacts

#: Which transforms each role goes through, in order.
#:
#: The support does not soak and does not cook: it goes in after draining. It
#: does ferment, being in the block throughout incubation.
#:
#: Pasteurisation is deliberately absent. Gentle heat moves no mass of protein,
#: fat, carbs, fibre or salt. Done uncovered it drives off water, which the
#: final weighing already accounts for. There is nothing to model.
PIPELINE: dict[str, tuple[str, ...]] = {
    "substrate": ("dehulling", "soaking", "cooking", "fermentation"),
    "support": ("roasting", "fermentation"),
    "acid": (),          # added after cooking; counted pro rata, untouched
    # A laboratory sample taken after cooking: only fermentation is left.
    "sample_after_cooking": ("fermentation",),
}

#: Roles left out of the calculation, and why. Both exclusions slightly
#: UNDER-declare the product, which is the safe direction.
EXCLUDED = {
    "soaking_acid": "leaves with the soaking water, which is thrown away",
    "starter": "a few grams for several kilos of product",
}


# --- Transforms as values ------------------------------------------------------
#
# A transform takes a sheet and returns a sheet. Both sheets share the SAME
# basis: grams of nutrient carried by 100 g of the ingredient as weighed before
# any transform. A transform never re-expresses a result "per 100 g of what is
# left" — the only division by the mass of product happens in `mixing.mix`.


@runtime_checkable
class Transform(Protocol):
    """One step an ingredient goes through: a sheet in, a sheet out.

    A step that depends on a setting (soaking time, fermentation time…) is
    built by a factory that takes the setting and returns a `Transform`. The
    setting is bound once; every transform then has the same call signature,
    and a pipeline is just a list.
    """

    @property
    def label(self) -> str:
        """What the step did, in French, for the calculation sheet."""
        ...

    def __call__(self, facts: NutritionFacts, /) -> NutritionFacts: ...


@dataclass(frozen=True, slots=True)
class Retention:
    """The common transform: each nutrient keeps a fraction of its mass.

    `factors` maps a nutrient to the fraction it retains: 1.0 keeps
    everything, 0.5 loses half. A nutrient that is not listed is untouched.
    A "dont" line that is not listed follows its total, so saturates never
    drift above fat.
    """
    label: str
    factors: Mapping[str, float] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name, factor in self.factors.items():
            if name not in NUTRIENTS:
                raise ValueError(f"unknown nutrient {name!r}")
            if factor < 0:
                raise ValueError(f"{name}: a retention factor cannot be negative")

    def __call__(self, facts: NutritionFacts, /) -> NutritionFacts:
        factors = dict(self.factors)
        for subset, total in SUBSET_OF.items():
            if subset not in factors and total in factors:
                factors[subset] = factors[total]
        return replace(facts, **{
            name: value * factor
            for name, factor in factors.items()
            if (value := getattr(facts, name)) is not None
        })


def process(facts: NutritionFacts, transforms: Iterable[Transform]) -> NutritionFacts:
    """Run a sheet through its transforms, in order."""
    for transform in transforms:
        facts = transform(facts)
    return facts


# --- The five transforms --------------------------------------------------------
#
# Every coefficient below carries its origin: a source `[n, p. x]` from
# refs/references.md, a HYPOTHESIS, or a GAP. A GAP is `None`: the nutrient
# comes out unknown rather than guessed. Filling a gap is a data change, not a
# code change.
#
# Cooking rates are (maximum loss, time constant) — see `retained`. What dissolves is
# modelled by fraction, not by species: carbs are split into sugars (soluble)
# and starch (≈ carbs − sugars, insoluble), so ONE transform serves soy and
# lentil alike. Details: refs/transformations.md.

type Loss = tuple[float, float] | None


def retained(loss: Loss, time: float) -> float | None:
    """Fraction kept after `time`, or `None` when the loss is unknown.

    The loss rises fast, then levels off once the soluble part is gone:
    kept = 1 − max_loss × (1 − e^(−time / τ)).
    """
    if time == 0:
        return 1.0
    if loss is None:
        return None
    max_loss, tau = loss
    return 1 - max_loss * (1 - exp(-time / tau))


def scaled(value: float | None, factor: float | None) -> float | None:
    """`value × factor`; unknown if either is."""
    return None if value is None or factor is None else value * factor


def split_carbs(facts: NutritionFacts, keep_sugars: float | None,
                keep_starch: float | None) -> dict[str, float | None]:
    """New `carbs` and `sugars`, starch (≈ carbs − sugars) and sugars kept apart."""
    sugars = scaled(facts.sugars, keep_sugars)
    if facts.carbs is None or facts.sugars is None:
        return {"carbs": None, "sugars": sugars}
    # Floored at zero: sugars above carbs is a faulty sheet, not starch.
    starch = scaled(max(0.0, facts.carbs - facts.sugars), keep_starch)
    carbs = None if starch is None or sugars is None else starch + sugars
    return {"carbs": carbs, "sugars": sugars}


def interpolated(points: tuple[tuple[float, float], ...], x: float) -> float | None:
    """Linear interpolation between known points; `None` outside them."""
    for (x0, y0), (x1, y1) in pairwise(points):
        if x0 <= x <= x1:
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    return None


def lost(points: tuple[tuple[float, float], ...], x: float) -> float | None:
    """Fraction kept, from known fractions lost; `None` outside them."""
    share = interpolated(points, x)
    return None if share is None else 1 - share


def saturated(facts: NutritionFacts, fat: float | None, share_gain: float | None) -> float | None:
    """Saturates once their share of fat has risen by `share_gain`, capped at fat."""
    if facts.saturates is None or fat is None or share_gain is None:
        return None
    if not facts.fat:
        return facts.saturates
    return min(fat, fat * (facts.saturates / facts.fat + share_gain))


def minus(value: float | None, amount: float) -> float | None:
    """`value − amount`; unknown if the sheet cannot spare that much."""
    return None if value is None or amount > value else value - amount


# --- Dehulling ---
#
# Hulls removed. Not a setting, and no mass here: the hulls' mass is carried by
# the yield factor, like every other change of mass. This transform only says
# which nutrients left with them, per 100 g of seed as weighed with its hulls.

# The hull is 8-10 % of a soybean [1, p. 60]: 7.9 % dehulled by hand, 9.5 %
# mechanically (Smith 1964, [12, p. 189]).
HULL_FRACTION = 0.09
# Hull composition, g per 100 g of hull: protein 8.8, carbohydrates 86, fat
# 1.0, ash 4.3 (Cowan 1969, cited in [12, p. 188]). Smith 1964 finds hulls at
# 11.7-12.5 % protein, holding 3 % of the seed's protein [12, p. 189].
HULL_PROTEIN = 0.088
HULL_FAT = 0.010
# The hull holds half of the seed's fibre [1, p. 60]; "a large proportion of
# the crude fiber lost is lost in the hulls" [12, p. 188]. Taken as a share of
# the SHEET's fibre, so it holds whatever the fibre method.
HULL_FIBRE_SHARE = 0.5
# HYPOTHESIS: the hull's other carbohydrates are not sugars or starch.
# Hull ash 4.3 % [12, p. 188] over seed ash 4.86-4.87 % (refs/official, NZ
# and USDA). HYPOTHESIS: sodium follows ash.
HULL_MINERALS_RATIO = 4.3 / 4.87


@dataclass(frozen=True, slots=True)
class Dehulling:
    """Hulls removed: what leaves with them, not their mass."""

    @property
    def label(self) -> str:
        return "Dépelliculage"

    def __call__(self, facts: NutritionFacts, /) -> NutritionFacts:
        hull_g = 100 * HULL_FRACTION      # per 100 g of seed with its hulls
        fat = minus(facts.fat, hull_g * HULL_FAT)
        keep_fat = None if fat is None or not facts.fat else fat / facts.fat
        # GAP: the germ (3 % of a soybean [1, p. 60]) is often lost too; not
        # modelled, since whether it goes depends on the machine.
        return replace(
            facts,
            fat=fat,
            saturates=scaled(facts.saturates, keep_fat if facts.fat else 1.0),
            fibre=scaled(facts.fibre, 1 - HULL_FIBRE_SHARE),
            protein=minus(facts.protein, hull_g * HULL_PROTEIN),
            salt=scaled(facts.salt, 1 - HULL_FRACTION * HULL_MINERALS_RATIO),
        )


# --- Soaking (one night, 10 to 15 h, room temperature, water thrown away) ---
#
# Tempeh soybeans soak overnight. Soaking is therefore not a setting: every
# coefficient below is the share KEPT after one night, 10 to 15 h.

# Sucrose left in whole soybeans soaked at 25 °C: 86.6 % at 6 h, 74.6 % at
# 12 h, 58.2 % at 18 h; fructose 76.9 % at 12 h [14, table 2, p. 1512].
# Sucrose and fructose (7.27 g/100 g, [14, p. 1512]) weighted over 10-15 h:
# ~73 % kept. Raffinose falls faster in [3] (44 % left at 12 h, 22 °C).
SOAKING_SUGARS_KEPT = 0.73
# HYPOTHESIS: starch is insoluble and stays in the seed.
SOAKING_STARCH_KEPT = 1.0
# Soluble (Lowry) protein in the soak water, 25 °C: 0.62 g at 12 h, 0.71 g at
# 18 h per 100 g of soybeans [14, table 1, p. 1511], ~1.7 % of protein. About
# half of the nitrogen leached is non-protein (Lo et al. 1968, cited in
# [14, p. 1510]): ~3 % of nitrogen-based protein. Plain water: acidified
# soaking loses less [1, p. 74] — GAP.
SOAKING_PROTEIN_KEPT = 0.97
# Solids in the soak water, 25 °C: 4.40 g at 12 h, 5.00 g at 18 h per 100 g of
# soybeans [14, table 1, p. 1511]; 4.9 % [12, p. 188]. Ash stays at 3.5-3.6 %
# of dry matter while soaking [13, table 1]: minerals leave at the pace of
# solids, ~5 %. HYPOTHESIS: sodium follows ash. (Unsalted tempeh declares
# "< 0,01 g" either way.)
SOAKING_MINERALS_KEPT = 0.95
# HYPOTHESIS: fibre stays. True for insoluble fibre; a sheet whose fibre
# counts oligosaccharides would lose some (refs/transformations.md, § 2).
SOAKING_FIBRE_KEPT = 1.0
# Fat −2.5 % after 24 h in room-temperature water [12, p. 193].
# HYPOTHESIS: linear, so ~1.2 % for one night.
SOAKING_FAT_KEPT = 0.988


@dataclass(frozen=True, slots=True)
class Soaking:
    """Soaking overnight (10 to 15 h) in water that is thrown away."""

    @property
    def label(self) -> str:
        return "Trempage (une nuit)"

    def __call__(self, facts: NutritionFacts, /) -> NutritionFacts:
        return replace(
            facts,
            fat=scaled(facts.fat, SOAKING_FAT_KEPT),
            saturates=scaled(facts.saturates, SOAKING_FAT_KEPT),
            **split_carbs(facts, SOAKING_SUGARS_KEPT, SOAKING_STARCH_KEPT),
            fibre=scaled(facts.fibre, SOAKING_FIBRE_KEPT),
            protein=scaled(facts.protein, SOAKING_PROTEIN_KEPT),
            salt=scaled(facts.salt, SOAKING_MINERALS_KEPT),
        )


# --- Cooking (minutes, boiling water thrown away) ---

# Sucrose −59 % over soaking and cooking (Shallenberger 1976, [12, p. 194]);
# soaking keeps ~73 % (SOAKING_SUGARS_KEPT), so cooking keeps 41/73, ~56 %.
# HYPOTHESIS: τ = 20 min, i.e. done within the usual 20-60 min [10, p. 1721].
COOKING_SUGARS: Loss = (0.44, 20.0)
# HYPOTHESIS: starch is insoluble and stays. Van Veen & Schaefer 1950 find no
# starch left in cooked beans [12, p. 195], but soybeans hold little [12, p. 194].
COOKING_STARCH: Loss = (0.0, 20.0)
# Protein lost from seed to tempeh: ~14 % [12, p. 192, with fermentation],
# 16.7 % on average over eight studies [12, p. 188], 19.7 % for Smith 1964
# [12, p. 189]; 8-23 % for dehulled cracked soybean, chickpea, pea and faba bean
# [15, tables 1-2, computed]. Taking ~14 %: ~2 % with the hulls, ~3 % at
# soaking, ~1.5 % at fermentation, leaving ~8 % to cooking — below the 10 %
# Smith measures at that step [12, p. 189].
# HYPOTHESIS: τ = 20 min.
COOKING_PROTEIN: Loss = (0.08, 20.0)
# Ash kept from dehulled seed to tempeh: 92-98 % for four legumes
# [15, tables 1-2, computed]; tempeh ash close to the seed's [12, p. 196].
# Soaking takes ~5 %, fermentation none: cooking ~2 %. (The refs/official
# pairs suggest far more, 25-42 %; set aside for a measured balance.)
# HYPOTHESIS: τ = 20 min.
COOKING_MINERALS: Loss = (0.02, 20.0)
# HYPOTHESIS: fibre stays (see SOAKING_FIBRE_KEPT).
COOKING_FIBRE: Loss = (0.0, 20.0)


@dataclass(frozen=True, slots=True)
class Cooking:
    """Boiling in water that is thrown away."""
    minutes: float

    def __post_init__(self) -> None:
        if self.minutes < 0:
            raise ValueError("a cooking time cannot be negative")

    @property
    def label(self) -> str:
        return f"Cuisson {self.minutes:g} min"

    def __call__(self, facts: NutritionFacts, /) -> NutritionFacts:
        t = self.minutes
        # Fat stays: insoluble, nothing to leach.
        return replace(
            facts,
            **split_carbs(facts, retained(COOKING_SUGARS, t), retained(COOKING_STARCH, t)),
            fibre=scaled(facts.fibre, retained(COOKING_FIBRE, t)),
            protein=scaled(facts.protein, retained(COOKING_PROTEIN, t)),
            salt=scaled(facts.salt, retained(COOKING_MINERALS, t)),
        )


# --- Fermentation (hours) ---

# Share of protein oxidised, i.e. lost: 0.5 % of initial dry matter by 32 h
# [16, p. 523], and 5, 10 and 20 g per kg of initial dry cotyledons at 28, 46
# and 72 h [9, p. 797], over protein at 45 % of dry matter [6, table 2]. Smith
# 1964 measures 1.7 % of nitrogen [12, p. 189]. Beyond 72 h: GAP.
FERMENTATION_PROTEIN_LOST = ((0.0, 0.0), (28.0, 0.011), (46.0, 0.022), (72.0, 0.044))

# Crude lipid per kg of initial dry matter, bacteria-free tempe, 30 °C [16,
# table 1, p. 529]: 243 (0 h), 228 (12 h), 211 (26 h), 215 (36 h), 216 (60 h),
# 99 (120 h), 89 (156 h), 81 g (180 h). Mature tempe loses ~12 % (26-60 h,
# averaged), then senescence burns fat fast. Corroborated: Van Buren 1972
# −9.7 % at 36 h [12, p. 188]; [7] and [2] once dry matter is accounted for.
# [10, p. 1733] misquotes this study as 30 %. Acidified autoclaved cotyledons,
# overnight-type process; [15] finds far more after a 24 h soak at 30 °C on
# cracked beans. Beyond 180 h: GAP.
FERMENTATION_FAT_LOST = ((0.0, 0.0), (12.0, 0.06), (26.0, 0.12), (60.0, 0.12),
                         (120.0, 0.59), (156.0, 0.63), (180.0, 0.67))

# Saturated share of fat, seed → tempeh, in points: +9.1 (USDA), +3.8 (NZ),
# +10.8 (Norway); +7.9 on average. Calibrated on refs/official. Taken whole by
# mature tempe, from 26 h, like fat [16]. It implies more saturated fat in mass
# than the seed held: mould mycelium making its own lipids would explain it,
# no source says so. Kept because under-declaring saturates is the unsafe
# direction. [2] finds the share falling with R. oligosporus in the lab.
# HYPOTHESIS: linear up to 26 h. Beyond 60 h: GAP.
FERMENTATION_SATURATED_SHARE_GAIN = ((0.0, 0.0), (26.0, 0.079), (60.0, 0.079))

# Sucrose −17 % over 48 h of fermentation, the decrease continuing afterwards
# (Shallenberger 1976, cited in [12, p. 194]). HYPOTHESIS: linear. Beyond 48 h: GAP.
FERMENTATION_SUGARS_LOST = ((0.0, 0.0), (48.0, 0.17))

# Starch. From dehulled seed to tempeh, nitrogen-free extract — starch for the
# most part in these legumes — keeps 62 % (faba bean), 70 % (chickpea) and
# 76 % (pea) of its mass after 35-40 h of fermentation [15, tables 1-2,
# computed]: 69 % on average. Soaking and cooking leave starch in the seed
# here, so all of it is charged to fermentation — an upper bound, since some
# leaves in the water. Earlier readings (soybean 0.4 → 0.1 % of dry matter,
# field bean −74 %, cited in [8, p. 624-625]) come from a starch-poor seed or
# a single secondary source.
# HYPOTHESIS: linear, extended to 48 h. Beyond 48 h: GAP.
FERMENTATION_STARCH_LOST = ((0.0, 0.0), (37.5, 0.31), (48.0, 0.39))

# HYPOTHESIS: fibre held constant. It rises in most studies — mould mycelium
# is fibre-rich (Steinkraus 1960 +58 %, Murata 1967 up to +34 %), one falling
# (Wang 1968 −21 %) [12, p. 195] — and crude fibre gains 15-31 % in mass from
# seed to tempeh for four legumes [15, tables 1-2, computed]. Crude fibre is
# not dietary fibre, so no figure is carried over: holding it under-declares,
# the safe direction.
FERMENTATION_FIBRE_KEPT = 1.0


@dataclass(frozen=True, slots=True)
class Fermentation:
    """Incubation with *Rhizopus*."""
    hours: float

    def __post_init__(self) -> None:
        if self.hours < 0:
            raise ValueError("a fermentation time cannot be negative")

    @property
    def label(self) -> str:
        return f"Fermentation {self.hours:g} h"

    def __call__(self, facts: NutritionFacts, /) -> NutritionFacts:
        t = self.hours
        fat = scaled(facts.fat, lost(FERMENTATION_FAT_LOST, t))
        # GAP: product temperature matters as much as time [2], [7], but no
        # source ties the losses to it yet — not a setting until one does.
        # Calibrated on R. oligosporus ([15], [16]). R. oryzae loses far more
        # fatty acids past ~40 h at 30 °C [2, table 1]: not modelled.
        return NutritionFacts(
            fat=fat,
            saturates=saturated(facts, fat, interpolated(FERMENTATION_SATURATED_SHARE_GAIN, t)),
            **split_carbs(facts, lost(FERMENTATION_SUGARS_LOST, t),
                          lost(FERMENTATION_STARCH_LOST, t)),
            fibre=scaled(facts.fibre, FERMENTATION_FIBRE_KEPT),
            protein=scaled(facts.protein, lost(FERMENTATION_PROTEIN_LOST, t)),
            # Minerals are not consumed: ash stays constant throughout
            # fermentation [16, p. 526].
            salt=facts.salt,
        )


# --- Roasting (yes or no) ---
#
# Roasting drives off water, which is not on the sheet, and runs Maillard and
# caramelisation, which are. Losses below are read on dry basis.
# HYPOTHESIS: roasting loses no dry matter, only water — volatiles neglected.

# Sugars. Soybean → kinako, both in the Japanese table (MEXT 2020, sum of
# weighed mono- and disaccharides): 6.0 → 6.1 g as sold, 6.85 → 6.35 g per
# 100 g of dry matter for yellow soybean (04023 → 04029), 8.57 → 7.86 for
# green (04104 → 04082): −7 % and −8 %. Calibrated on refs/official. Reducing
# sugars, 0.4 g in green soybean, are gone from its kinako, as Maillard would
# have it. [18, table 6, p. 43] finds no significant loss after drum roasting
# of soaked beans: no figure there, the couples give one.
ROASTING_SUGARS_KEPT = 0.92

# Fibre. Total dietary fibre of quinoa, whole seeds roasted 8 min at 120 °C:
# 17.31 → 15.04 g as analysed, 18.81 → 15.83 g on dry basis, −16 %
# [19, table 1]. Same sign on soybean → kinako, Prosky method, −8 % on dry
# basis (MEXT 04023 → 04029, refs/official). Roasted black chickpea −7 % and
# maize −12.5 %, cited in [19]. Taking the larger loss under-declares fibre,
# the safe direction.
ROASTING_FIBRE_KEPT = 0.84


@dataclass(frozen=True, slots=True)
class Roasting:
    """Dry roasting, as of a support such as kinako."""

    @property
    def label(self) -> str:
        return "Torréfaction"

    def __call__(self, facts: NutritionFacts, /) -> NutritionFacts:
        return replace(
            facts,
            # [19, table 1]: total starch unchanged on dry basis.
            **split_carbs(facts, ROASTING_SUGARS_KEPT, 1.0),
            fibre=scaled(facts.fibre, ROASTING_FIBRE_KEPT),
            # Fat, protein and ash unchanged on dry basis, 110-120 °C [13,
            # table 1], [19, table 1]. The MEXT couples scatter by ±10 % on
            # these (fat even rises): two samples, not one roasted twice.
        )


# --- A step that happened but cannot be computed ---

@dataclass(frozen=True, slots=True)
class Unknown:
    """A transform whose setting is missing: every nutrient comes out unknown."""
    label: str

    def __call__(self, facts: NutritionFacts, /) -> NutritionFacts:
        return NutritionFacts()


#: Every coefficient of the five transforms, as shown on the calculation sheet.
#: `None` is a gap.
COEFFICIENTS = {
    "hull_protein": HULL_PROTEIN,
    "hull_fat": HULL_FAT,
    "hull_fraction": HULL_FRACTION,
    "hull_fibre_share": HULL_FIBRE_SHARE,
    "hull_minerals_ratio": HULL_MINERALS_RATIO,
    "soaking_sugars_kept": SOAKING_SUGARS_KEPT,
    "soaking_starch_kept": SOAKING_STARCH_KEPT,
    "soaking_protein_kept": SOAKING_PROTEIN_KEPT,
    "soaking_minerals_kept": SOAKING_MINERALS_KEPT,
    "soaking_fibre_kept": SOAKING_FIBRE_KEPT,
    "soaking_fat_kept": SOAKING_FAT_KEPT,
    "cooking_sugars": COOKING_SUGARS,
    "cooking_starch": COOKING_STARCH,
    "cooking_protein": COOKING_PROTEIN,
    "cooking_minerals": COOKING_MINERALS,
    "cooking_fibre": COOKING_FIBRE,
    "fermentation_protein_lost": FERMENTATION_PROTEIN_LOST,
    "fermentation_fat_lost": FERMENTATION_FAT_LOST,
    "fermentation_saturated_share_gain": FERMENTATION_SATURATED_SHARE_GAIN,
    "fermentation_sugars_lost": FERMENTATION_SUGARS_LOST,
    "fermentation_starch_lost": FERMENTATION_STARCH_LOST,
    "fermentation_fibre_kept": FERMENTATION_FIBRE_KEPT,
    "roasting_sugars_kept": ROASTING_SUGARS_KEPT,
    "roasting_fibre_kept": ROASTING_FIBRE_KEPT,
}
