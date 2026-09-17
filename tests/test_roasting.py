"""Roasting: water leaves, nothing on the sheet moves."""
import pytest

from zyfenutri import Roasting, Transform


def test_roasting_changes_none_of_the_seven_values(soy):
    """[13, table 1]: 110 °C for 10 min leaves soybean flour unchanged on dry basis."""
    assert Roasting()(soy) == soy


def test_is_a_transform_without_setting():
    step = Roasting()
    assert isinstance(step, Transform)
    assert step.label == "Torréfaction"


def test_even_a_strong_roast_keeps_the_sugars(soy):
    """[18, table 6]: sucrose not significantly lower after 3 h of drum roasting."""
    assert Roasting()(soy).sugars == soy.sugars


@pytest.mark.skip(reason="TODO important : fibres après une torréfaction forte (produits de Maillard)")
def test_a_strong_roast_and_fibre():
    """Maillard products may be counted as fibre; no measure yet."""
