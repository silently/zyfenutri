"""The data in `refs/analyses/` as a test set.

Two reasons to run tests through these files rather than numbers in the code:

1. **Whatever is entered becomes a check.** Adding a laboratory analysis
   extends coverage without touching code — and if the estimate falls outside
   the regulatory tolerances against a real measurement, the suite says so.
2. **The format is checked for real.** A misspelt key in a reference file
   would otherwise be silently ignored, and the analysis would count for
   nothing.

⚠️ These tests read `refs/` through `zyfenutri.refs_data`. When the directory
is absent everything is **skipped** rather than failed — the package must stay
testable without it.
"""
import pytest

from zyfenutri.nutrients import SUBSET_OF
from zyfenutri.refs_data import (
    fermentation_deviations,
    load_analyses,
    refs_dir,
)

pytestmark = pytest.mark.skipif(refs_dir() is None, reason="refs/ absent")


# --- The format holds --------------------------------------------------------

def test_every_reference_file_parses():
    """Loading alone already checks indentation and decimal points."""
    assert load_analyses() is not None


def test_no_unknown_field_in_any_reference_file():
    """A typo ("proteine_g" for "proteines_g") raises nothing: the value is
    just ignored, and the analysis counts for nothing."""
    for doc in load_analyses():
        assert not doc.unknown_fields, (
            f"{doc.path.name} : champ(s) inconnu(s) {doc.unknown_fields}. "
            "Vérifiez l'orthographe contre MODELE.yml."
        )


def test_compositions_stay_physically_possible():
    for analysis in load_analyses():
        for where, sample in (("matiere_premiere", analysis.matiere_premiere),
                              ("avant", analysis.avant), ("apres", analysis.apres)):
            for name, value in sample.composition.items():
                assert 0 <= value <= 100, f"{analysis.path.name}/{where}/{name} = {value}"
            for subset, total in SUBSET_OF.items():
                if subset in sample.composition and total in sample.composition:
                    assert sample.composition[subset] <= sample.composition[total] + 1e-9, (
                        f"{analysis.path.name}/{where} : {subset} dépasse {total}"
                    )
            if sample.masse_g is not None:
                assert sample.masse_g > 0, f"{analysis.path.name}/{where} : masse ≤ 0"


# --- The whole chain, on the worked example ----------------------------------

def test_the_worked_example_round_trips():
    """The example is built backwards: its "after" values come from the
    coefficients applied to its "before" values. The calculation must find
    them again — which checks at once the YAML reading, the French key
    mapping, the engine, and the division by the harvested mass."""
    examples = [a for a in load_analyses() if a.is_example and a.avant.usable]
    assert examples, "l'exemple pédagogique a disparu de refs/analyses/"

    for analysis in examples:
        deviations = fermentation_deviations(analysis)
        assert deviations, f"{analysis.path.name} : rien à comparer"
        for deviation in deviations:
            assert abs(deviation.delta) < 0.01, (
                f"{analysis.path.name}/{deviation.field} : prédit {deviation.predicted}, "
                f"fichier {deviation.measured}"
            )


# --- Real analyses, against the regulatory tolerances ------------------------

def test_real_analyses_fall_within_the_regulatory_tolerances():
    """The only threshold that means anything: would the estimate stand up to
    an inspection against this measurement? A "30% gap" says nothing until you
    know what quantity it is 30% of.

    Until a real analysis is entered this test is **skipped** — it switches
    itself on with the first filled-in file.
    """
    real = [a for a in load_analyses()
            if not a.is_example and a.avant.usable and a.apres.usable]
    if not real:
        pytest.skip("aucune analyse de laboratoire réelle dans refs/analyses/")

    outside = []
    for analysis in real:
        for deviation in fermentation_deviations(analysis):
            if not deviation.within:
                outside.append(
                    f"{analysis.reference}/{deviation.field} : prédit {deviation.predicted} g, "
                    f"mesuré {deviation.measured} g, écart {deviation.delta:+} g "
                    f"pour une tolérance de ± {deviation.tolerance} g"
                )
    assert not outside, (
        "L'estimation sort des tolérances réglementaires face à un dosage :\n  "
        + "\n  ".join(outside)
        + "\n→ les coefficients sont à caler (check.py)."
    )
