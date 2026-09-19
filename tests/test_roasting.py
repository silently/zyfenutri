"""Roasting: water leaves; Maillard takes some sugars, heat some fibre."""
import pytest

from zyfenutri import Roasting, Transform


def test_is_a_transform_without_setting():
    step = Roasting()
    assert isinstance(step, Transform)
    assert step.label == "Torréfaction"


def test_roasting_transforms_the_product(soy):
    """Roasted is not raw: something on the sheet moves."""
    assert Roasting()(soy) != soy


def test_maillard_takes_8_percent_of_the_sugars(soy):
    """MEXT 2020, soybean → kinako, dry basis: −7 % (yellow), −8 % (green)."""
    assert Roasting()(soy).sugars == pytest.approx(soy.sugars * 0.92)


def test_starch_stays_so_carbs_fall_by_the_sugars_alone(soy):
    """[19, table 1]: total starch unchanged on dry basis."""
    out = Roasting()(soy)
    assert soy.carbs - out.carbs == pytest.approx(soy.sugars - out.sugars)


def test_roasting_lowers_dietary_fibre(soy):
    """[19, table 1]: quinoa, 120 °C 8 min, 18.81 → 15.83 g of dry matter."""
    assert Roasting()(soy).fibre == pytest.approx(soy.fibre * 0.84)


def test_fat_protein_and_salt_do_not_move(soy):
    """[13, table 1], [19, table 1]: unchanged on dry basis."""
    out = Roasting()(soy)
    assert (out.fat, out.saturates, out.protein, out.salt) == \
           (soy.fat, soy.saturates, soy.protein, soy.salt)
