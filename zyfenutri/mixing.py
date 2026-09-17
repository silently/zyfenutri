"""Mixing: several prepared ingredients become one product, per 100 g.

This is where the mass of product enters, and the only place it does. Every
sheet reaching here still counts nutrients per 100 g of RAW ingredient; each
portion's yield factor turns its raw mass into product mass, and the single
division by the total happens here. Applying a yield anywhere else would
count water twice.
"""
from collections.abc import Iterable
from dataclasses import dataclass

from zyfenutri.nutrients import NUTRIENTS, NutritionFacts


@dataclass(frozen=True, slots=True)
class Portion:
    """One ingredient as it enters the mix.

    - `facts`: its sheet after its own transforms, still per 100 g of raw
      ingredient (see `transforms.Transform`);
    - `raw_mass`: how much raw ingredient went in. Grams, or any proportion
      as long as every portion uses the same unit;
    - `yield_factor`: its mass in the finished product / its raw mass before
      any transform. ONE factor for the whole chain, never split per step:
      hull losses if dehulled (down), water taken up while soaking and
      cooking (up), a little water lost while fermenting (down). 1.0 for an
      ingredient added as is, such as vinegar.

    The factor carries mass only. What the hulls took with them in nutrients
    belongs to the dehulling transform — mass and composition are counted
    apart, so nothing is counted twice.

    [1, p. 80]: soybeans 1 → 2.33 soaked → 2.02 dehulled → 1.90 cooked
    → 1.74 tempeh (Steinkraus et al. 1961, cited there).
    """
    facts: NutritionFacts
    raw_mass: float
    yield_factor: float = 1.0

    def __post_init__(self) -> None:
        if self.raw_mass < 0:
            raise ValueError("a raw mass cannot be negative")
        if self.yield_factor <= 0:
            raise ValueError("a yield factor must be positive")


def mix(portions: Iterable[Portion], *, product_mass: float | None = None) -> NutritionFacts:
    """The product's sheet, per 100 g of product.

    Product mass is predicted as the sum of `raw_mass × yield_factor`. Pass
    `product_mass` when it was weighed: a weighing beats a prediction. It must
    then be in the same unit as the raw masses.

    A nutrient unknown for any portion is unknown for the mix: summing the
    others would treat the gap as a zero.
    """
    portions = list(portions)
    mass = product_mass if product_mass is not None else sum(
        p.raw_mass * p.yield_factor for p in portions)
    if not mass or mass <= 0:
        raise ValueError("nothing to mix: the product mass is zero")

    values: dict[str, float | None] = {}
    for name in NUTRIENTS:
        per_portion = [getattr(p.facts, name) for p in portions]
        if any(value is None for value in per_portion):
            values[name] = None
            continue
        nutrient_mass = sum(p.raw_mass * value / 100.0
                            for p, value in zip(portions, per_portion))
        values[name] = nutrient_mass / mass * 100.0
    return NutritionFacts(**values)
