"""Physical bounds on a composition — no product, no regulation, just sense."""
import pytest

from zyfenutri import MASS_BALANCE_MAX_G, check, mass_balance

SHEET = {"fat": 20.0, "saturates": 2.9, "carbs": 15.0, "sugars": 5.7,
         "fibre": 15.0, "protein": 40.0, "salt": 0.01}


def test_mass_balance_adds_only_what_adds_up():
    """Saturates are part of fat and sugars part of carbs: counting them
    separately would double their mass."""
    assert mass_balance(SHEET) == pytest.approx(20 + 15 + 15 + 40 + 0.01)


def test_an_empty_sheet_is_not_judged():
    assert mass_balance({}) is None


def test_a_sheet_over_one_hundred_grams_is_refused():
    """Whatever is under 100 g is necessarily water and ash. This check needs
    no extra data, and it catches a physically impossible sheet."""
    with pytest.raises(ValueError, match="impossible"):
        check({"fat": 50.0, "carbs": 30.0, "protein": 30.0})
    assert MASS_BALANCE_MAX_G == 102.0


def test_rounding_gets_the_benefit_of_the_doubt():
    """Four values over 10 g rounded to the gram can inflate the sum by 2 g
    with nothing being wrong."""
    check({"fat": 25.0, "carbs": 25.0, "fibre": 25.0, "protein": 26.0})


def test_a_subset_cannot_exceed_its_total():
    """Saturates above fat is the most common typing mistake, and it would go
    unnoticed on the label."""
    with pytest.raises(ValueError, match="saturates"):
        check({"fat": 2.0, "saturates": 5.0})


def test_nothing_is_negative_and_nothing_exceeds_a_hundred():
    with pytest.raises(ValueError, match="negative"):
        check({"fat": -1.0})
    with pytest.raises(ValueError, match="100 g"):
        check({"fat": 120.0})
