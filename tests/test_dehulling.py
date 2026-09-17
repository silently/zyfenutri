"""Dehulling: the hull is mostly fibre, so it does not take its share of everything."""
import pytest

from zyfenutri import Dehulling, Transform


def test_other_nutrients_lose_far_less_than_the_hull_weighs(soy):
    """The hull is 9 % of the seed, but protein loses much less than 9 %."""
    assert 0.98 < Dehulling()(soy).protein / soy.protein < 1.0


def test_the_hull_takes_half_the_fibre(soy):
    """[1, p. 60]: the hull, 8-10 % of the seed, holds half of its fibre."""
    assert Dehulling()(soy).fibre == pytest.approx(soy.fibre / 2)


def test_the_hull_takes_its_protein(soy):
    """Cowan 1969 [12, p. 188]: hulls are 8.8 % protein; 9 g of hull per 100 g."""
    assert Dehulling()(soy).protein == pytest.approx(40.0 - 9 * 0.088)


def test_sugars_and_starch_stay(soy):
    out = Dehulling()(soy)
    assert (out.carbs, out.sugars) == (soy.carbs, soy.sugars)


def test_is_a_transform_without_setting():
    step = Dehulling()
    assert isinstance(step, Transform)
    assert step.label == "Dépelliculage"


@pytest.mark.skip(reason="à recouper : composition de pellicule hors soja (docs/A-LIRE.md, LWT 2014)")
def test_hull_composition_holds_for_other_seeds():
    """Cowan 1969 and [1] describe soybean hulls only."""


@pytest.mark.skip(reason="GAP: germ loss not modelled")
def test_germ_loss():
    """[1, p. 60]: the germ is 3 % of a soybean and often lost."""
