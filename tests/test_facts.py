"""A nutrition facts sheet, and the energy that follows from it."""
from dataclasses import FrozenInstanceError, fields

import pytest

from zyfenutri import NUTRIENTS, NutritionFacts, energy, energy_of

SOY = NutritionFacts(fat=20.0, saturates=2.9, carbs=15.0, sugars=5.7,
                     fibre=15.0, protein=40.0, salt=0.01)


def test_a_sheet_holds_the_seven_values_in_label_order():
    assert tuple(f.name for f in fields(NutritionFacts)) == NUTRIENTS


def test_an_unknown_value_is_not_a_zero():
    sheet = NutritionFacts(fat=20.0)
    assert sheet.protein is None
    assert "protein" in sheet.unknown and "fat" not in sheet.unknown


def test_a_sheet_cannot_be_edited_in_place():
    with pytest.raises(FrozenInstanceError):
        SOY.fat = 0.0


def test_input_aliases_are_accepted():
    assert NutritionFacts.from_mapping({"fat_g": 20, "proteines": 40}) == \
        NutritionFacts(fat=20.0, protein=40.0)


def test_energy_follows_from_the_sheet_in_either_unit():
    """Nothing to store: the four macros that carry energy are on the sheet."""
    assert energy_of(SOY, "kJ") == pytest.approx(20 * 37 + 15 * 17 + 40 * 17 + 15 * 8)
    assert energy_of(SOY, "kcal") == pytest.approx(20 * 9 + 15 * 4 + 40 * 4 + 15 * 2)


def test_energy_agrees_with_the_dictionary_version():
    kj, kcal = energy(SOY.as_dict())
    assert energy_of(SOY, "kJ") == pytest.approx(kj)
    assert energy_of(SOY, "kcal") == pytest.approx(kcal)


def test_no_energy_when_a_macro_is_unknown():
    assert energy_of(NutritionFacts(fat=20.0, carbs=15.0, protein=40.0), "kJ") is None


def test_an_unknown_unit_is_refused():
    with pytest.raises(ValueError):
        energy_of(SOY, "cal")
