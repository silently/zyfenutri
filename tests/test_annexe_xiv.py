"""Coefficients d'énergie de l'annexe XIV — le calcul, pas la recopie."""
import pytest

from zyfenutri.annexe_xiv import NUTRIENT_FIELDS, energy_kcal, energy_kj


def test_energy_uses_annex_xiv_factors():
    # lipides 37, glucides 17, protéines 17, fibres 8 kJ/g
    assert energy_kj(fat=10, carbohydrates=0, protein=0, fibre=0) == 370.0
    assert energy_kj(fat=0, carbohydrates=10, protein=0, fibre=0) == 170.0
    assert energy_kj(fat=0, carbohydrates=0, protein=10, fibre=0) == 170.0
    assert energy_kj(fat=0, carbohydrates=0, protein=0, fibre=10) == 80.0

    # lipides 9, glucides 4, protéines 4, fibres 2 kcal/g
    assert energy_kcal(fat=10, carbohydrates=0, protein=0, fibre=0) == 90.0
    assert energy_kcal(fat=0, carbohydrates=10, protein=0, fibre=0) == 40.0
    assert energy_kcal(fat=0, carbohydrates=0, protein=10, fibre=0) == 40.0
    assert energy_kcal(fat=0, carbohydrates=0, protein=0, fibre=10) == 20.0


def test_fibre_counts_towards_energy():
    """Les omettre sous-déclare l'énergie d'un produit qui en est riche, ce
    qu'est le tempeh."""
    sans = energy_kj(fat=5, carbohydrates=12, protein=18, fibre=0)
    avec = energy_kj(fat=5, carbohydrates=12, protein=18, fibre=6)
    assert avec - sans == pytest.approx(48.0)      # 8 kJ/g × 6 g


def test_kcal_is_not_kj_divided_by_4184():
    """L'annexe XIV donne deux jeux de coefficients : convertir ferait diverger
    les deux chiffres de l'étiquette."""
    kj = energy_kj(fat=5, carbohydrates=12, protein=18, fibre=6)
    kcal = energy_kcal(fat=5, carbohydrates=12, protein=18, fibre=6)
    assert kj == 743.0 and kcal == 177.0
    assert kcal != round(kj / 4.184, 1)


def test_a_missing_macro_yields_no_energy():
    """Mieux vaut ne rien afficher qu'un total amputé d'un nutriment."""
    assert energy_kj(fat=None, carbohydrates=12, protein=18, fibre=6) is None
    assert energy_kcal(fat=5, carbohydrates=12, protein=18, fibre=None) is None


def test_seven_fields_are_declared():
    """7 saisis + l'énergie en kJ et en kcal = les 9 valeurs de l'étiquette."""
    assert len(NUTRIENT_FIELDS) == 7
    assert "salt_g" in NUTRIENT_FIELDS and "fibre_g" in NUTRIENT_FIELDS


# --- Arrondis réglementaires (tableau 4, guide de décembre 2012) --------------

def test_rounding_follows_the_commission_table():
    """Vérifié sur le document source le 2026-09-12, point 6, tableau 4."""
    from zyfenutri.annexe_xiv import declared_value

    # Énergie : à l'unité, sans décimale.
    assert declared_value("energy_kj", 1096.4) == "1096 kJ"
    assert declared_value("energy_kcal", 262.2) == "262 kcal"

    # Macros : ≥ 10 g au gramme, entre 0,5 et 10 g au décigramme.
    assert declared_value("protein_g", 20.9) == "21 g"
    assert declared_value("fibre_g", 8.08) == "8,1 g"
    # ≤ 0,5 g : « 0 g » ou « < 0,5 g » autorisé.
    assert declared_value("sugars_g", 0.3) == "< 0,5 g"

    # Acides gras saturés : seuil négligeable à 0,1 g, pas 0,5.
    assert declared_value("saturates_g", 0.05) == "< 0,1 g"
    assert declared_value("saturates_g", 1.7) == "1,7 g"

    # Sel : ≥ 1 g au décigramme, en dessous au centigramme.
    assert declared_value("salt_g", 1.4) == "1,4 g"
    assert declared_value("salt_g", 0.35) == "0,35 g"


def test_salt_is_never_zero_and_is_declared_below_the_negligible_threshold():
    """Le sel d'un tempeh n'est pas ajouté : c'est le sodium naturellement
    présent dans les intrants. Il n'est donc jamais nul — et il reste toujours
    sous le seuil de négligeabilité, d'où « < 0,01 g » sur toutes nos
    étiquettes : exactement la mention prévue par le tableau 4."""
    from zyfenutri.annexe_xiv import SALT_DECLARED_MENTION, SALT_NEGLIGIBLE_G, declared_value

    # ⚠️ Seuil et mention DIFFÈRENT : négligeable sous 0,0125 g, mention
    # « < 0,01 g ». Imprimer le seuil donnerait « < 0,0125 g », qu'on ne lit
    # sur aucune étiquette.
    assert SALT_NEGLIGIBLE_G == 0.0125
    assert SALT_DECLARED_MENTION == "0,01"
    for minuscule in (0.004, 0.01, 0.0125):
        assert declared_value("salt_g", minuscule) == "< 0,01 g"
    # Au-dessus du seuil, on redonne la valeur, au centigramme.
    assert declared_value("salt_g", 0.02) == "0,02 g"


def test_an_unknown_value_has_no_declared_form():
    """Un tiret à l'écran, jamais un zéro : « 0 g » est une affirmation."""
    from zyfenutri.annexe_xiv import declared_value, declared_values

    assert declared_value("protein_g", None) is None
    assert declared_values({"protein_g": None})["protein_g"] is None
