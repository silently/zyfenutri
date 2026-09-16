"""The calculation: what it does, and what it refuses to do."""
import pytest

from zyfenutri import compute

SOY = {"fat": 20.0, "saturates": 3.0, "carbs": 30.0, "sugars": 7.0,
       "fibre": 20.0, "protein": 36.0, "salt": 0.02}
RICE = {"fat": 1.0, "saturates": 0.3, "carbs": 80.0, "sugars": 0.5,
        "fibre": 2.0, "protein": 6.0, "salt": 0.0}


def one_substrate(**document):
    return compute({
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
    for name in ("protein", "fat", "carbs", "fibre"):
        assert wet["per_100g"][name] == pytest.approx(dry["per_100g"][name] / 2, rel=1e-3)


def test_water_is_never_counted_twice():
    """The trap: a hydration factor ON TOP of the division would count water
    twice. So absolute masses must not depend on the harvest weight."""
    a = one_substrate(harvested_g=1500)
    b = one_substrate(harvested_g=3000)
    assert a["ingredients"][0]["contributes_g"] == b["ingredients"][0]["contributes_g"]


# --- Who goes through what ----------------------------------------------------

def test_a_substrate_soaks_cooks_and_ferments():
    line = one_substrate(harvested_g=2000)["ingredients"][0]
    assert line["transforms"] == ["soaking_and_cooking", "fermentation"]


def test_a_support_ferments_but_never_soaks():
    """It goes in after draining: it does not soak, but it is in the block
    throughout incubation."""
    result = compute({"harvested_g": 1000, "ingredients": [
        {"name": "Farine de riz", "role": "support", "weight_g": 100, "per_100g": RICE}]})
    assert result["ingredients"][0]["transforms"] == ["fermentation"]
    # Protein goes through fermentation intact: 100 g x 6 % = 6 g.
    assert result["per_100g"]["protein"] == pytest.approx(0.6, abs=0.01)


def test_roasting_only_bites_on_sugars():
    """Roasting drives off water, and water is not a nutrient. Only Maillard
    bites, and only on sugars."""
    kinako = {"fat": 25.0, "saturates": 3.6, "carbs": 14.0, "sugars": 10.0,
              "fibre": 18.0, "protein": 37.0, "salt": 0.01}
    plain = compute({"harvested_g": 1000, "ingredients": [
        {"name": "Kinako", "role": "support", "weight_g": 100, "per_100g": kinako}]})
    roasted = compute({"harvested_g": 1000, "ingredients": [
        {"name": "Kinako", "role": "support", "weight_g": 100,
         "roasted": True, "per_100g": kinako}]})
    assert roasted["per_100g"]["sugars"] < plain["per_100g"]["sugars"]
    for name in ("protein", "fat", "fibre", "carbs"):
        assert roasted["per_100g"][name] == plain["per_100g"][name], name
    assert "roasting" in roasted["ingredients"][0]["transforms"]


def test_the_pre_inoculation_acid_goes_through_untouched():
    """Added after cooking: its only rule is its share of the mass."""
    result = compute({"harvested_g": 1000, "ingredients": [
        {"name": "Vinaigre", "role": "acid", "weight_g": 100,
         "per_100g": {"fat": 0.0, "saturates": 0.0, "carbs": 1.0, "sugars": 0.4,
                      "fibre": 0.0, "protein": 0.0, "salt": 0.01}}]})
    assert result["per_100g"]["carbs"] == 0.1        # 100 g x 1 %, no loss
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

def test_dehulling_shifts_the_balance_towards_protein():
    """Hulls are almost pure fibre, so what is left is richer in protein."""
    plain = one_substrate(harvested_g=2000)
    hulled = compute({"harvested_g": 2000, "ingredients": [
        {"name": "Soja", "role": "substrate", "weight_g": 1000,
         "raw_weight_g": 1100, "dehulled": True, "per_100g": SOY}]})
    assert hulled["per_100g"]["protein"] > plain["per_100g"]["protein"]
    assert hulled["per_100g"]["fibre"] < plain["per_100g"]["fibre"]
    assert "dehulling" in hulled["ingredients"][0]["transforms"]


def test_dehulling_needs_both_weights():
    """The hull mass is the gap between gross and net — never an assumption."""
    result = compute({"harvested_g": 2000, "ingredients": [
        {"name": "Soja", "role": "substrate", "weight_g": 1000,
         "dehulled": True, "per_100g": SOY}]})
    assert "dehulling" not in result["ingredients"][0]["transforms"]


def test_removing_more_fibre_than_the_sheet_declares_is_reported():
    """If the bound bites, sheet and weights contradict each other. Say so,
    rather than return a zero that would read like a measurement."""
    result = compute({"harvested_g": 2000, "ingredients": [
        {"name": "Soja", "role": "substrate", "weight_g": 1000, "raw_weight_g": 1500,
         "dehulled": True, "per_100g": {**SOY, "fibre": 2.0}}]})
    assert any("fibre" in w for w in result["warnings"])


# --- The harvest weight -------------------------------------------------------

def test_a_recipe_can_be_costed_before_anything_is_weighed():
    """No weighing: the harvest is predicted from the yield factor. This is
    what lets a recipe be costed before it has ever been made."""
    result = compute({"ingredients": [
        {"name": "Soja", "role": "substrate", "weight_g": 1000,
         "yield": 1.75, "per_100g": SOY}]})
    assert result["harvested_g"] == 1750
    assert result["harvest_estimated"] is True
    assert result["per_100g"]["protein"] is not None
    # But it is NOT complete: one does not label with an estimated denominator.
    assert result["complete"] is False
    assert any("not to label" in m for m in result["missing"])


def test_a_weighed_harvest_always_beats_a_predicted_one():
    result = compute({"harvested_g": 2000, "ingredients": [
        {"name": "Soja", "role": "substrate", "weight_g": 1000,
         "yield": 1.75, "per_100g": SOY}]})
    assert result["harvested_g"] == 2000
    assert result["harvest_estimated"] is False


def test_only_substrates_carry_a_yield_factor():
    """A support does not make the product swell: its mass simply adds."""
    result = compute({"ingredients": [
        {"name": "Kinako", "role": "support", "weight_g": 30,
         "yield": 1.75, "per_100g": RICE}]})
    assert result["harvested_g"] is None


# --- Honesty ------------------------------------------------------------------

def test_an_incomplete_sheet_is_reported_not_guessed():
    result = compute({"harvested_g": 2000, "ingredients": [
        {"name": "Soja", "role": "substrate", "weight_g": 1000,
         "per_100g": {"protein": 36.0}}]})
    assert result["complete"] is False
    assert any("no fat" in m for m in result["missing"])
    # What is known is still computed — it is a floor, not a label.
    assert result["per_100g"]["protein"] is not None
    assert result["per_100g"]["fat"] is None


def test_energy_is_missing_when_a_macro_is():
    """An energy short of one nutrient is worse than no energy at all."""
    result = compute({"harvested_g": 2000, "ingredients": [
        {"name": "Soja", "role": "substrate", "weight_g": 1000,
         "per_100g": {"protein": 36.0}}]})
    assert result["per_100g"]["energy_kj"] is None
    assert result["label"]["energy"] is None


def test_the_steps_are_returned_so_the_result_can_be_argued_with():
    result = one_substrate(harvested_g=2000)
    joined = " ".join(result["steps"])
    assert "Trempage" in joined and "Fermentation" in joined
    assert "÷ 2000 g récoltés" in joined
