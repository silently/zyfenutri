"""Annex XIV energy, table 4 rounding, table 1 tolerances.

These are legal figures, checked against the source documents on 2026-09-12.
They are not opinions, and a failure here means the label would be wrong.
"""
import pytest

from zyfenutri import declared, declared_label, energy, tolerance
from zyfenutri.label import SALT_DECLARED_MENTION, SALT_NEGLIGIBLE_G

SHEET = {"fat": 10.0, "carbs": 5.0, "protein": 20.0, "fibre": 6.0}


def test_energy_uses_annex_xiv_factors():
    kj, kcal = energy(SHEET)
    assert kj == pytest.approx(10 * 37 + 5 * 17 + 20 * 17 + 6 * 8)
    assert kcal == pytest.approx(10 * 9 + 5 * 4 + 20 * 4 + 6 * 2)


def test_kcal_is_not_kj_divided_by_4184():
    """Annex XIV gives two independent sets of factors. Converting would make
    the two printed figures disagree with each other."""
    kj, kcal = energy(SHEET)
    assert kcal != pytest.approx(kj / 4.184, rel=1e-3)


def test_a_missing_macro_yields_no_energy_at_all():
    """Better nothing than an energy short of one nutrient."""
    assert energy({**SHEET, "fibre": None}) == (None, None)


@pytest.mark.parametrize("name, value, written", [
    ("fat", 12.4, "12 g"),          # >= 10 g : to the gram
    ("fat", 9.54, "9,5 g"),         # < 10 g : to the decigram
    ("fat", 0.4, "< 0,5 g"),        # negligible
    ("saturates", 0.05, "< 0,1 g"), # saturates have a lower threshold
    ("salt", 1.44, "1,4 g"),        # >= 1 g : decigram
    ("salt", 0.35, "0,35 g"),       # < 1 g : centigram
    ("energy_kj", 876.3, "876 kJ"),
    ("energy_kcal", 210.4, "210 kcal"),
])
def test_rounding_follows_table_4(name, value, written):
    assert declared(name, value) == written


def test_an_unknown_value_has_no_written_form():
    """A dash on screen, never a zero: "0 g" is a claim."""
    assert declared("fat", None) is None


def test_salt_is_never_zero_and_is_written_below_the_threshold():
    """A tempeh's salt is not added: it is the sodium naturally in the inputs.
    So it is never nil, and always under the negligibility threshold."""
    assert SALT_NEGLIGIBLE_G == 0.0125
    assert SALT_DECLARED_MENTION == "0,01"
    # The threshold and the printed text differ: printing the threshold would
    # give "< 0,0125 g", which appears on no label anywhere.
    for tiny in (0.004, 0.01, 0.0125):
        assert declared("salt", tiny) == "< 0,01 g"
    assert declared("salt", 0.02) == "0,02 g"


def test_energy_is_not_rounded():
    """`declared` rounds to the whole unit. Rounding here too would move that
    figure: 577.481 kJ through the decigram is 577.5, which prints "578 kJ"."""
    kj, _ = energy({"fat": 3.013, "carbs": 20.0, "protein": 6.0, "fibre": 3.0})
    assert kj == pytest.approx(577.481)
    assert declared("energy_kj", kj) == "577 kJ"
    assert declared("energy_kj", round(kj, 1)) == "578 kJ"  # what two rounds would give


@pytest.mark.parametrize("name, value, written", [
    ("protein", 2.449, "2,4 g"),   # through the centigram: 2.45, printed "2,5 g"
    ("fibre", 3.9499, "3,9 g"),    # through the centigram: 3.95, printed "4,0 g"
    ("fat", 0.5049, "0,5 g"),      # through the centigram: 0.50, called negligible
])
def test_a_value_is_rounded_once_only(name, value, written):
    """Table 4 rounds the computed value, not a value already rounded. Two
    rounds in a row move the figure by a decigram, and can turn a value above
    the negligibility threshold into a "< 0,5 g" — which is a claim, not a
    rounding."""
    assert declared(name, value) == written
    assert declared(name, round(value, 2)) != written  # what two rounds would give


def test_the_label_carries_the_nine_values():
    label = declared_label({**SHEET, "saturates": 2.0, "sugars": 1.0,
                            "salt": 0.01, "energy_kj": 876.3, "energy_kcal": 210.4})
    assert label["energy"] == "876 kJ / 210 kcal"
    assert set(label) == {"energy", "energy_kj", "energy_kcal", "fat", "saturates",
                          "carbs", "sugars", "fibre", "protein", "salt"}


def test_the_energy_comes_joined_and_apart():
    """A caller holding energy in two fields takes the two mentions as they
    are. Writing them again from a rounded value would round twice."""
    label = declared_label({**SHEET, "energy_kj": 876.3, "energy_kcal": 210.4})
    assert (label["energy_kj"], label["energy_kcal"]) == ("876 kJ", "210 kcal")
    assert label["energy"] == f'{label["energy_kj"]} / {label["energy_kcal"]}'


@pytest.mark.parametrize("name, value, expected", [
    ("fibre", 6.0, 2.0),        # under 10 g: ABSOLUTE, and far wider than 20 %
    ("salt", 0.02, 0.375),      # under 1,25 g: absolute
    ("protein", 20.0, 4.0),     # 10-40 g: 20 %
    ("fat", 50.0, 8.0),         # over 40 g: absolute again
])
def test_tolerance_is_not_twenty_percent_everywhere(name, value, expected):
    """The point of table 1: under the thresholds an ABSOLUTE margin applies,
    often much wider. A "30 % error" says nothing until you know on what."""
    assert tolerance(name, value) == pytest.approx(expected)
