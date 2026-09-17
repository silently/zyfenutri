"""Dehulling: the hull is mostly fibre, so it does not take its share of everything."""
import pytest

from zyfenutri import Dehulling, Transform


def test_no_hull_changes_nothing_but_fibre(soy):
    out = Dehulling(0)(soy)
    assert (out.fat, out.protein, out.carbs) == (soy.fat, soy.protein, soy.carbs)


def test_other_nutrients_lose_far_less_than_the_hull_weighs(soy):
    """9 % of the mass leaves, but protein loses much less than 9 %."""
    out = Dehulling(0.09)(soy)
    assert 0.98 < out.protein / soy.protein < 1.0


def test_fraction_from_the_two_weighings():
    assert Dehulling.from_weights(1100, 1000).hull_fraction == pytest.approx(1 / 11)


def test_the_hull_takes_half_the_fibre(soy):
    """[1, p. 60]: the hull, 8-10 % of the seed, holds half of its fibre."""
    assert Dehulling(0.09)(soy).fibre == pytest.approx(soy.fibre / 2)


def test_the_hull_takes_its_protein(soy):
    """Cowan 1969 [12, p. 188]: hulls are 8.8 % protein."""
    assert Dehulling(0.09)(soy).protein == pytest.approx(40.0 - 9 * 0.088)


def test_is_a_transform():
    assert isinstance(Dehulling(0.09), Transform)


@pytest.mark.parametrize("fraction", [-0.1, 1.0])
def test_a_nonsense_fraction_is_refused(fraction):
    with pytest.raises(ValueError):
        Dehulling(fraction)


@pytest.mark.skip(reason="à recouper : composition de pellicule hors soja (docs/A-LIRE.md, LWT 2014)")
def test_hull_composition_holds_for_other_seeds():
    """Cowan 1969 and [1] describe soybean hulls only."""


@pytest.mark.skip(reason="GAP: germ loss not modelled")
def test_germ_loss():
    """[1, p. 60]: the germ is 3 % of a soybean and often lost."""
