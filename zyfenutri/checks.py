"""What a per-100 g composition is allowed to be.

Physical bounds only — no product, no database, no regulation beyond common
sense: nothing is negative, nothing exceeds 100 g inside 100 g, a "dont" line
stays under its total, and what adds up cannot exceed 100 g.
"""
from __future__ import annotations

from zyfenutri.nutrients import NUTRIENTS, SUBSET_OF

#: What actually adds up. Not all seven: saturates are part of fat and sugars
#: part of carbs — counting them separately would double their mass.
ADDITIVE = ("fat", "carbs", "fibre", "protein", "salt")

#: Above this, the sheet is impossible. The margin covers legal rounding: four
#: values over 10 g rounded to the gram can inflate the sum by 2 g with nothing
#: being wrong.
MASS_BALANCE_MAX_G = 102.0

#: Above this it is suspect but not impossible: almost nothing would be left
#: for water and ash, which no ordinary food has at zero. A pure fat comes
#: close to 100 g, hence a warning rather than a refusal.
MASS_BALANCE_SUSPECT_G = 95.0


def mass_balance(per_100g: dict) -> float | None:
    """Sum of what adds up, in g per 100 g. `None` for an empty sheet.

    This check needs no extra data: whatever is under 100 g is necessarily
    water and ash. That is enough to catch a physically impossible sheet.
    """
    present = [per_100g.get(k) for k in ADDITIVE if per_100g.get(k) is not None]
    return round(sum(present), 2) if present else None


def check(per_100g: dict) -> None:
    """Raise `ValueError` if the composition cannot exist."""
    for name in NUTRIENTS:
        value = per_100g.get(name)
        if value is None:
            continue
        if value < 0:
            raise ValueError(f"{name} cannot be negative")
        if value > 100:
            raise ValueError(f"{name} cannot exceed 100 g per 100 g")
    for subset, total in SUBSET_OF.items():
        low, high = per_100g.get(subset), per_100g.get(total)
        if low is not None and high is not None and low > high:
            raise ValueError(f"{subset} cannot exceed {total} — it is part of it")

    total = mass_balance(per_100g)
    if total is not None and total > MASS_BALANCE_MAX_G:
        raise ValueError(
            f"macronutrients add up to {total:.1f} g per 100 g: impossible. "
            "One value is wrong, or the sheet is on a dry-matter basis."
        )
