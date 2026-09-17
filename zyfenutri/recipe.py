"""A recipe: ingredients, each with its own transforms, mixed into a product.

    Recipe(name="Tempeh de soja", ingredients=(
        Ingredient(name="Soja", facts=soy, raw_mass=1000, yield_factor=1.75,
                   transforms=(Dehulling(0.09), Soaking(12), Cooking(30), Fermentation(36))),
        Ingredient(name="Vinaigre", facts=vinegar, raw_mass=50),
    )).facts()

Nothing new happens here: each ingredient goes through `transforms.process`,
the results go through `mixing.mix`. This module only names the pieces.
"""
from dataclasses import dataclass

from zyfenutri.mixing import Portion, mix
from zyfenutri.nutrients import NutritionFacts
from zyfenutri.transforms import Transform, process


@dataclass(frozen=True, slots=True, kw_only=True)
class Ingredient:
    """One ingredient as weighed, and what it goes through.

    `facts` is its sheet per 100 g AS WEIGHED, before any transform;
    `yield_factor` its mass in the product over that raw mass (see `Portion`).
    """
    name: str
    facts: NutritionFacts
    raw_mass: float
    transforms: tuple[Transform, ...] = ()
    yield_factor: float = 1.0

    def portion(self) -> Portion:
        return Portion(process(self.facts, self.transforms), self.raw_mass, self.yield_factor)


@dataclass(frozen=True, slots=True, kw_only=True)
class Recipe:
    """Ingredients mixed into one product. `product_mass`: if it was weighed."""
    name: str
    ingredients: tuple[Ingredient, ...]
    product_mass: float | None = None

    def facts(self) -> NutritionFacts:
        """The product's sheet, per 100 g of product."""
        return mix((i.portion() for i in self.ingredients), product_mass=self.product_mass)

    def steps(self) -> list[str]:
        """What each ingredient went through, in French, for the calculation sheet."""
        return [f"{i.name} : {' → '.join(t.label for t in i.transforms) or 'tel quel'}"
                for i in self.ingredients]
