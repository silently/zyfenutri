"""Lecture de `refs/` — les analyses de laboratoire.

Toutes les fonctions rendent des listes vides si le dossier est absent : le
paquet reste utilisable sans lui. Deux consommateurs : `check.py` (la lecture
qu'on regarde) et `tests/test_refs.py` (celle qui échoue).

L'intérêt de passer par un module commun plutôt que de relire le YAML des deux
côtés : le **mot-à-mot français → champ du modèle** n'existe qu'à un endroit.
Une clé mal orthographiée dans un fichier de référence serait sinon ignorée en
silence des deux côtés, et l'analyse compterait pour rien.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from zyfenutri.annexe_xiv import NUTRIENT_FIELDS

#: Où chercher les données de référence : à côté du paquet, ou là où
#: `ZYFE_NUTRI_REFS` le dit. Absent, tout rend des listes vides — le paquet
#: reste utilisable sans ses données.
_CANDIDATES = [
    os.environ.get("ZYFE_NUTRI_REFS"),
    Path(__file__).resolve().parents[1] / "refs",
]

#: Nom dans les fichiers de référence → champ du modèle.
FIELD_BY_FR = {
    "matieres_grasses_g": "fat_g",
    "acides_gras_satures_g": "saturates_g",
    "glucides_g": "carbohydrates_g",
    "sucres_g": "sugars_g",
    "fibres_g": "fibre_g",
    "proteines_g": "protein_g",
    "sel_g": "salt_g",
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
    """Un état mesuré : une masse et une composition pour 100 g."""
    description: str | None = None
    masse_g: float | None = None
    humidite_g_100g: float | None = None
    #: Composition en champs du modèle (`fat_g`…), valeurs pour 100 g.
    composition: dict[str, float] = field(default_factory=dict)

    @property
    def usable(self) -> bool:
        """Exploitable pour un calage : sans masse, une composition pour 100 g
        ne se compare à rien (cf. le piège rappelé en tête des modèles)."""
        return bool(self.masse_g) and bool(self.composition)


@dataclass
class Analysis:
    path: Path
    reference: str
    is_example: bool = False
    recette_code: str | None = None
    lot_id: str | None = None
    matiere_premiere: Sample = field(default_factory=Sample)
    avant: Sample = field(default_factory=Sample)
    apres: Sample = field(default_factory=Sample)
    #: Clés inconnues rencontrées — une faute de frappe fait taire une valeur.
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
    # `MODELE.yml` est un gabarit : il n'est jamais une donnée.
    return sorted(p for p in directory.glob("*.yml") if p.stem != "MODELE")


def _sample(raw: dict | None, where: str, unknown: list[str]) -> Sample:
    if not isinstance(raw, dict):
        return Sample()
    for key in raw:
        if key not in _SAMPLE_KEYS:
            unknown.append(f"{where}.{key}")
    composition_raw = raw.get("composition_pour_100g") or {}
    composition: dict[str, float] = {}
    for nom, valeur in composition_raw.items():
        champ = FIELD_BY_FR.get(nom)
        if champ is None:
            unknown.append(f"{where}.composition_pour_100g.{nom}")
        elif isinstance(valeur, (int, float)):
            composition[champ] = float(valeur)
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
        produit = data.get("produit") or {}
        out.append(Analysis(
            path=path,
            reference=str(data.get("reference") or path.stem),
            is_example=bool(data.get("exemple")),
            recette_code=produit.get("recette_code"),
            lot_id=produit.get("lot_id"),
            matiere_premiere=_sample(data.get("matiere_premiere"), "matiere_premiere", unknown),
            avant=_sample(data.get("avant_fermentation"), "avant_fermentation", unknown),
            apres=_sample(data.get("apres_fermentation"), "apres_fermentation", unknown),
            unknown_fields=unknown,
        ))
    return out


@dataclass
class Deviation:
    """Écart entre ce que l'application prédit et ce que le labo a mesuré."""
    field: str
    predicted: float
    measured: float
    tolerance: float

    @property
    def delta(self) -> float:
        return round(self.predicted - self.measured, 3)

    @property
    def within(self) -> bool:
        """Dans la tolérance réglementaire — le seul seuil qui ait un sens ici."""
        return abs(self.predicted - self.measured) <= self.tolerance


def predict_after_fermentation(analysis: Analysis) -> dict[str, float]:
    """Ce que l'application prédit pour l'« après », partant de l'« avant ».

    On IMPOSE les transformations (`fermentation` seule) au lieu de s'en
    remettre à une catégorie : l'échantillon a déjà trempé et cuit, et aucune
    catégorie du référentiel ne décrit cet état intermédiaire.
    """
    from zyfenutri.engine import estimate_batch_nutrition

    result = estimate_batch_nutrition(
        harvest_weight_g=analysis.apres.masse_g,
        ingredients=[{
            "input_type_name": analysis.reference,
            "category": None,
            "spec_identifier": None,
            "net_weight_g": analysis.avant.masse_g,
            "gross_weight_g": None,
            "dehulled": False,
            # L'échantillon a déjà trempé et cuit : seule la FERMENTATION reste
            # à appliquer. Lui remettre le lessivage compterait deux fois une
            # perte déjà subie.
            "transformations": ("fermentation",),
            "composition": analysis.avant.composition,
        }],
    )
    return {k: v for k, v in result.per_100g.items() if v is not None}


def fermentation_deviations(analysis: Analysis) -> list[Deviation]:
    """Prédit vs mesuré, nutriment par nutriment. `[]` si non exploitable."""
    from zyfenutri.annexe_xiv import tolerance_for

    if not (analysis.avant.usable and analysis.apres.usable):
        return []
    predit = predict_after_fermentation(analysis)
    return [
        Deviation(
            field=champ,
            predicted=predit[champ],
            measured=analysis.apres.composition[champ],
            tolerance=tolerance_for(champ, analysis.apres.composition[champ]),
        )
        for champ in NUTRIENT_FIELDS
        if champ in predit and champ in analysis.apres.composition
    ]
