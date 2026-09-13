"""Le moteur en ligne de commande : du JSON entre, du JSON sort.

    echo '{"harvest_weight_g": 1750, "ingredients": [...]}' | python -m zyfenutri

C'est l'interface à utiliser quand importer le paquet n'est pas possible ou
pas souhaitable : **aucun serveur, aucun port, aucune requête HTTP** — un
processus, une entrée standard, une sortie standard. Le découplage est celui du
système d'exploitation, ce qui est à la fois le plus simple et le plus solide :
l'appelant n'a même pas à partager l'interpréteur Python.

Codes de sortie : **0** calcul abouti · **2** entrée invalide (le message part
sur stderr, et le JSON de sortie porte `error`).
"""
from __future__ import annotations

import argparse
import dataclasses
import json
import sys

from zyfenutri import __version__
from zyfenutri.annexe_xiv import declared_values
from zyfenutri.engine import estimate_batch_nutrition


def calculer(payload: dict) -> dict:
    """Le calcul, sur un dictionnaire déjà lu. Sans effet de bord."""
    resultat = estimate_batch_nutrition(
        harvest_weight_g=payload.get("harvest_weight_g"),
        ingredients=payload.get("ingredients") or [],
        coefficients=payload.get("coefficients"),
    )
    sortie = dataclasses.asdict(resultat)
    # Les neuf valeurs telles qu'elles s'écrivent sur l'étiquette : c'est
    # souvent tout ce que l'appelant veut, et les recalculer chez lui serait
    # dupliquer la règle d'arrondi.
    sortie["declared"] = declared_values({
        **resultat.per_100g,
        "energy_kj": resultat.energy_kj,
        "energy_kcal": resultat.energy_kcal,
    })
    sortie["version"] = __version__
    return sortie


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="zyfenutri",
        description="Composition nutritionnelle d'un lot de tempeh (JSON sur stdin).")
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument("--indent", type=int, default=None,
                        help="indentation du JSON de sortie (défaut : compact)")
    args = parser.parse_args(argv)

    brut = sys.stdin.read()
    try:
        payload = json.loads(brut)
    except json.JSONDecodeError as exc:
        print(f"entrée illisible : {exc}", file=sys.stderr)
        json.dump({"error": f"JSON invalide : {exc}"}, sys.stdout)
        return 2
    if not isinstance(payload, dict):
        print("l'entrée doit être un objet JSON", file=sys.stderr)
        json.dump({"error": "l'entrée doit être un objet JSON"}, sys.stdout)
        return 2

    try:
        sortie = calculer(payload)
    except (TypeError, ValueError, KeyError) as exc:
        print(f"entrée invalide : {exc}", file=sys.stderr)
        json.dump({"error": str(exc)}, sys.stdout)
        return 2

    json.dump(sortie, sys.stdout, ensure_ascii=False, indent=args.indent)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
