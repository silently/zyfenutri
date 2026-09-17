"""Cooking: boiling water thrown away."""
import pytest

from zyfenutri import Cooking, Transform


def test_no_cooking_changes_nothing(soy):
    assert Cooking(0)(soy) == soy


def test_fat_does_not_dissolve(soy):
    out = Cooking(30)(soy)
    assert (out.fat, out.saturates) == (soy.fat, soy.saturates)


def test_sugars_lose_what_soaking_left_to_leach(soy):
    """[12, p. 194]: −59 % over soaking and cooking; soaking keeps 73 % [14]."""
    assert Cooking(120)(soy).sugars / soy.sugars == pytest.approx(0.56, abs=0.005)


def test_starch_and_fibre_stay(soy):
    out = Cooking(60)(soy)
    assert out.carbs - out.sugars == pytest.approx(soy.carbs - soy.sugars)
    assert out.fibre == soy.fibre


def test_protein_and_minerals_leach(soy):
    """[12], [15]: ~8 % of protein; minerals ~2 % ([15]: ash 92-98 % kept overall)."""
    out = Cooking(120)(soy)
    assert out.protein / soy.protein == pytest.approx(0.92, abs=0.001)
    assert out.salt / soy.salt == pytest.approx(0.98, abs=0.001)


def test_is_a_transform():
    step = Cooking(minutes=30)
    assert isinstance(step, Transform)
    assert step.label == "Cuisson 30 min"


def test_a_negative_time_is_refused():
    with pytest.raises(ValueError):
        Cooking(-1)


@pytest.mark.skip(reason="à recouper hors soja avec [4] et [5]")
def test_cooking_losses_hold_for_lentils_and_chickpeas():
    """The coefficients come from soybeans [12]."""
