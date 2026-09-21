"""What goes on the label: energy, rounding, tolerances.

All three come from Regulation (EU) 1169/2011 and the Commission's December
2012 tolerance guidance. The reasoning behind each is in `refs/methode.md`;
this module only applies the rules.
"""
from typing import Literal

from zyfenutri.nutrients import NUTRIENTS, NutritionFacts

#: Annex XIV conversion factors, for the four macros that carry energy.
KJ_PER_G = {"fat": 37.0, "carbs": 17.0, "protein": 17.0, "fibre": 8.0}
KCAL_PER_G = {"fat": 9.0, "carbs": 4.0, "protein": 4.0, "fibre": 2.0}

#: Annex XIV also rates organic acids. They are not among the seven declared
#: values, so `energy()` never sees them — but a table that counted them will
#: report more energy than our macros imply. On a 5% vinegar that is 65 kJ.
ORGANIC_ACIDS_KJ_PER_G = 13.0
ORGANIC_ACIDS_KCAL_PER_G = 3.0

#: Below this, the value may be declared as "< x". Threshold and printed text
#: differ for salt: negligible under 0.0125 g, but "< 0,01 g" is what one
#: writes. Printing the threshold would give "< 0,0125 g", which appears on no
#: label anywhere.
_NEGLIGIBLE = {
    "fat": (0.5, "0,5"), "carbs": (0.5, "0,5"), "sugars": (0.5, "0,5"),
    "protein": (0.5, "0,5"), "fibre": (0.5, "0,5"),
    "saturates": (0.1, "0,1"), "salt": (0.0125, "0,01"),
}
SALT_NEGLIGIBLE_G, SALT_DECLARED_MENTION = _NEGLIGIBLE["salt"]

#: Tolerance table 1. Each entry: (below this value, use this absolute margin).
#: `None` as a margin means the relative one applies.
RELATIVE_TOLERANCE = 0.20
_TOLERANCES: dict[str, list[tuple[float | None, float | None]]] = {
    "carbs": [(10, 2.0), (40, None), (None, 8.0)],
    "sugars": [(10, 2.0), (40, None), (None, 8.0)],
    "protein": [(10, 2.0), (40, None), (None, 8.0)],
    "fibre": [(10, 2.0), (40, None), (None, 8.0)],
    "fat": [(10, 1.5), (40, None), (None, 8.0)],
    "saturates": [(4, 0.8), (None, None)],
    "salt": [(1.25, 0.375), (None, None)],
}


type EnergyUnit = Literal["kJ", "kcal"]

_FACTORS_BY_UNIT: dict[str, dict[str, float]] = {"kJ": KJ_PER_G, "kcal": KCAL_PER_G}


def energy_of(facts: NutritionFacts, unit: EnergyUnit = "kJ") -> float | None:
    """Energy of a sheet, per 100 g, in the unit asked for. Unrounded.

    `None` if any of the four macros that carry energy is unknown. Each unit
    has its own Annex XIV factors: kcal is not kJ / 4.184.

    The seven values are enough for tempeh, not for every food: Annex XIV also
    rates organic acids, polyols and alcohol, which the sheet does not hold.
    """
    try:
        factors = _FACTORS_BY_UNIT[unit]
    except KeyError:
        raise ValueError(f"unknown energy unit {unit!r}: 'kJ' or 'kcal'") from None
    values = {name: getattr(facts, name) for name in factors}
    if any(value is None for value in values.values()):
        return None
    return sum(factor * values[name] for name, factor in factors.items())


def energy(per_100g: dict[str, float | None]) -> tuple[float | None, float | None]:
    """Energy in kJ and kcal, from the macros. Never copied from a table. Unrounded.

    Returns `(None, None)` if any of the four contributing macros is missing:
    an energy short of one nutrient is worse than no energy at all.

    kcal is *not* kJ / 4.184. Annex XIV gives two independent sets of factors,
    and converting would make the two printed figures disagree.

    `declared` rounds to the whole unit, and it is the only thing that rounds:
    a decigram on the way would move that figure. 631.46 kJ through the
    decigram is 631.5, which then prints as "632 kJ" instead of "631 kJ".
    """
    if any(per_100g.get(k) is None for k in KJ_PER_G):
        return None, None
    kj = sum(factor * per_100g[k] for k, factor in KJ_PER_G.items())
    kcal = sum(factor * per_100g[k] for k, factor in KCAL_PER_G.items())
    return kj, kcal


def _fr(value: float, decimals: int) -> str:
    """French decimal comma — these strings are meant to be printed as is."""
    return f"{value:.{decimals}f}".replace(".", ",")


def declared(name: str, value: float | None) -> str | None:
    """One value, written the way it must appear on the label (table 4).

    `None` stays `None`: a dash on screen, never a zero. "0 g" is a claim.
    """
    if value is None:
        return None
    if name in ("energy_kj", "energy_kcal"):
        return f"{round(value):d} {'kJ' if name == 'energy_kj' else 'kcal'}"

    threshold, mention = _NEGLIGIBLE.get(name, (0.5, "0,5"))
    if value <= threshold:
        return f"< {mention} g"
    if name == "salt":
        # Decigram from 1 g up, centigram below.
        return f"{_fr(round(value, 1), 1)} g" if value >= 1 else f"{_fr(round(value, 2), 2)} g"
    if value >= 10:
        return f"{round(value):d} g"
    return f"{_fr(round(value, 1), 1)} g"


def declared_label(per_100g: dict[str, float | None]) -> dict[str, str | None]:
    """The nine values as they are written, energy first.

    The two energy mentions come both joined, as a label prints them, and
    apart, for a caller that holds them in two fields. Apart matters: writing
    them from a value this module already rounded would round twice, and a
    second round moves the figure by a unit.
    """
    kj, kcal = per_100g.get("energy_kj"), per_100g.get("energy_kcal")
    written_kj, written_kcal = declared("energy_kj", kj), declared("energy_kcal", kcal)
    out: dict[str, str | None] = {
        "energy": f"{written_kj} / {written_kcal}" if kj is not None else None,
        "energy_kj": written_kj,
        "energy_kcal": written_kcal,
    }
    for name in NUTRIENTS:
        out[name] = declared(name, per_100g.get(name))
    return out


def tolerance(name: str, value: float) -> float:
    """Absolute tolerance, in grams, around a declared value.

    The only threshold that means anything when judging an estimate against a
    measurement: it says whether the gap would stand up to an inspection. A
    "30% error" says nothing until you know what quantity it is 30% of.
    """
    for threshold, absolute in _TOLERANCES.get(name, [(None, None)]):
        if threshold is None or value < threshold:
            return absolute if absolute is not None else round(value * RELATIVE_TOLERANCE, 4)
    return round(value * RELATIVE_TOLERANCE, 4)
