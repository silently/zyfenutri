"""Soaking: what dissolves leaves, whatever the seed."""
import pytest

from zyfenutri import NutritionFacts, Soaking, Transform

SOY = NutritionFacts(fat=20.0, saturates=2.9, carbs=15.0, sugars=5.7,
                     fibre=15.0, protein=40.0, salt=0.01)
LENTIL = NutritionFacts(fat=1.5, saturates=0.2, carbs=48.0, sugars=2.0,
                        fibre=11.0, protein=24.0, salt=0.02)


def carbs_loss(facts: NutritionFacts, hours: float) -> float:
    return 1 - Soaking(hours)(facts).carbs / facts.carbs


def test_one_transform_serves_soy_and_lentil():
    """Soy carbs are mostly sugars, lentil carbs mostly starch: the same rule
    takes far more from soy, without knowing which seed it is soaking."""
    assert carbs_loss(SOY, 12) > 5 * carbs_loss(LENTIL, 12)


def test_starch_stays_in_the_seed():
    out = Soaking(12)(LENTIL)
    assert out.carbs - out.sugars == pytest.approx(LENTIL.carbs - LENTIL.sugars)


def test_fat_loses_a_little_in_a_day():
    """[12, p. 193]: 24 h in room-temperature water, fat −2.5 %."""
    assert Soaking(24)(SOY).fat / SOY.fat == pytest.approx(0.975)


def test_fat_beyond_a_day_is_unknown():
    """GAP: longer soaks lose much more, faster when warm [12, p. 193]."""
    assert Soaking(36)(SOY).fat is None


def test_protein_and_minerals_leach_steadily():
    """[13], [14]: ~6 % of protein and ~5 % of minerals by 24 h, at a steady rate."""
    assert Soaking(24)(SOY).protein / SOY.protein == pytest.approx(0.94)
    assert Soaking(24)(SOY).salt / SOY.salt == pytest.approx(0.95)
    assert Soaking(12)(SOY).protein / SOY.protein == pytest.approx(0.97)


def test_protein_beyond_a_day_is_unknown():
    """GAP: losses keep growing past 24 h [13, table 1]."""
    assert Soaking(48)(SOY).protein is None


def test_fibre_stays():
    assert Soaking(12)(SOY).fibre == SOY.fibre


def test_no_soaking_changes_nothing():
    assert Soaking(0)(SOY) == SOY


def test_the_loss_levels_off():
    """Once the soluble part is gone, soaking longer takes almost nothing more."""
    assert carbs_loss(SOY, 6) < carbs_loss(SOY, 24)
    assert carbs_loss(SOY, 48) == pytest.approx(carbs_loss(SOY, 72), abs=1e-4)


def test_without_sugars_carbs_cannot_be_split():
    out = Soaking(12)(NutritionFacts(carbs=15.0, fat=20.0))
    assert out.carbs is None
    assert out.fat is not None


def test_a_sheet_with_sugars_above_carbs_has_no_starch():
    out = Soaking(12)(NutritionFacts(carbs=5.0, sugars=6.0))
    assert out.carbs == pytest.approx(out.sugars)


def test_soaking_is_a_transform():
    step = Soaking(hours=12)
    assert isinstance(step, Transform)
    assert step.label == "Trempage 12 h"


def test_a_negative_time_is_refused():
    with pytest.raises(ValueError):
        Soaking(-1)


def test_sugars_follow_soybean_raffinose_leaching():
    """[3, table II, p. 431]: soybean raffinose 60.1 mg/g raw, 40.1 after 3 h
    of soaking, 26.3 after 12 h."""
    sheet = NutritionFacts(carbs=10.0, sugars=10.0)
    assert Soaking(3)(sheet).sugars / 10.0 == pytest.approx(40.1 / 60.1, abs=0.01)
    assert Soaking(12)(sheet).sugars / 10.0 == pytest.approx(26.3 / 60.1, abs=0.01)


@pytest.mark.skip(reason="GAP: protein loss on soaking not sourced (acidified vs plain)")
def test_acidified_soaking_keeps_protein():
    """[6, table 1]: acidification leaves protein insoluble. To write once a
    figure is found."""
