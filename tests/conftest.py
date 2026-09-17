"""Sheets shared by the transform and recipe tests. Orders of magnitude, not data."""
import pytest

from zyfenutri import NutritionFacts


@pytest.fixture
def soy() -> NutritionFacts:
    return NutritionFacts(fat=20.0, saturates=2.9, carbs=15.0, sugars=5.7,
                          fibre=15.0, protein=40.0, salt=0.01)


@pytest.fixture
def lentil() -> NutritionFacts:
    return NutritionFacts(fat=1.5, saturates=0.2, carbs=48.0, sugars=2.0,
                          fibre=11.0, protein=24.0, salt=0.02)


@pytest.fixture
def vinegar() -> NutritionFacts:
    return NutritionFacts(fat=0.0, saturates=0.0, carbs=0.93, sugars=0.4,
                          fibre=0.0, protein=0.0, salt=0.013)
