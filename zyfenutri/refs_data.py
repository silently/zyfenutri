"""Reading `refs/` — the laboratory analyses.

Every function returns empty lists when the directory is absent: the package
stays usable without it. Two consumers: `check.py` (the reading one looks at)
and `tests/test_refs.py` (the one that fails).

Why one shared module rather than reading the YAML on both sides: the mapping
from the French file keys to our field names exists in one place only. A
misspelt key in a reference file would otherwise be silently ignored on both
sides, and the analysis would count for nothing.

The file keys stay in French on purpose: the files are filled in by hand, by
the people who run the lab analyses.
"""
import os
from dataclasses import dataclass, field
from pathlib import Path

from zyfenutri.nutrients import NUTRIENTS as NUTRIENT_FIELDS

#: Where to look for reference data: where `ZYFENUTRI_REFS` says, or next to
#: the package. `ZYFE_NUTRI_REFS` is the former name, still honoured. When
#: nothing is found, everything returns empty lists.
_CANDIDATES = [
    os.environ.get("ZYFENUTRI_REFS"),
    os.environ.get("ZYFE_NUTRI_REFS"),
    Path(__file__).resolve().parents[1] / "refs",
]

#: Key in the reference files → our field name.
FIELD_BY_FR = {
    "matieres_grasses_g": "fat",
    "acides_gras_satures_g": "saturates",
    "glucides_g": "carbs",
    "sucres_g": "sugars",
    "fibres_g": "fibre",
    "proteines_g": "protein",
    "sel_g": "salt",
}

_SAMPLE_KEYS = {"description", "masse_g", "humidite_g_100g", "composition_pour_100g"}


def refs_dir() -> Path | None:
    for candidate in _CANDIDATES:
        if not candidate:
            continue
        path = Path(candidate)
        if path.is_dir():
            return path
    return None


@dataclass
class Sample:
    """One measured state: a mass and a composition per 100 g."""
    description: str | None = None
    masse_g: float | None = None
    humidite_g_100g: float | None = None
    #: Composition keyed by our field names (`fat`…), per 100 g.
    composition: dict[str, float] = field(default_factory=dict)

    @property
    def usable(self) -> bool:
        """Usable for calibration: without a mass, a per-100 g composition
        compares to nothing (see the trap spelt out at the top of MODELE.yml)."""
        return bool(self.masse_g) and bool(self.composition)


@dataclass
class Analysis:
    path: Path
    reference: str
    is_example: bool = False
    recette_code: str | None = None
    lot_id: str | None = None
    #: Incubation time, hours: what `Fermentation` needs to predict "after".
    fermentation_h: float | None = None
    matiere_premiere: Sample = field(default_factory=Sample)
    avant: Sample = field(default_factory=Sample)
    apres: Sample = field(default_factory=Sample)
    #: Unknown keys met while reading — a typo silences a value.
    unknown_fields: list[str] = field(default_factory=list)


def _read_yaml(path: Path) -> dict:
    import yaml
    return yaml.safe_load(path.read_text()) or {}


def _files(subdir: str) -> list[Path]:
    root = refs_dir()
    if root is None:
        return []
    directory = root / subdir
    if not directory.is_dir():
        return []
    # `MODELE.yml` is a template, never data.
    return sorted(p for p in directory.glob("*.yml") if p.stem != "MODELE")


def _sample(raw: dict | None, where: str, unknown: list[str]) -> Sample:
    if not isinstance(raw, dict):
        return Sample()
    for key in raw:
        if key not in _SAMPLE_KEYS:
            unknown.append(f"{where}.{key}")
    composition_raw = raw.get("composition_pour_100g") or {}
    composition: dict[str, float] = {}
    for key, value in composition_raw.items():
        name = FIELD_BY_FR.get(key)
        if name is None:
            unknown.append(f"{where}.composition_pour_100g.{key}")
        elif isinstance(value, (int, float)):
            composition[name] = float(value)
    return Sample(
        description=raw.get("description"),
        masse_g=raw.get("masse_g"),
        humidite_g_100g=raw.get("humidite_g_100g"),
        composition=composition,
    )


def load_analyses() -> list[Analysis]:
    out: list[Analysis] = []
    for path in _files("analyses"):
        data = _read_yaml(path)
        unknown: list[str] = []
        product = data.get("produit") or {}
        out.append(Analysis(
            path=path,
            reference=str(data.get("reference") or path.stem),
            is_example=bool(data.get("exemple")),
            recette_code=product.get("recette_code"),
            lot_id=product.get("lot_id"),
            fermentation_h=data.get("duree_fermentation_h"),
            matiere_premiere=_sample(data.get("matiere_premiere"), "matiere_premiere", unknown),
            avant=_sample(data.get("avant_fermentation"), "avant_fermentation", unknown),
            apres=_sample(data.get("apres_fermentation"), "apres_fermentation", unknown),
            unknown_fields=unknown,
        ))
    return out


@dataclass
class Deviation:
    """Gap between what the calculation predicts and what the lab measured."""
    field: str
    predicted: float
    measured: float
    tolerance: float

    @property
    def delta(self) -> float:
        return round(self.predicted - self.measured, 3)

    @property
    def within(self) -> bool:
        """Within the regulatory tolerance — the only threshold that means anything here."""
        return abs(self.predicted - self.measured) <= self.tolerance


def predict_after_fermentation(analysis: Analysis) -> dict[str, float]:
    """What the calculation predicts for "after", starting from "before".

    The sample has already soaked and cooked, so only fermentation is left:
    it gets the `sample_after_cooking` role, whose pipeline is exactly that.
    """
    from zyfenutri.engine import compute

    result = compute({
        "fermentation_hours": analysis.fermentation_h,
        "ingredients": [{
            "name": analysis.reference,
            # Not `substrate`: that would apply leaching a second time to a
            # loss the sample has already taken.
            "role": "sample_after_cooking",
            "weight_g": analysis.avant.masse_g,
            # ⚠️ Les deux masses de l'analyse SONT le facteur de rendement de
            # cet échantillon : après / avant. C'est la même division qu'un
            # poids pesé donnerait, exprimée dans la seule grandeur que le
            # moteur connaisse désormais.
            "yield": analysis.apres.masse_g / analysis.avant.masse_g,
            "per_100g": analysis.avant.composition,
        }],
    })
    return {k: v for k, v in result["per_100g"].items() if v is not None}


def fermentation_deviations(analysis: Analysis) -> list[Deviation]:
    """Predicted vs measured, nutrient by nutrient. `[]` if not usable."""
    from zyfenutri.label import tolerance

    if not (analysis.avant.usable and analysis.apres.usable):
        return []
    predicted = predict_after_fermentation(analysis)
    return [
        Deviation(
            field=name,
            predicted=predicted[name],
            measured=analysis.apres.composition[name],
            tolerance=tolerance(name, analysis.apres.composition[name]),
        )
        for name in NUTRIENT_FIELDS
        if name in predicted and name in analysis.apres.composition
    ]
