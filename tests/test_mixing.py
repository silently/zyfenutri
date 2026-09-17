"""Mixing: the one place the product mass enters."""
import pytest

from zyfenutri import NutritionFacts, Portion, mix

SOY = NutritionFacts(fat=20.0, saturates=3.0, carbs=30.0, sugars=7.0,
                     fibre=20.0, protein=36.0, salt=0.02)
VINEGAR = NutritionFacts(fat=0.0, saturates=0.0, carbs=0.93, sugars=0.4,
                         fibre=0.0, protein=0.0, salt=0.013)


def test_an_ingredient_added_as_is_keeps_its_sheet():
    """Vinegar: no transform, yield 1. What goes in is what comes out."""
    out = mix([Portion(VINEGAR, raw_mass=50)])
    for name, value in VINEGAR.as_dict().items():
        assert getattr(out, name) == pytest.approx(value)


def test_water_uptake_is_carried_by_the_yield_alone():
    """Doubling in weight halves every value, with no coefficient saying so."""
    dry = mix([Portion(SOY, raw_mass=1000, yield_factor=1.0)])
    wet = mix([Portion(SOY, raw_mass=1000, yield_factor=2.0)])
    assert wet.protein == pytest.approx(dry.protein / 2)


def test_a_mix_is_weighted_by_raw_mass():
    out = mix([Portion(SOY, raw_mass=1000, yield_factor=1.75),
               Portion(VINEGAR, raw_mass=50)])
    assert out.protein == pytest.approx(1000 * 0.36 / (1750 + 50) * 100)


def test_a_weighed_product_mass_beats_the_prediction():
    out = mix([Portion(SOY, raw_mass=1000, yield_factor=1.75)], product_mass=2000)
    assert out.protein == pytest.approx(360 / 2000 * 100)


def test_a_nutrient_unknown_for_one_portion_is_unknown_for_the_mix():
    out = mix([Portion(SOY, raw_mass=1000), Portion(NutritionFacts(fat=1.0), raw_mass=10)])
    assert out.protein is None
    assert out.fat is not None


def test_nothing_to_mix_is_refused():
    with pytest.raises(ValueError):
        mix([])
