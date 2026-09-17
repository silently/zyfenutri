"""A recipe runs end to end, even while most transforms are gaps."""
import pytest

from zyfenutri import (Cooking, Dehulling, Fermentation, Ingredient, NutritionFacts, Recipe,
                       Roasting, Soaking, energy_of)


@pytest.fixture
def tempeh(soy, vinegar):
    kinako = NutritionFacts(fat=25.0, saturates=3.6, carbs=14.0, sugars=10.0,
                            fibre=18.0, protein=37.0, salt=0.01)
    return Recipe(name="Tempeh de soja", ingredients=(
        Ingredient(name="Soja", facts=soy, raw_mass=1000, yield_factor=1.75,
                   transforms=(Dehulling(0.09), Soaking(), Cooking(30), Fermentation(36))),
        Ingredient(name="Kinako", facts=kinako, raw_mass=10,
                   transforms=(Roasting(2), Fermentation(36))),
        Ingredient(name="Vinaigre", facts=vinegar, raw_mass=50),
    ))


def test_a_full_recipe_runs(tempeh):
    assert isinstance(tempeh.facts(), NutritionFacts)


def test_what_is_known_comes_through(soy):
    """Fat is known through dehulling, soaking and cooking."""
    recipe = Recipe(name="Soja cuit", ingredients=(
        Ingredient(name="Soja", facts=soy, raw_mass=1000, yield_factor=2.0,
                   transforms=(Dehulling(0.09), Soaking(), Cooking(30))),))
    assert recipe.facts().fat is not None


def test_for_now_roasting_leaves_carbs_and_fibre_unknown(tempeh):
    """Roasting is the last transform with gaps. This test is meant to start
    failing once it is sourced."""
    known = {k for k, v in tempeh.facts().as_dict().items() if v is not None}
    assert known == {"fat", "saturates", "protein", "salt"}


def test_a_gap_anywhere_leaves_the_nutrient_unknown(tempeh):
    """Carbs are a gap at roasting (the kinako): the product's carbs, and so
    its energy, are unknown, not a guess."""
    assert tempeh.facts().carbs is None
    assert energy_of(tempeh.facts()) is None


def test_an_ingredient_added_as_is_keeps_its_sheet(vinegar):
    recipe = Recipe(name="Vinaigre", ingredients=(
        Ingredient(name="Vinaigre", facts=vinegar, raw_mass=50),))
    assert recipe.facts().salt == pytest.approx(vinegar.salt)


def test_a_weighed_product_mass_is_used(soy):
    recipe = Recipe(name="Soja", product_mass=2000, ingredients=(
        Ingredient(name="Soja", facts=soy, raw_mass=1000, yield_factor=1.75),))
    assert recipe.facts().protein == pytest.approx(40.0 * 1000 / 2000)


def test_steps_describe_the_chain(tempeh):
    assert tempeh.steps()[0] == ("Soja : Dépelliculage (9 % de pellicule) → Trempage (une nuit)"
                                 " → Cuisson 30 min → Fermentation 36 h")
    assert tempeh.steps()[2] == "Vinaigre : tel quel"


@pytest.mark.skip(reason="coquille : à écrire quand les transformations seront calées")
def test_soy_tempeh_stays_within_codex_bounds():
    """[10, p. 1719]: protein ≥ 15 %, fat ≥ 7 %, crude fibre ≤ 2.5 %."""
