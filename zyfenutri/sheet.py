"""Ce qu'une composition pour 100 g a le droit d'être.

Les bornes physiques d'une fiche, indépendantes de tout produit et de toute
base de données : rien ne peut être négatif, rien ne peut dépasser 100 g dans
100 g, un « dont » ne peut pas dépasser son total, et la somme de ce qui
s'additionne ne peut pas dépasser 100 g.

⚠️ **Module sans dépendance**, comme tout ce paquet : ces règles doivent
pouvoir servir à qui veut vérifier une fiche, sans traîner un ORM ni un
framework web derrière elles.
"""
from __future__ import annotations

#: Les 7 valeurs d'une fiche, pour 100 g.
NUTRIENTS = ("fat_g", "saturates_g", "carbohydrates_g", "sugars_g",
             "fibre_g", "protein_g", "salt_g")

#: ⚠️ Les composants qui s'ADDITIONNENT. Pas les sept : les AGS sont une part
#: des matières grasses et les sucres une part des glucides — les compter
#: séparément doublerait leur masse.
ADDITIVE = ("fat_g", "carbohydrates_g", "fibre_g", "protein_g", "salt_g")

#: Les deux « dont », et leur total.
SUBSET_OF = {"saturates_g": "fat_g", "sugars_g": "carbohydrates_g"}

#: Au-delà, la fiche est **impossible**. La marge couvre les arrondis
#: réglementaires — quatre valeurs ≥ 10 g arrondies au gramme peuvent gonfler
#: la somme de 2 g sans que rien ne soit faux.
MASS_BALANCE_MAX_G = 102.0

#: Au-delà, elle est **suspecte** sans être impossible : il ne resterait presque
#: rien pour l'eau et les cendres, qu'aucun aliment courant n'a à zéro (un corps
#: gras pur approche les 100 g, d'où un simple avertissement).
MASS_BALANCE_SUSPECT_G = 95.0


def mass_balance(values: dict) -> float | None:
    """Somme des macronutriments qui s'additionnent, en g pour 100 g.

    `None` si aucune valeur n'est saisie — on ne juge pas une fiche vide.

    ⚠️ Ce contrôle ne demande **aucune donnée supplémentaire** : ce qui reste
    sous 100 g est forcément de l'eau et des cendres. Il suffit à attraper une
    fiche physiquement impossible.
    """
    presents = [values.get(f) for f in ADDITIVE if values.get(f) is not None]
    return round(sum(presents), 2) if presents else None


def check_nutrients(values: dict) -> None:
    """Lève `ValueError` si la composition est impossible.

    Négatif impossible, et rien ne peut dépasser 100 g dans 100 g de produit.
    Les deux « dont » sont bornés par leur total : des acides gras saturés
    supérieurs aux matières grasses est la faute de saisie la plus courante, et
    elle passerait inaperçue sur l'étiquette.
    """
    for field in NUTRIENTS:
        v = values.get(field)
        if v is None:
            continue
        if v < 0:
            raise ValueError(f"{field} ne peut pas être négatif")
        if v > 100:
            raise ValueError(f"{field} ne peut pas dépasser 100 g pour 100 g")
    for subset, total in SUBSET_OF.items():
        sub, tot = values.get(subset), values.get(total)
        if sub is not None and tot is not None and sub > tot:
            raise ValueError(f"{subset} ne peut pas dépasser {total} (c'est une part de ce total)")

    somme = mass_balance(values)
    if somme is not None and somme > MASS_BALANCE_MAX_G:
        raise ValueError(
            f"Les macronutriments totalisent {somme:.1f} g pour 100 g de produit : "
            "c'est impossible. Vérifiez la fiche — une valeur est fausse, ou elle "
            "est exprimée sur matière sèche."
        )
