"""The calculation: what it does, and what it refuses to do."""
import pytest

from zyfenutri import compute

SOY = {"fat": 20.0, "saturates": 3.0, "carbs": 30.0, "sugars": 7.0,
       "fibre": 20.0, "protein": 36.0, "salt": 0.02}
RICE = {"fat": 1.0, "saturates": 0.3, "carbs": 80.0, "sugars": 0.5,
        "fibre": 2.0, "protein": 6.0, "salt": 0.0}
PROCESS = {"cooking_minutes": 30, "fermentation_hours": 36}


def one_substrate(**document):
    return compute({
        **PROCESS,
        "ingredients": [{"name": "Soja", "role": "substrate",
                         "weight_g": 1000, "per_100g": SOY}],
        **document,
    })


# --- The heart: water is carried by the final division, once -----------------

def test_water_uptake_halves_the_values():
    """A batch that doubled in weight by taking up water has all its values
    halved. The final division does that on its own."""
    dry = one_substrate(harvested_g=1000)
    wet = one_substrate(harvested_g=2000)
    assert wet["per_100g"]["fat"] == pytest.approx(dry["per_100g"]["fat"] / 2, rel=1e-3)


def test_water_is_never_counted_twice():
    """The trap: a hydration factor ON TOP of the division would count water
    twice. So absolute masses must not depend on the harvest weight."""
    a = one_substrate(harvested_g=1500)
    b = one_substrate(harvested_g=3000)
    assert a["ingredients"][0]["contributes_g"] == b["ingredients"][0]["contributes_g"]


# --- Who goes through what ----------------------------------------------------

def test_a_substrate_soaks_cooks_and_ferments():
    line = one_substrate(harvested_g=2000)["ingredients"][0]
    assert line["transforms"] == ["Trempage (une nuit)", "Cuisson 30 min", "Fermentation 36 h"]


def test_a_support_ferments_but_never_soaks():
    """It goes in after draining: it does not soak, but it is in the block
    throughout incubation."""
    result = compute({"harvested_g": 1000, **PROCESS, "ingredients": [
        {"name": "Farine de riz", "role": "support", "weight_g": 100, "per_100g": RICE}]})
    assert result["ingredients"][0]["transforms"] == ["Fermentation 36 h"]
    # 100 g × 1 % fat, 11 % of it lost to fermentation, over 1000 g.
    assert result["per_100g"]["fat"] == pytest.approx(0.089, abs=0.01)


def test_a_roasted_support_is_roasted_then_fermented():
    result = compute({"harvested_g": 1000, **PROCESS, "ingredients": [
        {"name": "Kinako", "role": "support", "weight_g": 100,
         "roasted": True, "per_100g": RICE}]})
    assert result["ingredients"][0]["transforms"] == ["Torréfaction", "Fermentation 36 h"]
    assert result["per_100g"]["energy_kj"] is not None


def test_a_roasting_intensity_is_no_longer_read():
    result = compute({"harvested_g": 1000, **PROCESS, "ingredients": [
        {"name": "Kinako", "role": "support", "weight_g": 100,
         "roasted": True, "roasting_intensity": 2, "per_100g": RICE}]})
    assert any("roasting_intensity" in w for w in result["warnings"])


def test_the_pre_inoculation_acid_goes_through_untouched():
    """Added after cooking: its only rule is its share of the mass."""
    result = compute({"harvested_g": 1000, "ingredients": [
        {"name": "Vinaigre", "role": "acid", "weight_g": 100,
         "per_100g": {"fat": 0.0, "saturates": 0.0, "carbs": 1.0, "sugars": 0.4,
                      "fibre": 0.0, "protein": 0.0, "salt": 0.01}}]})
    assert result["per_100g"]["carbs"] == 0.1        # 100 g × 1 %, no loss
    assert result["ingredients"][0]["transforms"] == []


@pytest.mark.parametrize("role, reason", [
    ("starter", "few grams"),
    ("soaking_acid", "thrown away"),
])
def test_what_is_left_out_says_why(role, reason):
    """Both exclusions slightly UNDER-declare, which is the safe direction."""
    result = compute({"harvested_g": 1000, "ingredients": [
        {"name": "X", "role": role, "weight_g": 10, "per_100g": RICE}]})
    line = result["ingredients"][0]
    assert line["counted"] is False
    assert reason in line["excluded_because"]


# --- Dehulling ----------------------------------------------------------------

def test_a_dehulled_substrate_goes_through_dehulling():
    result = compute({"harvested_g": 2000, **PROCESS, "ingredients": [
        {"name": "Soja", "role": "substrate", "weight_g": 1000,
         "dehulled": True, "per_100g": SOY}]})
    assert result["ingredients"][0]["transforms"][0] == "Dépelliculage"


def test_hulls_weigh_nothing_here():
    """Their mass is in the yield factor: the weight before dehulling is the
    raw mass, and the prediction multiplies it by the yield."""
    result = compute({**PROCESS, "ingredients": [
        {"name": "Soja", "role": "substrate", "weight_g": 1000, "yield": 1.75,
         "dehulled": True, "per_100g": SOY}]})
    assert result["harvested_g"] == 1750


def test_a_raw_weight_is_no_longer_read():
    result = one_substrate(harvested_g=2000, ingredients=[
        {"name": "Soja", "role": "substrate", "weight_g": 1000, "raw_weight_g": 1100,
         "dehulled": True, "per_100g": SOY}])
    assert any("raw_weight_g" in w for w in result["warnings"])


# --- The harvest weight -------------------------------------------------------

def test_a_recipe_can_be_costed_before_anything_is_weighed():
    """No weighing: the harvest is predicted from the yield factor."""
    result = compute({**PROCESS, "ingredients": [
        {"name": "Soja", "role": "substrate", "weight_g": 1000,
         "yield": 1.75, "per_100g": SOY}]})
    assert result["harvested_g"] == 1750
    assert result["harvest_estimated"] is True
    assert result["per_100g"]["fat"] is not None
    # But it is NOT complete: one does not label with an estimated denominator.
    assert result["complete"] is False
    assert any("not to label" in m for m in result["missing"])


def test_a_weighed_harvest_always_beats_a_predicted_one():
    result = one_substrate(harvested_g=2000)
    assert result["harvested_g"] == 2000
    assert result["harvest_estimated"] is False


def test_only_substrates_carry_a_yield_factor():
    """A support does not make the product swell: its mass simply adds."""
    result = compute({"ingredients": [
        {"name": "Kinako", "role": "support", "weight_g": 30,
         "yield": 1.75, "per_100g": RICE}]})
    assert result["harvested_g"] is None


# --- Unknowns cascade ---------------------------------------------------------

def test_a_missing_setting_makes_everything_unknown():
    """No cooking time: the cooking cannot be computed, so nothing after it."""
    result = compute({"harvested_g": 2000, "fermentation_hours": 36,
                      "ingredients": [{"name": "Soja", "role": "substrate",
                                       "weight_g": 1000, "per_100g": SOY}]})
    assert all(v is None for v in result["per_100g"].values())
    assert any("cooking_minutes" in m for m in result["missing"])
    assert result["complete"] is False


def test_an_ingredient_without_composition_makes_the_product_unknown():
    """Not a partial sum over the others: an unknown ingredient, an unknown product."""
    result = compute({"harvested_g": 1000, "ingredients": [
        {"name": "Vinaigre", "role": "acid", "weight_g": 100, "per_100g": SOY},
        {"name": "Mystère", "role": "acid", "weight_g": 10}]})
    assert all(v is None for v in result["per_100g"].values())
    assert any("no composition" in m for m in result["missing"])


def test_an_ingredient_without_weight_makes_the_product_unknown():
    result = compute({"harvested_g": 1000, "ingredients": [
        {"name": "Vinaigre", "role": "acid", "weight_g": 100, "per_100g": SOY},
        {"name": "Sel", "role": "acid", "per_100g": SOY}]})
    assert all(v is None for v in result["per_100g"].values())


def test_a_nutrient_missing_from_one_sheet_is_unknown_in_the_product():
    result = compute({"harvested_g": 1000, "ingredients": [
        {"name": "Vinaigre", "role": "acid", "weight_g": 100, "per_100g": SOY},
        {"name": "Farine", "role": "acid", "weight_g": 100, "per_100g": {"fat": 1.0}}]})
    assert result["per_100g"]["protein"] is None
    assert result["per_100g"]["fat"] is not None
    assert any("sheet has no protein" in m for m in result["missing"])


def test_energy_is_missing_when_a_macro_is():
    """An energy short of one nutrient is worse than no energy at all."""
    result = one_substrate(harvested_g=2000, fermentation_hours=60)
    assert result["per_100g"]["carbs"] is None
    assert result["per_100g"]["energy_kj"] is None
    assert result["label"]["energy"] is None


def test_an_invalid_setting_is_reported_not_raised():
    result = one_substrate(harvested_g=2000, cooking_minutes=-3)
    assert any("invalid cooking time" in m for m in result["missing"])


def test_a_soaking_time_is_no_longer_read():
    """Soaking is always one night, 10 to 15 h."""
    result = one_substrate(harvested_g=2000, soaking_hours=30)
    assert any("one night" in w for w in result["warnings"])


# --- What comes out -----------------------------------------------------------

def test_the_steps_are_returned_so_the_result_can_be_argued_with():
    joined = " ".join(one_substrate(harvested_g=2000)["steps"])
    assert "Trempage (une nuit)" in joined and "Fermentation 36 h" in joined
    assert "÷ 2000 g récoltés" in joined


def test_coefficients_are_shown_and_no_longer_read():
    result = one_substrate(harvested_g=2000, coefficients={"leaching_carbs": 45})
    assert result["coefficients"]["soaking_sugars_kept"] == 0.73
    assert any("no longer read" in w for w in result["warnings"])


def test_a_fully_described_soy_tempeh_can_be_labelled():
    result = one_substrate(harvested_g=2000)
    assert result["complete"] is True
    assert result["label"]["energy"] is not None


def test_a_gap_is_spelled_out_in_the_steps():
    result = one_substrate(harvested_g=2000, fermentation_hours=60)
    assert "jamais remplacée par un zéro" in " ".join(result["steps"])
