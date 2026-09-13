"""**zyfenutri** — composition nutritionnelle du tempeh.

Le calcul qui transforme *ce qu'on a mis dans le lot* en *ce qu'on écrit sur
l'étiquette*. Pas de serveur, pas de base de données, pas de dépendance : une
bibliothèque pure et un script.

    from zyfenutri import estimate, declared_values

    resultat = estimate(
        harvest_weight_g=1750,
        ingredients=[{
            "input_type_name": "Soja", "category": "substrate",
            "net_weight_g": 1000, "composition": {...},
        }],
    )

En ligne de commande, le même calcul lit du JSON sur l'entrée standard :

    echo '{"harvest_weight_g": 1750, "ingredients": [...]}' | python -m zyfenutri

⚠️ **Ce paquet ne décide de rien.** Il applique des règles documentées à des
données qu'on lui donne, et rend la chaîne de calcul déroulée (`steps`) pour
qu'elle soit contestable. La méthode et ce qui la fonde sont dans
`refs/methode.md` — c'est ce document qu'on présente à un contrôle.
"""
from zyfenutri.annexe_xiv import (
    KCAL_PER_G,
    KJ_PER_G,
    NUTRIENT_FIELDS,
    NUTRIENT_LABELS,
    declared_value,
    declared_values,
    energy_kcal,
    energy_kj,
    tolerance_for,
)
from zyfenutri.engine import (
    DEFAULT_COEFFICIENTS,
    EXCLUS,
    PIPELINE,
    BatchNutrition,
    IngredientContribution,
    estimate_batch_nutrition as estimate,
)
from zyfenutri.sheet import (
    MASS_BALANCE_MAX_G,
    MASS_BALANCE_SUSPECT_G,
    check_nutrients,
    mass_balance,
)

__version__ = "1.0.0"

__all__ = [
    "estimate", "BatchNutrition", "IngredientContribution",
    "DEFAULT_COEFFICIENTS", "PIPELINE", "EXCLUS",
    "NUTRIENT_FIELDS", "NUTRIENT_LABELS", "KJ_PER_G", "KCAL_PER_G",
    "energy_kj", "energy_kcal", "declared_value", "declared_values",
    "tolerance_for", "mass_balance", "check_nutrients",
    "MASS_BALANCE_MAX_G", "MASS_BALANCE_SUSPECT_G", "__version__",
]
