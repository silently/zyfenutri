"""The seven declared nutrients, and how to read them from a document.

Everything downstream speaks these seven keys and nothing else. Energy is not
one of them: it is always recomputed from the macros (see `label.py`).
"""
from collections.abc import Mapping
from dataclasses import astuple, dataclass

#: The seven values a nutrition declaration must carry, in label order.
NUTRIENTS = ("fat", "saturates", "carbs", "sugars", "fibre", "protein", "salt")

#: French labels, as they appear on a French label.
LABELS = {
    "fat": "Matières grasses",
    "saturates": "dont acides gras saturés",
    "carbs": "Glucides",
    "sugars": "dont sucres",
    "fibre": "Fibres alimentaires",
    "protein": "Protéines",
    "salt": "Sel",
}

#: A "dont" line can never exceed the total it is part of.
SUBSET_OF = {"saturates": "fat", "sugars": "carbs"}

#: Spellings we accept on input. Being liberal here costs one dict and saves
#: every caller a translation layer.
ALIASES = {
    "fat_g": "fat", "lipides": "fat", "matieres_grasses": "fat",
    "saturates_g": "saturates", "saturated": "saturates", "ags": "saturates",
    "carbohydrates": "carbs", "carbohydrates_g": "carbs", "carbs_g": "carbs",
    "glucides": "carbs",
    "sugars_g": "sugars", "sucres": "sugars",
    "fibre_g": "fibre", "fiber": "fibre", "fibres": "fibre",
    "protein_g": "protein", "proteins": "protein", "proteines": "protein",
    "salt_g": "salt", "sel": "salt",
}


def read_per_100g(raw: dict | None) -> dict[str, float]:
    """A `per_100g:` block from a document, keyed by our seven names.

    Unknown keys are ignored on purpose: a table may carry vitamins or minerals
    we do not declare, and refusing the whole sheet over them would be unkind.
    A missing nutrient stays missing — it is never turned into a zero, because
    "we don't know" and "there is none" are different claims.
    """
    if not raw:
        return {}
    out: dict[str, float] = {}
    for key, value in raw.items():
        name = ALIASES.get(str(key).strip().lower(), str(key).strip().lower())
        if name in NUTRIENTS and isinstance(value, (int, float)):
            out[name] = float(value)
    return out


@dataclass(frozen=True, slots=True, kw_only=True)
class NutritionFacts:
    """A nutrition facts sheet: the seven values, in grams per 100 g.

    `None` means "not known", never "none": an unknown value stays unknown
    through every calculation instead of quietly becoming a zero.

    Energy is not stored. It follows from these values (see
    `label.energy_of`), and storing it would let the two disagree.

    Immutable: a transform returns a new sheet, it never edits one in place.
    Constructing a sheet checks nothing — `checks.check` says whether it can
    physically exist.
    """
    fat: float | None = None
    saturates: float | None = None
    carbs: float | None = None
    sugars: float | None = None
    fibre: float | None = None
    protein: float | None = None
    salt: float | None = None

    @classmethod
    def from_mapping(cls, raw: Mapping | None) -> NutritionFacts:
        """Build a sheet from a `per_100g:` block, accepting the input aliases."""
        return cls(**read_per_100g(raw))

    def as_dict(self) -> dict[str, float | None]:
        """The seven values keyed by name, in label order."""
        return dict(zip(NUTRIENTS, astuple(self)))

    @property
    def unknown(self) -> tuple[str, ...]:
        """Names of the values that are not known."""
        return tuple(name for name, value in self.as_dict().items() if value is None)
