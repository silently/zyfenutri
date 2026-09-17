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
# Rates are (maximum loss, time constant) — see `retained`. What dissolves is
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


def minus(value: float | None, amount: float) -> float | None:
    """`value − amount`; unknown if the sheet cannot spare that much."""
    return None if value is None or amount > value else value - amount


# --- Dehulling ---

# Hull composition, g per 100 g of hull: protein 8.8, carbohydrates 86, fat
# 1.0, ash 4.3 (Cowan 1969, cited in [12, p. 188]). Smith 1964 finds hulls at
# 11.7-12.5 % protein, holding 3 % of the seed's protein [12, p. 189].
HULL_PROTEIN = 0.088
HULL_FAT = 0.010
# The hull is 8-10 % of the seed and holds half of its fibre [1, p. 60]; "a
# large proportion of the crude fiber lost is lost in the hulls" [12, p. 188].
# Taken as a share of the SHEET's fibre, so it holds whatever the fibre method.
# HYPOTHESIS: the share scales with the hull fraction, around 9 %.
HULL_FIBRE_SHARE = 0.5
HULL_REFERENCE_FRACTION = 0.09
# HYPOTHESIS: the hull's other carbohydrates are not sugars or starch.
# Hull ash 4.3 % [12, p. 188] over seed ash 4.86-4.87 % (refs/official, NZ
# and USDA). HYPOTHESIS: sodium follows ash.
HULL_MINERALS_RATIO = 4.3 / 4.87


@dataclass(frozen=True, slots=True)
class Dehulling:
    """Hulls removed. `hull_fraction` is the share of raw mass that left."""
    hull_fraction: float

    def __post_init__(self) -> None:
        if not 0 <= self.hull_fraction < 1:
            raise ValueError("a hull fraction lies between 0 and 1")

    @classmethod
    def from_weights(cls, raw_g: float, dehulled_g: float) -> Dehulling:
        """From the two weighings: before and after dehulling."""
        return cls(1 - dehulled_g / raw_g)

    @property
    def label(self) -> str:
        return f"Dépelliculage ({self.hull_fraction * 100:.0f} % de pellicule)"

    def __call__(self, facts: NutritionFacts, /) -> NutritionFacts:
        hull_g = 100 * self.hull_fraction      # per 100 g of raw seed
        fat = minus(facts.fat, hull_g * HULL_FAT)
        keep_fat = None if fat is None or not facts.fat else fat / facts.fat
        # GAP: the germ (3 % of a soybean [1, p. 60]) is often lost too; not
        # modelled, since whether it goes depends on the machine.
        return replace(
            facts,
            fat=fat,
            saturates=scaled(facts.saturates, keep_fat if facts.fat else 1.0),
            fibre=scaled(facts.fibre, 1 - min(1.0, HULL_FIBRE_SHARE * self.hull_fraction
                                              / HULL_REFERENCE_FRACTION)),
            protein=minus(facts.protein, hull_g * HULL_PROTEIN),
            salt=scaled(facts.salt, 1 - self.hull_fraction * HULL_MINERALS_RATIO),
        )


# --- Soaking (hours, room temperature, water thrown away) ---

# [3, table II, p. 431]: soybean raffinose 60.1 → 40.1 (3 h) → 26.3 mg/g (12 h),
# fitted. Across 5 legumes τ = 3.1-3.8 h, but the ceiling spans 16-70 %.
# HYPOTHESIS: raffinose stands in for sucrose. [3, p. 433] finds bigger sugars
# leach slower; Shallenberger 1976 measures sucrose −59 % over soaking and
# cooking, raffinose −52 % [12, p. 194]: same order.
SOAKING_SUGARS: Loss = (0.58, 3.5)
# HYPOTHESIS: starch is insoluble and stays in the seed.
SOAKING_STARCH: Loss = (0.0, 3.5)
# Solids leach at a steady rate throughout soaking, faster when warm; the
# protein share of what leaches grows with time [14, abstract]. Soaking loses
# ~5 % of solids (4.9 % [12, p. 188]; dry solids 100 → 95.1 [1, p. 80]).
# Protein, dry basis, 25 °C: 46.0 → 43.9 % at 24 h, 35.8 % at 72 h [13, table 1];
# with 5 % of solids gone, ~10 % of protein lost at 24 h. Smith 1964 gives
# ~6.5 % (dehulling and soaking, hulls aside) [12, p. 189]; the overall ~12 %
# of [12, p. 192] leaves ~6 % once hulls and cooking are counted.
# Retained: 6 % at 24 h, linear. Plain water: acidified soaking loses less
# [1, p. 74] — GAP. Beyond 24 h: GAP (losses keep growing [13], [14]).
SOAKING_PROTEIN_LOST = ((0.0, 0.0), (24.0, 0.06))
# Ash stays at 3.5-3.6 % of dry matter from 0 to 72 h [13, table 1]: minerals
# leave at the pace of solids, ~5 % by 24 h (see above). HYPOTHESIS: sodium
# follows ash; linear. Beyond 24 h: GAP. (Unsalted tempeh declares "< 0,01 g".)
SOAKING_MINERALS_LOST = ((0.0, 0.0), (24.0, 0.05))
# HYPOTHESIS: fibre stays. True for insoluble fibre; a sheet whose fibre
# counts oligosaccharides would lose some (refs/transformations.md, § 2).
SOAKING_FIBRE: Loss = (0.0, 3.5)
# 24 h in room-temperature water: fat −2.5 %; longer soaks lose much more,
# faster in warm water [12, p. 193]. Beyond 24 h: GAP.
SOAKING_FAT_LOST = ((0.0, 0.0), (24.0, 0.025))


@dataclass(frozen=True, slots=True)
class Soaking:
    """Soaking in water that is thrown away."""
    hours: float

    def __post_init__(self) -> None:
        if self.hours < 0:
            raise ValueError("a soaking time cannot be negative")

    @property
    def label(self) -> str:
        return f"Trempage {self.hours:g} h"

    def __call__(self, facts: NutritionFacts, /) -> NutritionFacts:
        t = self.hours
        keep_fat = lost(SOAKING_FAT_LOST, t)
        return replace(
            facts,
            fat=scaled(facts.fat, keep_fat),
            saturates=scaled(facts.saturates, keep_fat),
            **split_carbs(facts, retained(SOAKING_SUGARS, t), retained(SOAKING_STARCH, t)),
            fibre=scaled(facts.fibre, retained(SOAKING_FIBRE, t)),
            protein=scaled(facts.protein, lost(SOAKING_PROTEIN_LOST, t)),
            salt=scaled(facts.salt, lost(SOAKING_MINERALS_LOST, t)),
        )


# --- Cooking (minutes, boiling water thrown away) ---

# Sucrose −59 % over soaking and cooking (Shallenberger 1976, [12, p. 194]);
# soaking alone takes ~56 % (SOAKING_SUGARS at 12 h), leaving ~7 % to cooking.
# HYPOTHESIS: τ = 20 min, i.e. done within the usual 20-60 min [10, p. 1721].
COOKING_SUGARS: Loss = (0.07, 20.0)
# HYPOTHESIS: starch is insoluble and stays. Van Veen & Schaefer 1950 find no
# starch left in cooked beans [12, p. 195], but soybeans hold little [12, p. 194].
COOKING_STARCH: Loss = (0.0, 20.0)
# ~12 % of protein goes before fermentation [12, p. 192]: ~2 % with the hulls
# (HULL_PROTEIN), ~6 % at soaking, leaving ~4 %. Smith 1964 alone measures
# 10.0 % at cooking [12, p. 189]: an upper reading. HYPOTHESIS: τ = 20 min.
COOKING_PROTEIN: Loss = (0.04, 20.0)
# Calibrated on refs/official: tables keep 58-75 % of ash from seed to tempeh,
# tempeh ash sits 3-9 % below the seed's on dry basis [12, p. 196]; ~72 % kept
# overall. Hulls take ~8 %, soaking ~5 %, fermentation none: cooking ~24 %.
# HYPOTHESIS: τ = 20 min.
COOKING_MINERALS: Loss = (0.24, 20.0)
# HYPOTHESIS: fibre stays (see SOAKING_FIBRE).
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

# Share of protein oxidised, i.e. lost: 5, 10 and 20 g per kg of initial dry
# cotyledons at 28, 46 and 72 h [9, p. 797, citing Ruiz-Terán & Owens 1996],
# over protein at 45 % of dry matter [6, table 2]. Smith 1964 measures 1.7 %
# of nitrogen [12, p. 189]; Steinkraus and Murata find total nitrogen constant
# [12, p. 192]. Beyond 72 h: unknown.
FERMENTATION_PROTEIN_LOST = ((0.0, 0.0), (28.0, 0.011), (46.0, 0.022), (72.0, 0.044))

# Share of fat lost, around 30 °C. Readings agree within their noise:
# - 3 % of initial dry matter by 32 h [9, p. 797], over crude lipid at 28.1 %
#   of dry matter in dehulled cooked soybeans [7, table 1] → 11 % of fat;
# - 36 h: total fat −9.7 % (Van Buren et al. 1972, cited in [12, p. 188]);
# - 46-48 h: fat as % of dry matter barely moves ([7, table 1]: 28.2 → 29.1;
#   [2, table 1]: 22.4 → 21.0) while ~10 % of dry matter goes ([6, p. 2238]),
#   → 7 % and 16 % lost;
# - [11, p. 268-269]: "a slight decrease in lipids". Other studies range from
#   0.8 to 24.5 % [12, p. 193], and [10, p. 1733] quotes 30 %.
# HYPOTHESIS: linear up to 32 h. Beyond 48 h: GAP — senescence burns fat fast
# ([9, p. 797]: 12 % of dry matter, almost all lipid, by 180 h).
FERMENTATION_FAT_LOST = ((0.0, 0.0), (32.0, 0.11), (48.0, 0.11))

# Sucrose −17 % over 48 h of fermentation, the decrease continuing afterwards
# (Shallenberger 1976, cited in [12, p. 194]). HYPOTHESIS: linear. Beyond 48 h: GAP.
FERMENTATION_SUGARS_LOST = ((0.0, 0.0), (48.0, 0.17))

# Starch: soybean 0.4 → 0.1 % of dry matter over 48-72 h, field bean −74 %
# (cited in [8, p. 624-625]); the NZ pair falls from 4.36 to 0.18 g
# (refs/official). HYPOTHESIS: linear, 75 % consumed by 48 h. Beyond: GAP.
FERMENTATION_STARCH_LOST = ((0.0, 0.0), (48.0, 0.75))

# HYPOTHESIS: fibre held constant. Most studies find it rising — mould
# mycelium is fibre-rich (Steinkraus 1960 +58 %, Murata 1967 up to +34 %),
# one falling (Wang 1968 −21 %) [12, p. 195]. Holding it under-declares, the
# safe direction.
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
        keep_fat = lost(FERMENTATION_FAT_LOST, t)
        # GAP: product temperature matters as much as time [2], [7], but no
        # source ties the losses to it yet — not a setting until one does.
        return NutritionFacts(
            fat=scaled(facts.fat, keep_fat),
            # HYPOTHESIS: saturates follow fat. [2] shows the saturated share
            # drifting both ways depending on the strain.
            saturates=scaled(facts.saturates, keep_fat),
            **split_carbs(facts, lost(FERMENTATION_SUGARS_LOST, t),
                          lost(FERMENTATION_STARCH_LOST, t)),
            fibre=scaled(facts.fibre, FERMENTATION_FIBRE_KEPT),
            protein=scaled(facts.protein, lost(FERMENTATION_PROTEIN_LOST, t)),
            # Minerals are not consumed: ash content rises as dry matter goes
            # [10, p. 1733] and barely moves overall [12, p. 196].
            salt=facts.salt,
        )


# --- Roasting (intensity 1 to 3) ---

# Light roasting (110 °C, 10 min) leaves total carbohydrates, protein, fat and
# ash of soybean flour unchanged on dry basis [13, table 1] — intensity 1.
# HYPOTHESIS: sugars and fibre, not measured apart, are unchanged too.
# GAP: darker roasts; Maillard consumes reducing sugars, how much is unknown.
ROASTING_SUGARS_KEPT: dict[int, float | None] = {1: 1.0, 2: None, 3: None}
ROASTING_FIBRE_KEPT: dict[int, float | None] = {1: 1.0, 2: None, 3: None}


@dataclass(frozen=True, slots=True)
class Roasting:
    """Dry roasting: 1 light, 2 medium, 3 dark."""
    intensity: int

    def __post_init__(self) -> None:
        if self.intensity not in ROASTING_SUGARS_KEPT:
            raise ValueError("a roasting intensity is 1, 2 or 3")

    @property
    def label(self) -> str:
        return f"Torréfaction (intensité {self.intensity})"

    def __call__(self, facts: NutritionFacts, /) -> NutritionFacts:
        # Roasting mostly drives off water, which is not on the sheet.
        return replace(
            facts,
            # HYPOTHESIS: starch is untouched.
            **split_carbs(facts, ROASTING_SUGARS_KEPT[self.intensity], 1.0),
            # Beyond intensity 1: Maillard products may be measured as fibre.
            fibre=scaled(facts.fibre, ROASTING_FIBRE_KEPT[self.intensity]),
            # HYPOTHESIS: fat, protein (nitrogen) and salt lose no mass.
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
    "hull_fibre_share": HULL_FIBRE_SHARE,
    "hull_reference_fraction": HULL_REFERENCE_FRACTION,
    "hull_minerals_ratio": HULL_MINERALS_RATIO,
    "soaking_sugars": SOAKING_SUGARS,
    "soaking_starch": SOAKING_STARCH,
    "soaking_protein_lost": SOAKING_PROTEIN_LOST,
    "soaking_minerals_lost": SOAKING_MINERALS_LOST,
    "soaking_fibre": SOAKING_FIBRE,
    "soaking_fat_lost": SOAKING_FAT_LOST,
    "cooking_sugars": COOKING_SUGARS,
    "cooking_starch": COOKING_STARCH,
    "cooking_protein": COOKING_PROTEIN,
    "cooking_minerals": COOKING_MINERALS,
    "cooking_fibre": COOKING_FIBRE,
    "fermentation_protein_lost": FERMENTATION_PROTEIN_LOST,
    "fermentation_fat_lost": FERMENTATION_FAT_LOST,
    "fermentation_sugars_lost": FERMENTATION_SUGARS_LOST,
    "fermentation_starch_lost": FERMENTATION_STARCH_LOST,
    "fermentation_fibre_kept": FERMENTATION_FIBRE_KEPT,
    "roasting_sugars_kept": ROASTING_SUGARS_KEPT,
    "roasting_fibre_kept": ROASTING_FIBRE_KEPT,
}
