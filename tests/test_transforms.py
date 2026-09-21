"""Transforms: a sheet in, a sheet out, on the same basis."""
import ast
import pathlib

import pytest

from zyfenutri import NutritionFacts, Retention, Transform, process

SOY = NutritionFacts(fat=20.0, saturates=2.9, carbs=15.0, sugars=5.7,
                     fibre=15.0, protein=40.0, salt=0.01)


def test_retention_multiplies_each_nutrient_by_its_own_factor():
    leaching = Retention("Trempage", {"carbs": 0.5, "salt": 0.65})
    out = leaching(SOY)
    assert out.carbs == pytest.approx(7.5)
    assert out.salt == pytest.approx(0.0065)
    assert out.protein == SOY.protein and out.fibre == SOY.fibre


def test_a_dont_line_follows_its_total():
    """Saturates are part of fat: losing fat loses saturates in proportion."""
    out = Retention("Fermentation", {"fat": 0.95})(SOY)
    assert out.saturates == pytest.approx(2.9 * 0.95)


def test_a_dont_line_can_have_its_own_factor():
    out = Retention("Torréfaction", {"sugars": 0.85})(SOY)
    assert out.sugars == pytest.approx(5.7 * 0.85)
    assert out.carbs == SOY.carbs


def test_an_unknown_value_stays_unknown():
    out = Retention("Trempage", {"carbs": 0.5})(NutritionFacts(fat=20.0))
    assert out.carbs is None


def test_a_setting_is_bound_by_a_factory():
    """A step that depends on a duration is built from it, then called like
    any other."""
    def soaking(hours: float) -> Transform:
        return Retention(f"Trempage {hours:g} h", {"carbs": max(0.0, 1 - 0.04 * hours)})

    step = soaking(12)
    assert isinstance(step, Transform)
    assert step.label == "Trempage 12 h"
    assert step(SOY).carbs == pytest.approx(15.0 * 0.52)


def test_transforms_run_in_order():
    out = process(SOY, [Retention("a", {"carbs": 0.5}), Retention("b", {"carbs": 0.4})])
    assert out.carbs == pytest.approx(15.0 * 0.5 * 0.4)


@pytest.mark.parametrize("factors", [{"water": 0.5}, {"carbs": -0.1}])
def test_nonsense_factors_are_refused(factors):
    with pytest.raises(ValueError):
        Retention("x", factors)


# --- Nothing rounds before the label -------------------------------------------

#: The chain from a sheet to a product: transforms, then the mix. Rounding is a
#: way of writing a number, so it belongs to `label.py` and nowhere else.
_EXACT_MODULES = ("transforms.py", "mixing.py", "recipe.py", "nutrients.py")


@pytest.mark.parametrize("module", _EXACT_MODULES)
def test_the_chain_never_rounds(module):
    """Five transforms run one after the other, then a division. A round in any
    of them would be an error the next step carries, and the chain would grow
    it. The value stays exact until `declared` writes it down."""
    source = (pathlib.Path(__file__).parents[1] / "zyfenutri" / module).read_text()
    called = {node.func.id for node in ast.walk(ast.parse(source))
              if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)}
    assert not called & {"round", "int", "floor", "ceil"}, (
        f"{module} rounds: rounding is how a value is written, not how it is computed")


def test_a_long_chain_keeps_every_digit():
    """The same, seen from the outside: after five retentions the value still
    carries digits far below anything a label ever prints."""
    steps = tuple(Retention(f"Étape {i}", {"protein": 0.9}) for i in range(5))
    out = process(NutritionFacts(protein=40.0), steps)
    assert out.protein == 40.0 * 0.9 ** 5          # exact, not merely close
    assert out.protein != pytest.approx(round(out.protein, 2), abs=1e-12)
