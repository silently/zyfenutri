"""**zyfenutri** — nutritional composition of tempeh.

The calculation that turns *what went into a batch* into *what may be written
on the label*. A library with no dependencies, and a command-line script.

    from zyfenutri import compute

    result = compute({
        "harvested_g": 1750,
        "ingredients": [
            {"name": "Soja", "role": "substrate", "weight_g": 1000,
             "per_100g": {"fat": 20, "saturates": 2.9, "carbs": 15,
                          "sugars": 5.7, "fibre": 15, "protein": 40, "salt": 0.01}},
        ],
    })
    print(result["label"])      # what is written
    print(result["steps"])      # how it got there

Same thing from a file:

    zyfenutri batch.yml

This package decides nothing. It applies documented rules to data it is given,
and returns the chain it followed so that it can be checked, and argued with.
The method, and what backs it, is in `refs/methode.md`.
"""
from zyfenutri.checks import MASS_BALANCE_MAX_G, MASS_BALANCE_SUSPECT_G, check, mass_balance
from zyfenutri.engine import compute
from zyfenutri.label import KCAL_PER_G, KJ_PER_G, declared, declared_label, energy, tolerance
from zyfenutri.nutrients import LABELS, NUTRIENTS
from zyfenutri.transforms import DEFAULTS, EXCLUDED, PIPELINE

__version__ = "2.0.0"

__all__ = [
    "compute", "NUTRIENTS", "LABELS", "DEFAULTS", "PIPELINE", "EXCLUDED",
    "energy", "declared", "declared_label", "tolerance",
    "mass_balance", "check", "MASS_BALANCE_MAX_G", "MASS_BALANCE_SUSPECT_G",
    "KJ_PER_G", "KCAL_PER_G", "__version__",
]
