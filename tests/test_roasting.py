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


@pytest.mark.skip(reason="GAP: sugar loss on a darker roast to source")
def test_a_dark_roast_loses_sugars():
    """Maillard consumes reducing sugars; no measure yet."""
