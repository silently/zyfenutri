"""The calculation: one document in, one document out.

    from zyfenutri import compute
    result = compute({"harvested_g": 1750, "fermentation_hours": 36, "ingredients": [...]})

Input and output are plain dictionaries, which is also exactly what YAML and
JSON give you. The document is read into a `recipe.Recipe`, and the recipe's
sheet is written back out with what a label needs.

An unknown anywhere — an ingredient without composition or weight, a missing
setting, a gap in a transform — makes the affected values unknown in the
product. Never a zero, never a partial sum.

The shape of both documents is described in the README.
"""
from collections.abc import Callable

from zyfenutri import transforms as tf
from zyfenutri.checks import ADDITIVE, MASS_BALANCE_SUSPECT_G, mass_balance
from zyfenutri.label import declared_label, energy
from zyfenutri.nutrients import NUTRIENTS, SUBSET_OF, NutritionFacts
from zyfenutri.recipe import Ingredient, Recipe


def _step(make: Callable[[float], tf.Transform], value: object, unknown: str,
          missing: list[str], what: str) -> tf.Transform:
    """A transform from its setting; an `Unknown` one if the setting is absent or wrong."""
    if value is None:
        missing.append(f"no {what}")
        return tf.Unknown(unknown)
    try:
        return make(value)
    except (TypeError, ValueError):
        missing.append(f"invalid {what}: {value!r}")
        return tf.Unknown(unknown)


def _ingredient(raw: dict, document: dict, missing: list[str]) -> tuple[dict, Ingredient | None]:
    """One ingredient: its line on the sheet, and what enters the recipe."""
    name = raw.get("name") or "—"
    role = (raw.get("role") or "").strip().lower()
    line: dict = {"name": name, "role": role or None, "counted": True,
                  "transforms": [], "contributes_g": {}}

    if excluded := tf.EXCLUDED.get(role):
        line.update(counted=False, excluded_because=excluded)
        return line, None

    facts = NutritionFacts.from_mapping(raw.get("per_100g"))
    weight = raw.get("weight_g")
    if facts == NutritionFacts():
        missing.append(f"{name} — no composition given")
    else:
        line["incomplete_sheet"] = list(facts.unknown)
        missing.extend(f"{name} — sheet has no {n}" for n in facts.unknown)
    if not weight:
        missing.append(f"{name} — no weight given")
        facts = NutritionFacts()     # an ingredient of unknown mass: all unknown

    steps = tf.PIPELINE.get(role, ())
    transforms: list[tf.Transform] = []
    raw_mass = float(weight or 0.0)
    raw_weight = raw.get("raw_weight_g")
    # Dehulling only counts when it was WEIGHED: the hull mass is the gap
    # between gross and net, never an assumption.
    if ("dehulling" in steps and raw.get("dehulled") and weight
            and raw_weight is not None and raw_weight > weight):
        transforms.append(tf.Dehulling.from_weights(raw_weight, weight))
        raw_mass = float(raw_weight)
    if "roasting" in steps and (raw.get("roasted") or raw.get("roasting_intensity") is not None):
        transforms.append(_step(tf.Roasting, raw.get("roasting_intensity"),
                                "Torréfaction (intensité inconnue)", missing,
                                f"roasting intensity for {name} (roasting_intensity: 1 to 3)"))
    if "soaking" in steps:
        transforms.append(_step(tf.Soaking, document.get("soaking_hours"),
                                "Trempage (durée inconnue)", missing, "soaking time (soaking_hours)"))
    if "cooking" in steps:
        transforms.append(_step(tf.Cooking, document.get("cooking_minutes"),
                                "Cuisson (durée inconnue)", missing, "cooking time (cooking_minutes)"))
    if "fermentation" in steps:
        transforms.append(_step(tf.Fermentation, document.get("fermentation_hours"),
                                "Fermentation (durée inconnue)", missing,
                                "fermentation time (fermentation_hours)"))

    # Only substrates swell: every other ingredient keeps its mass.
    yield_factor = raw.get("yield") if role == "substrate" else 1.0
    ingredient = Ingredient(name=name, facts=facts, raw_mass=raw_mass,
                            transforms=tuple(transforms), yield_factor=yield_factor or 1.0)

    prepared = tf.process(facts, ingredient.transforms)
    line["transforms"] = [t.label for t in ingredient.transforms]
    line["contributes_g"] = {n: None if v is None else round(raw_mass * v / 100, 3)
                             for n, v in prepared.as_dict().items()}
    line["yield_known"] = role != "substrate" or bool(raw.get("yield"))
    return line, ingredient


def _plain(value: object) -> object:
    """Tuples as lists: YAML cannot write a tuple."""
    if isinstance(value, tuple | list):
        return [_plain(v) for v in value]
    if isinstance(value, dict):
        return {k: _plain(v) for k, v in value.items()}
    return value


def compute(document: dict) -> dict:
    """Nutritional composition per 100 g of finished tempeh.

    Never raises on missing data: it reports. `complete` says whether the
    result may be put on a label, and `missing` says what stands in the way.
    """
    missing: list[str] = []
    warnings: list[str] = []
    pairs = [_ingredient(raw, document, missing) for raw in document.get("ingredients") or []]
    lines = [line for line, _ in pairs]
    counted = tuple(i for _, i in pairs if i is not None)

    weighed = document.get("harvested_g")
    substrates = [line for line in lines if line["role"] == "substrate"]
    if weighed:
        product_mass, estimated = float(weighed), False
    elif substrates and all(line.get("yield_known", True) for line in lines):
        product_mass = round(sum(i.raw_mass * i.yield_factor for i in counted), 1)
        estimated = True
        missing.append("harvest weight predicted, not weighed — fine to design "
                       "a recipe, not to label a product")
    else:
        product_mass, estimated = None, False
        missing.append("no harvest weight, and no yield factor to predict one")
    for line in lines:
        line.pop("yield_known", None)

    recipe = Recipe(name=document.get("recipe") or "—", ingredients=counted,
                    product_mass=product_mass)
    facts = recipe.facts() if counted and product_mass else NutritionFacts()

    per_100g = {n: None if v is None else round(v, 2) for n, v in facts.as_dict().items()}
    # A "dont" above its total has no physical meaning: it can only come from rounding.
    for subset, total in SUBSET_OF.items():
        if per_100g[subset] is not None and per_100g[total] is not None:
            per_100g[subset] = min(per_100g[subset], per_100g[total])
    if counted and product_mass:
        missing.extend(f"{n} unknown in the product: an ingredient or a transform "
                       "does not know it yet" for n in NUTRIENTS if per_100g[n] is None)

    kj, kcal = energy(per_100g)
    per_100g_full = {**per_100g, "energy_kj": kj, "energy_kcal": kcal}

    balance = (mass_balance(per_100g)
               if all(per_100g[n] is not None for n in ADDITIVE) else None)
    if balance is not None and balance > MASS_BALANCE_SUSPECT_G:
        warnings.append(f"macronutrients add up to {balance:g} g per 100 g: "
                        "almost nothing left for water and ash")
    if document.get("coefficients"):
        warnings.append("coefficients are no longer read from the document: "
                        "they live in zyfenutri/transforms.py, each with its source")

    missing = list(dict.fromkeys(missing))
    return {
        "recipe": document.get("recipe"),
        "harvested_g": product_mass,
        "harvest_estimated": estimated,
        "complete": bool(counted) and bool(product_mass) and not missing,
        "per_100g": per_100g_full,
        "label": declared_label(per_100g_full),
        "dry_matter_g": balance,
        "ingredients": lines,
        "missing": missing,
        "warnings": warnings,
        "steps": _steps(recipe, product_mass, estimated, per_100g),
        "coefficients": _plain(tf.COEFFICIENTS),
    }


def _steps(recipe: Recipe, product_mass: float | None, estimated: bool,
           per_100g: dict[str, float | None]) -> list[str]:
    """The chain, spelled out. This is the sheet one shows when challenged."""
    n = len(recipe.ingredients)
    out = [f"Apport de chaque intrant : masse pesée × composition pour 100 g "
           f"({n} intrant{'s' if n > 1 else ''})", *recipe.steps()]
    if product_mass:
        out.append(f"Ramené à 100 g de produit fini : ÷ {product_mass:g} g "
                   f"{'PRÉDITS par le facteur de rendement' if estimated else 'récoltés'}. "
                   "C'est cette division qui porte l'eau reprise")
        out.append("Énergie calculée depuis les macros (annexe XIV), jamais recopiée")
    if any(v is None for v in per_100g.values()):
        out.append("Une valeur inconnue d'un intrant ou d'une transformation rend la valeur "
                   "du produit inconnue : elle n'est jamais remplacée par un zéro")
    return out
