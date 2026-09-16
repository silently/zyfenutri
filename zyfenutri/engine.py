"""The calculation: one document in, one document out.

    from zyfenutri import compute
    result = compute({"harvested_g": 1750, "ingredients": [...]})

Input and output are plain dictionaries, which is also exactly what YAML and
JSON give you. There is no object model to learn and no state to carry.

The shape of both documents is described in the README.
"""
from __future__ import annotations

from zyfenutri import transforms
from zyfenutri.checks import MASS_BALANCE_SUSPECT_G, mass_balance
from zyfenutri.label import declared_label, energy
from zyfenutri.nutrients import NUTRIENTS, SUBSET_OF, read_per_100g

#: Roles we know. Anything else is counted pro rata with no transformation,
#: which is the conservative reading of "we were not told what this is".
KNOWN_ROLES = tuple(transforms.PIPELINE) + tuple(transforms.EXCLUDED)


def _ingredient(raw: dict, coefficients: dict[str, float]) -> dict:
    """One ingredient: from what was weighed to what it contributes."""
    name = raw.get("name") or "—"
    role = (raw.get("role") or "").strip().lower()
    line: dict = {"name": name, "role": role or None, "counted": True,
                  "transforms": [], "contributes_g": {}}

    excluded = transforms.EXCLUDED.get(role)
    if excluded:
        line.update(counted=False, excluded_because=excluded)
        return line

    weight = raw.get("weight_g")
    per_100g = read_per_100g(raw.get("per_100g"))
    if not per_100g:
        line.update(counted=False, excluded_because="no composition given")
        return line
    if not weight:
        line.update(counted=False, excluded_because="no weight given")
        return line

    steps = transforms.PIPELINE.get(role, ())
    raw_weight = raw.get("raw_weight_g")
    # Dehulling only counts when it was WEIGHED: the hull mass is the gap
    # between gross and net, never an assumption.
    dehulled = (bool(raw.get("dehulled")) and "dehulling" in steps
                and raw_weight is not None and raw_weight > weight)

    # When the grain is dehulled the sheet describes it AS BOUGHT, hulls
    # included, so we start from the gross weight.
    base = raw_weight if dehulled else weight
    masses = {n: base * per_100g[n] / 100.0 for n in NUTRIENTS if n in per_100g}

    if dehulled:
        masses, warning = transforms.dehull(
            masses, per_100g=per_100g, hull_g=raw_weight - weight, coefficients=coefficients)
        line["transforms"].append("dehulling")
        if warning:
            line["warning"] = warning
    if "soaking_and_cooking" in steps:
        masses = transforms.apply(masses, transforms.SOAKING_AND_COOKING, coefficients)
        line["transforms"].append("soaking_and_cooking")
    if "roasting" in steps and raw.get("roasted"):
        masses = transforms.apply(masses, transforms.ROASTING, coefficients)
        line["transforms"].append("roasting")
    if "fermentation" in steps:
        masses = transforms.apply(masses, transforms.FERMENTATION, coefficients)
        line["transforms"].append("fermentation")

    line["contributes_g"] = {n: round(m, 3) for n, m in masses.items()}
    line["incomplete_sheet"] = sorted(n for n in NUTRIENTS if n not in per_100g)
    return line


def _harvest(document: dict, ingredients: list[dict]) -> tuple[float | None, bool]:
    """The weight to divide by: measured, or predicted from the yield factor.

    Measured always wins. The yield factor exists so a recipe can be costed
    before anything has been made — it already absorbs sorting and dehulling
    losses (down) and hydration (up), which is why only substrates carry one.
    """
    weighed = document.get("harvested_g")
    if weighed:
        return float(weighed), False
    predicted = sum(
        (item.get("raw_weight_g") or item.get("weight_g") or 0.0) * (item.get("yield") or 0.0)
        for item in ingredients
        if (item.get("role") or "").strip().lower() == "substrate" and item.get("yield")
    )
    return (round(predicted, 1), True) if predicted > 0 else (None, False)


def compute(document: dict) -> dict:
    """Nutritional composition per 100 g of finished tempeh.

    Never raises on missing data: it reports. `complete` says whether the
    result may be put on a label, and `missing` says what stands in the way.
    """
    coefficients = {**transforms.DEFAULTS, **(document.get("coefficients") or {})}
    raw_ingredients = document.get("ingredients") or []

    lines = [_ingredient(item, coefficients) for item in raw_ingredients]
    counted = [line for line in lines if line["counted"]]
    harvested_g, estimated = _harvest(document, raw_ingredients)

    totals: dict[str, float] = {}
    for line in counted:
        for name, mass in line["contributes_g"].items():
            totals[name] = totals.get(name, 0.0) + mass

    missing: list[str] = []
    warnings: list[str] = [f"{l['name']}: {l['warning']}" for l in lines if l.get("warning")]
    for line in lines:
        if not line["counted"] and line.get("excluded_because", "").startswith("no "):
            missing.append(f"{line['name']} — {line['excluded_because']}")
        for name in line.get("incomplete_sheet") or []:
            missing.append(f"{line['name']} — sheet has no {name}")

    per_100g: dict[str, float | None] = {n: None for n in NUTRIENTS}
    if harvested_g and counted:
        for name in NUTRIENTS:
            if name in totals:
                per_100g[name] = round(totals[name] / harvested_g * 100.0, 2)
        # A "dont" above its total has no physical meaning: it can only come
        # from rounding or from an inconsistent sheet.
        for subset, total in SUBSET_OF.items():
            if per_100g[subset] is not None and per_100g[total] is not None:
                per_100g[subset] = min(per_100g[subset], per_100g[total])
    elif not harvested_g:
        missing.append("no harvest weight, and no yield factor to predict one")
    if estimated:
        missing.append("harvest weight predicted, not weighed — fine to design "
                       "a recipe, not to label a product")

    kj, kcal = energy(per_100g)
    per_100g_full = {**per_100g, "energy_kj": kj, "energy_kcal": kcal}

    balance = mass_balance(per_100g)
    if balance is not None and balance > MASS_BALANCE_SUSPECT_G:
        warnings.append(f"macronutrients add up to {balance:g} g per 100 g: "
                        "almost nothing left for water and ash")

    return {
        "recipe": document.get("recipe"),
        "harvested_g": harvested_g,
        "harvest_estimated": estimated,
        "complete": bool(counted) and bool(harvested_g) and not missing,
        "per_100g": per_100g_full,
        "label": declared_label(per_100g_full),
        "dry_matter_g": balance,
        "ingredients": lines,
        "missing": missing,
        "warnings": warnings,
        "steps": _steps(counted, coefficients, harvested_g, estimated),
        "coefficients": coefficients,
    }


def _steps(counted: list[dict], coefficients: dict[str, float],
           harvested_g: float | None, estimated: bool) -> list[str]:
    """The chain, spelled out. This is the sheet one shows when challenged."""
    c = coefficients
    out = [f"Apport de chaque intrant : masse pesée × composition pour 100 g "
           f"({len(counted)} intrant{'s' if len(counted) > 1 else ''})"]
    if any("dehulling" in l["transforms"] for l in counted):
        out.append(f"T1 · Dépelliculage : on part du poids brut, puis on retire la "
                   f"pellicule, comptée à {c['hull_fibre']:g} % de fibres")
    if any("soaking_and_cooking" in l["transforms"] for l in counted):
        out.append(f"T2a · Trempage et cuisson (substrats) : −{c['leaching_carbs']:g} % de "
                   f"glucides, −{c['leaching_protein']:g} % de protéines, "
                   f"−{c['leaching_minerals']:g} % de sel partis à l'eau, qui est jetée")
    if any("roasting" in l["transforms"] for l in counted):
        out.append(f"T3 · Torréfaction : −{c['roasting_sugars']:g} % de sucres (Maillard). "
                   "Le reste ne bouge pas — une torréfaction chasse de l'eau")
    if any("fermentation" in l["transforms"] for l in counted):
        out.append(f"T2b · Fermentation : −{c['fermentation_carbs']:g} % de glucides et "
                   f"−{c['fermentation_fat']:g} % de lipides consommés par le mycélium ; "
                   "les protéines sont hydrolysées, pas brûlées")
    if any(not l["transforms"] for l in counted):
        out.append("Acidifiant pré-inoculation : ajouté après cuisson, compté au prorata")
    if harvested_g:
        out.append(f"T5 · Ramené à 100 g : ÷ {harvested_g:g} g "
                   f"{'PRÉDITS par le facteur de rendement' if estimated else 'récoltés'}. "
                   "C'est cette division qui porte l'eau reprise")
        out.append("Énergie calculée depuis les macros (annexe XIV), jamais recopiée")
    return out
