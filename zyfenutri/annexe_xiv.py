"""Valeurs nutritionnelles : les 7 macronutriments saisis, l'énergie calculée.

⚠️ **L'énergie ne se recopie jamais d'une table de composition.** Elle se
calcule depuis les macronutriments avec les coefficients de conversion de
l'**annexe XIV du règlement (UE) n° 1169/2011**. Recopier l'énergie d'une
table donne un chiffre incohérent avec ses propres macros — c'est précisément
ce qu'un contrôle recoupe en premier. Raisonnement complet : `refs/methode.md`.

Une fiche produit porte donc **7 champs**, tous pour 100 g, et l'application
en dérive les **2 expressions de l'énergie** (kJ et kcal) — soit les 9 valeurs
de l'étiquette.

⚠️ « Glucides » au sens INCO = glucides **assimilables**, fibres exclues.
Certaines tables donnent des glucides *totaux* : les confondre gonfle à la fois
les glucides et l'énergie.
"""
from __future__ import annotations

# Annexe XIV — coefficients de conversion, par gramme.
#
# ⚠️ **Quatre des huit coefficients seulement.** L'annexe en donne aussi pour
# les polyols (10), l'éthanol (29), les salatrims (25) et les **acides
# organiques (13 kJ/g)**. On ne les modélise pas parce qu'ils ne font pas
# partie des sept nutriments déclarés — mais la conséquence est réelle : sur un
# produit **acide**, le calcul sous-estime. Un vinaigre à 5 % d'acide acétique,
# c'est 65 kJ que ce calcul ne voit pas. Un écart avec une table Ciqual sur un
# vinaigre est donc **attendu**, pas suspect.
KJ_PER_G = {"fat": 37.0, "carbohydrates": 17.0, "protein": 17.0, "fibre": 8.0}
KCAL_PER_G = {"fat": 9.0, "carbohydrates": 4.0, "protein": 4.0, "fibre": 2.0}

#: L'annexe XIV donne aussi des coefficients pour ce qui ne se déclare pas.
#: Un seul nous concerne : les **acides organiques**. `energy_kj` ne les voit
#: jamais — ils ne font pas partie des sept — mais ils portent de l'énergie, et
#: c'est ce qui explique qu'une table en annonce plus que nos quatre macros
#: n'en impliquent. Sur un vinaigre, ils font 80 % du total.
#: Servent à **reconstituer** l'énergie d'une ligne Ciqual, jamais à déclarer
#: celle du produit.
#: ⚠️ L'alcool (29 kJ/g) et les polyols (10 kJ/g) ne sont pas modélisés : aucun
#: intrant courant du tempeh n'en contient. Les ajouter serait du code mort.
ORGANIC_ACIDS_KJ_PER_G = 13.0
ORGANIC_ACIDS_KCAL_PER_G = 3.0

# Les 7 champs saisis, dans l'ordre réglementaire d'affichage sur l'étiquette
# (l'énergie vient avant, mais elle n'est pas saisie).
NUTRIENT_FIELDS = (
    "fat_g",
    "saturates_g",
    "carbohydrates_g",
    "sugars_g",
    "fibre_g",
    "protein_g",
    "salt_g",
)

NUTRIENT_LABELS = {
    "fat_g": "Matières grasses",
    "saturates_g": "dont acides gras saturés",
    "carbohydrates_g": "Glucides",
    "sugars_g": "dont sucres",
    "fibre_g": "Fibres alimentaires",
    "protein_g": "Protéines",
    "salt_g": "Sel",
}

# Les deux couples « dont » : le sous-ensemble ne peut pas dépasser son total.
SUBSET_OF = {"saturates_g": "fat_g", "sugars_g": "carbohydrates_g"}


def energy_kj(fat: float | None, carbohydrates: float | None,
              protein: float | None, fibre: float | None) -> float | None:
    """kJ pour 100 g. `None` si une macro énergétique manque.

    Les fibres comptent (8 kJ/g) : les omettre sous-déclare l'énergie d'un
    produit qui en est riche, ce qu'est le tempeh.
    """
    return _energy(KJ_PER_G, fat, carbohydrates, protein, fibre)


def energy_kcal(fat: float | None, carbohydrates: float | None,
                protein: float | None, fibre: float | None) -> float | None:
    """kcal pour 100 g. Calculée depuis les macros, **pas** convertie des kJ :
    l'annexe XIV donne deux jeux de coefficients, et arrondir kJ/4,184 ferait
    diverger les deux chiffres de l'étiquette."""
    return _energy(KCAL_PER_G, fat, carbohydrates, protein, fibre)


def _energy(factors: dict[str, float], fat, carbohydrates, protein, fibre) -> float | None:
    # Une macro manquante rend l'énergie fausse, pas approximative : mieux vaut
    # ne rien afficher que d'annoncer un total amputé d'un nutriment.
    values = {"fat": fat, "carbohydrates": carbohydrates, "protein": protein, "fibre": fibre}
    if any(v is None for v in values.values()):
        return None
    return round(sum(factors[k] * v for k, v in values.items()), 1)


# ══════════════════════════════════════════════════════════════════════════════
#  Arrondis réglementaires — tableau 4 du guide de la Commission (déc. 2012),
#  point 6 « Règles d'arrondi des valeurs pour les denrées alimentaires ».
#  Vérifié sur le document source le 2026-09-12.
#
#  ⚠️ Ce guide n'a **aucune valeur juridique** (il le dit lui-même) : c'est un
#  outil à l'intention des autorités de contrôle. Mais c'est ce que le
#  contrôleur a sous les yeux, donc le repère à tenir.
# ══════════════════════════════════════════════════════════════════════════════

#: field → (seuil de négligeabilité, mention autorisée en dessous).
#: ⚠️ Le seuil et la mention **diffèrent** pour le sel : le tableau 4 le déclare
#: négligeable sous **0,0125 g**, mais la mention autorisée est « < 0,01 g ».
#: Imprimer le seuil donnerait « < 0,0125 g », qu'on ne lit sur aucune étiquette.
_NEGLIGIBLE = {
    "fat_g": (0.5, "0,5"),
    "carbohydrates_g": (0.5, "0,5"),
    "sugars_g": (0.5, "0,5"),
    "protein_g": (0.5, "0,5"),
    "fibre_g": (0.5, "0,5"),
    "saturates_g": (0.1, "0,1"),
    "salt_g": (0.0125, "0,01"),
}

#: ⚠️ Le sel d'un tempeh ne vient pas d'un ajout : c'est le sodium
#: naturellement présent dans les intrants. Il n'est donc **jamais nul**, et il
#: est toujours sous le seuil de négligeabilité — d'où « < 0,01 g » sur toutes
#: nos étiquettes, exactement la mention prévue par le tableau 4.
SALT_NEGLIGIBLE_G, SALT_DECLARED_MENTION = _NEGLIGIBLE["salt_g"]


def _fr(value: float, decimals: int) -> str:
    return f"{value:.{decimals}f}".replace(".", ",")


def declared_value(field: str, value: float | None) -> str | None:
    """La valeur telle qu'elle s'écrit sur l'étiquette, arrondis compris.

    Renvoie `None` si la valeur est inconnue — un tiret à l'écran, pas un zéro.
    """
    if value is None:
        return None

    if field in ("energy_kj", "energy_kcal"):
        # Énergie : à l'unité la plus proche, sans décimale.
        return f"{round(value):d} {'kJ' if field == 'energy_kj' else 'kcal'}"

    seuil, mention = _NEGLIGIBLE.get(field, (0.5, "0,5"))
    if value <= seuil:
        return f"< {mention} g"

    if field == "salt_g":
        # ≥ 1 g au décigramme, en dessous au centigramme (tableau 4).
        return (f"{_fr(round(value, 1), 1)} g" if value >= 1
                else f"{_fr(round(value, 2), 2)} g")
    if value >= 10:
        return f"{round(value):d} g"               # au gramme
    return f"{_fr(round(value, 1), 1)} g"          # au décigramme


def declared_values(values: dict[str, float | None]) -> dict[str, str | None]:
    """Les neuf valeurs de l'étiquette, mises en forme."""
    return {
        field: declared_value(field, values.get(field))
        for field in (*NUTRIENT_FIELDS, "energy_kj", "energy_kcal")
    }


# ══════════════════════════════════════════════════════════════════════════════
#  Tolérances — tableau 1 du même guide (décembre 2012), point 3
#  « Tolérances pour les denrées alimentaires ». Vérifié sur le document source
#  le 2026-09-12.
#
#  ⚠️ Ce n'est PAS « ± 20 % » partout : sous les seuils, c'est une tolérance
#  **absolue** qui s'applique, souvent bien plus généreuse. C'est l'idée reçue
#  la plus répandue sur le sujet (cf. refs/methode.md § 2).
#
#  ⚠️ La tolérance **inclut déjà l'incertitude de mesure** du laboratoire de
#  contrôle : inutile de la majorer.
# ══════════════════════════════════════════════════════════════════════════════

#: field → [(seuil, tolérance absolue ou None pour « ± 20 % »), …] appliqué en
#: ordre croissant de seuil ; `None` en seuil = au-delà de tout.
_TOLERANCES: dict[str, list[tuple[float | None, float | None]]] = {
    # Glucides, sucres, protéines, fibres : < 10 g → ± 2 g ; 10–40 g → ± 20 % ; > 40 g → ± 8 g
    "carbohydrates_g": [(10, 2.0), (40, None), (None, 8.0)],
    "sugars_g": [(10, 2.0), (40, None), (None, 8.0)],
    "protein_g": [(10, 2.0), (40, None), (None, 8.0)],
    "fibre_g": [(10, 2.0), (40, None), (None, 8.0)],
    # Matières grasses : < 10 g → ± 1,5 g ; 10–40 g → ± 20 % ; > 40 g → ± 8 g
    "fat_g": [(10, 1.5), (40, None), (None, 8.0)],
    # Acides gras saturés : < 4 g → ± 0,8 g ; ≥ 4 g → ± 20 %
    "saturates_g": [(4, 0.8), (None, None)],
    # Sel : < 1,25 g → ± 0,375 g ; ≥ 1,25 g → ± 20 %
    "salt_g": [(1.25, 0.375), (None, None)],
}

RELATIVE_TOLERANCE = 0.20


def tolerance_for(field: str, declared: float) -> float:
    """Tolérance **absolue**, en g, autour d'une valeur déclarée.

    C'est le seul seuil qui ait un sens pour juger une estimation face à un
    dosage : il dit si l'écart serait opposable au contrôle, là où un « écart
    de 30 % » ne dit rien tant qu'on ne sait pas sur quelle quantité.
    """
    for seuil, absolue in _TOLERANCES.get(field, [(None, None)]):
        if seuil is None or declared < seuil:
            return absolue if absolue is not None else round(declared * RELATIVE_TOLERANCE, 4)
    return round(declared * RELATIVE_TOLERANCE, 4)
