"""Soaking overnight: what dissolves leaves, whatever the seed."""
import pytest

from zyfenutri import NutritionFacts, Soaking, Transform

SOY = NutritionFacts(fat=20.0, saturates=2.9, carbs=15.0, sugars=5.7,
                     fibre=15.0, protein=40.0, salt=0.01)
LENTIL = NutritionFacts(fat=1.5, saturates=0.2, carbs=48.0, sugars=2.0,
                        fibre=11.0, protein=24.0, salt=0.02)


def carbs_loss(facts: NutritionFacts) -> float:
    return 1 - Soaking()(facts).carbs / facts.carbs


def test_one_transform_serves_soy_and_lentil():
    """Soy carbs are mostly sugars, lentil carbs mostly starch: the same rule
    takes far more from soy, without knowing which seed it is soaking."""
    assert carbs_loss(SOY) > 5 * carbs_loss(LENTIL)


def test_sugars_follow_soybean_sucrose_over_a_night():
    """[14, table 2]: whole soybeans at 25 °C keep 74.6 % of sucrose at 12 h."""
    assert Soaking()(SOY).sugars / SOY.sugars == pytest.approx(0.746, abs=0.02)


def test_starch_stays_in_the_seed():
    out = Soaking()(LENTIL)
    assert out.carbs - out.sugars == pytest.approx(LENTIL.carbs - LENTIL.sugars)


def test_fat_loses_about_one_percent():
    """[12, p. 193]: −2.5 % after 24 h; half of it for a night."""
    assert Soaking()(SOY).fat / SOY.fat == pytest.approx(0.988)


def test_protein_and_minerals_leach():
    """[14, table 1]: ~3 % of protein; minerals at the pace of solids, ~5 %."""
    out = Soaking()(SOY)
    assert out.protein / SOY.protein == pytest.approx(0.97)
    assert out.salt / SOY.salt == pytest.approx(0.95)


def test_fibre_stays():
    assert Soaking()(SOY).fibre == SOY.fibre


def test_without_sugars_carbs_cannot_be_split():
    out = Soaking()(NutritionFacts(carbs=15.0, fat=20.0))
    assert out.carbs is None
    assert out.fat is not None


def test_a_sheet_with_sugars_above_carbs_has_no_starch():
    out = Soaking()(NutritionFacts(carbs=5.0, sugars=6.0))
    assert out.carbs == pytest.approx(out.sugars)


def test_soaking_is_a_transform_for_one_night():
    step = Soaking()
    assert isinstance(step, Transform)
    # ⚠️ Le libellé nomme le rinçage : les coefficients sont mesurés DANS
    # l'eau, donc ils supposent qu'on la retire en entier.
    assert step.label == "Trempage et rinçage (une nuit)"


@pytest.mark.skip(reason="GAP: protein loss on soaking not sourced (acidified vs plain)")
def test_acidified_soaking_keeps_protein():
    """[6, table 1]: acidification leaves protein insoluble. To write once a
    figure is found."""
