"""Fermentation: what the mould breathes away."""
import pytest

from zyfenutri import Fermentation, NutritionFacts, Transform


def test_protein_is_barely_lost(soy):
    """[9, p. 797]: 10 g per kg of dry cotyledons oxidised at 46 h, ~2 % of protein."""
    assert Fermentation(46)(soy).protein / soy.protein == pytest.approx(0.978, abs=0.001)


def test_protein_loss_grows_with_time(soy):
    assert Fermentation(72)(soy).protein < Fermentation(28)(soy).protein


def test_protein_beyond_known_times_is_unknown(soy):
    assert Fermentation(96)(soy).protein is None


def test_minerals_are_not_consumed(soy):
    assert Fermentation(36)(soy).salt == soy.salt


def test_mature_tempe_loses_about_an_eighth_of_its_fat(soy):
    """[16, table 1]: crude lipid 243 → 211-216 g/kg of initial dry matter, 26-60 h."""
    assert Fermentation(32)(soy).fat / soy.fat == pytest.approx(0.88)


def test_fat_loss_holds_until_48_hours(soy):
    """[16, table 1]: no change from 26 to 60 h."""
    assert Fermentation(48)(soy).fat == Fermentation(32)(soy).fat


def test_senescence_burns_fat(soy):
    """[16, table 1]: 99 g/kg left at 120 h, 81 g/kg at 180 h."""
    assert Fermentation(120)(soy).fat / soy.fat == pytest.approx(0.41)
    assert Fermentation(200)(soy).fat is None


def test_the_saturated_share_of_fat_rises(soy):
    """Calibrated on refs/official: +3.8 to +10.8 points, +7.9 on average."""
    out = Fermentation(36)(soy)
    assert out.saturates / out.fat == pytest.approx(soy.saturates / soy.fat + 0.079)


def test_saturates_never_exceed_fat():
    out = Fermentation(36)(NutritionFacts(fat=10.0, saturates=9.8))
    assert out.saturates <= out.fat


def test_saturates_beyond_60_hours_are_unknown(soy):
    assert Fermentation(120)(soy).saturates is None


def test_sucrose_drops_by_a_sixth_in_48_hours(soy):
    """Shallenberger 1976 [12, p. 194]: sucrose −17 % over 48 h."""
    assert Fermentation(48)(soy).sugars / soy.sugars == pytest.approx(0.83)


def test_about_a_third_of_the_starch_is_consumed(soy):
    """[15]: 62-76 % of nitrogen-free extract kept for faba bean, chickpea and pea."""
    out = Fermentation(37.5)(soy)
    assert (out.carbs - out.sugars) / (soy.carbs - soy.sugars) == pytest.approx(0.69)


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
