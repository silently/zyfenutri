"""Fermentation: what the mould breathes away."""
import pytest

from zyfenutri import Fermentation, Transform


def test_protein_is_barely_lost(soy):
    """[9, p. 797]: 10 g per kg of dry cotyledons oxidised at 46 h, ~2 % of protein."""
    assert Fermentation(46)(soy).protein / soy.protein == pytest.approx(0.978, abs=0.001)


def test_protein_loss_grows_with_time(soy):
    assert Fermentation(72)(soy).protein < Fermentation(28)(soy).protein


def test_protein_beyond_known_times_is_unknown(soy):
    assert Fermentation(96)(soy).protein is None


def test_minerals_are_not_consumed(soy):
    assert Fermentation(36)(soy).salt == soy.salt


def test_fat_loses_about_a_tenth_by_32_hours(soy):
    """[9, p. 797] over [7, table 1]: 3 % of dry matter, ~11 % of fat."""
    assert Fermentation(32)(soy).fat / soy.fat == pytest.approx(0.89)


def test_fat_loss_holds_until_48_hours(soy):
    """[2] and [7] at 46-48 h, with ~10 % of dry matter lost [6]."""
    assert Fermentation(48)(soy).fat == Fermentation(32)(soy).fat


def test_fat_beyond_48_hours_is_unknown(soy):
    """GAP: senescence burns fat fast [9, p. 797]."""
    assert Fermentation(60)(soy).fat is None


def test_saturates_follow_fat(soy):
    out = Fermentation(36)(soy)
    assert out.saturates / soy.saturates == pytest.approx(out.fat / soy.fat)


def test_sucrose_drops_by_a_sixth_in_48_hours(soy):
    """Shallenberger 1976 [12, p. 194]: sucrose −17 % over 48 h."""
    assert Fermentation(48)(soy).sugars / soy.sugars == pytest.approx(0.83)


def test_starch_is_mostly_consumed_by_48_hours(soy):
    """[8, p. 624-625]: soybean starch 0.4 → 0.1 %, field bean −74 %."""
    out = Fermentation(48)(soy)
    assert (out.carbs - out.sugars) / (soy.carbs - soy.sugars) == pytest.approx(0.25)


def test_carbs_beyond_48_hours_are_unknown(soy):
    assert Fermentation(60)(soy).carbs is None


def test_fibre_is_held(soy):
    """Hypothesis: most studies find it rising [12, p. 195]; holding it under-declares."""
    assert Fermentation(36)(soy).fibre == soy.fibre


def test_is_a_transform():
    step = Fermentation(hours=36)
    assert isinstance(step, Transform)
    assert step.label == "Fermentation 36 h"


def test_a_negative_time_is_refused():
    with pytest.raises(ValueError):
        Fermentation(-1)


@pytest.mark.skip(reason="to check against Ruiz-Terán & Owens 1996, and [10]'s 30 %")
def test_fat_loss_matches_the_primary_source():
    """The 11 % estimate rests on two reviews and two %-of-dry-matter series."""


@pytest.mark.skip(reason="GAP: fibre gain from mycelium needs the dry-matter loss")
def test_fibre_rises():
    """[9, p. 798]: 3.7 → 5.8 % of dry matter."""
