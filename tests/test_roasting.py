"""Roasting: water leaves, Maillard eats sugars."""
import pytest

from zyfenutri import Roasting, Transform


def test_fat_protein_and_salt_do_not_move(soy):
    out = Roasting(2)(soy)
    assert (out.fat, out.protein, out.salt) == (soy.fat, soy.protein, soy.salt)


def test_light_roasting_changes_nothing(soy):
    """[13, table 1]: 110 °C for 10 min leaves soybean flour unchanged on dry basis."""
    assert Roasting(1)(soy) == soy


@pytest.mark.parametrize("name", ["carbs", "sugars", "fibre"])
def test_darker_roasts_are_unknown(soy, name):
    """GAP: no source beyond a light roast."""
    assert getattr(Roasting(2)(soy), name) is None


def test_is_a_transform():
    step = Roasting(intensity=3)
    assert isinstance(step, Transform)
    assert step.label == "Torréfaction (intensité 3)"


@pytest.mark.parametrize("intensity", [0, 4])
def test_intensity_is_one_to_three(intensity):
    with pytest.raises(ValueError):
        Roasting(intensity)


@pytest.mark.skip(reason="GAP: sugar loss per intensity to source")
def test_darker_roasting_loses_more_sugars():
    """Maillard consumes more reducing sugars as intensity rises."""
