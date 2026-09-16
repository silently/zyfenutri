"""What happens to a nutrient at each step of making tempeh.

Each transformation is a pure function: absolute masses in, absolute masses
out. One rule per nutrient per step, and nothing else — energy is absent
because it is recomputed at the end.

Everything is in ABSOLUTE MASSES from start to finish, and no transformation
touches water. Hydration is carried by the final division, once. That single
rule is what keeps water from being counted twice.

Where the coefficients come from, and what they are worth: `refs/methode.md`.
"""
from __future__ import annotations

#: Loss percentages. Every one of them can be overridden by the caller.
DEFAULTS: dict[str, float] = {
    # T1 · dehulling — legume hulls are almost pure fibre, so removing 8% of
    # the mass does not remove 8% of every nutrient.
    "hull_fibre": 85.0,

    # T2a · soaking and cooking. The water is thrown away; what dissolves in
    # it is lost. One coefficient for both steps: weighing cannot tell them
    # apart, and two numbers for one observable gap is two numbers to tune.
    "leaching_carbs": 50.0,
    "leaching_protein": 3.0,
    "leaching_minerals": 35.0,

    # T2b · fermentation. The mycelium burns carbs for energy and starts on
    # fats through its lipases. Protein is hydrolysed, not consumed.
    "fermentation_carbs": 60.0,
    "fermentation_fat": 5.0,

    # T3 · roasting. Mostly drives off water, and water is not a nutrient. The
    # only real effect on the seven values is Maillard eating reducing sugars.
    "roasting_sugars": 15.0,
}

#: T2a — soaking and cooking. Fat and fibre are insoluble: nothing leaves.
SOAKING_AND_COOKING = {
    "carbs": "leaching_carbs",
    "sugars": "leaching_carbs",
    "protein": "leaching_protein",
    "salt": "leaching_minerals",
}

#: T2b — fermentation. Fibre is not calibrated (no usable data), so it is held
#: constant, which makes it an over-estimate — see `refs/methode.md`.
FERMENTATION = {
    "fat": "fermentation_fat",
    "saturates": "fermentation_fat",
    "carbs": "fermentation_carbs",
    "sugars": "fermentation_carbs",
}

#: T3 — roasting. Only Maillard bites, and only on sugars.
ROASTING = {"sugars": "roasting_sugars"}

#: Which transformations each role goes through, in order.
#:
#: The support does not soak and does not cook: it goes in after draining. It
#: does ferment, being in the block throughout incubation. So "tempehisation"
#: is two steps that do not apply to the same ingredients.
#:
#: Pasteurisation is deliberately absent. Gentle heat moves no mass of protein,
#: fat, carbs, fibre or salt. It denatures proteins — structure, not mass — and
#: destroys vitamins we do not declare. Done uncovered it drives off water,
#: which the final weighing already accounts for. There is nothing to model.
PIPELINE: dict[str, tuple[str, ...]] = {
    "substrate": ("dehulling", "soaking_and_cooking", "fermentation"),
    "support": ("roasting", "fermentation"),
    "acid": (),          # added after cooking; counted pro rata, untouched
    # A laboratory sample taken after cooking: only fermentation is left. No
    # referential category describes that state, so it gets its own role
    # rather than borrowing a neighbouring one.
    "sample_after_cooking": ("fermentation",),
}

#: Roles left out of the calculation, and why. Both exclusions slightly
#: UNDER-declare the product, which is the safe direction.
EXCLUDED = {
    "soaking_acid": "leaves with the soaking water, which is thrown away",
    "starter": "a few grams for several kilos of product",
}


def apply(masses: dict[str, float], rules: dict[str, str],
          coefficients: dict[str, float]) -> dict[str, float]:
    """Apply one transformation: each nutrient loses what its rule says."""
    return {
        name: mass * (1.0 - coefficients.get(rules[name], 0.0) / 100.0) if name in rules else mass
        for name, mass in masses.items()
    }


def dehull(masses: dict[str, float], *, per_100g: dict[str, float], hull_g: float,
           coefficients: dict[str, float]) -> tuple[dict[str, float], str | None]:
    """T1 — remove the hull, which is not the average composition of the grain.

    This is the whole point of the step: weighing sees mass leave, it does not
    see that what left was almost only fibre. Applying the average composition
    to the net weight would under-state protein and fat in the finished product.

    Returns the masses and, if the fibre bound had to bite, a warning.
    """
    fibre_share = coefficients.get("hull_fibre", 85.0) / 100.0
    out = dict(masses)
    warning = None

    removed = hull_g * fibre_share
    fibre = masses.get("fibre")
    if fibre is not None:
        # We cannot remove more fibre than the grain holds. If the bound bites,
        # the sheet and the weights contradict each other — say so rather than
        # return a zero that would read like a measurement.
        if removed > fibre * 0.95:
            warning = ("hulls would carry away more fibre than the sheet declares. "
                       "Check the sheet or the gross/net weights — the fibre value "
                       "is a floor, not a measurement.")
            removed = fibre * 0.95
        out["fibre"] = max(0.0, fibre - removed)

    # The remaining 15% of the hull carries the other nutrients pro rata.
    rest = hull_g * (1 - fibre_share)
    for name, mass in masses.items():
        if name == "fibre":
            continue
        out[name] = max(0.0, mass - rest * per_100g.get(name, 0.0) / 100.0)
    return out, warning
