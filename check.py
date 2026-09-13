#!/usr/bin/env python3
"""Confronte les analyses de laboratoire au calcul nutritionnel de l'application.

    python check.py

Il ne modifie rien : les écarts se reportent à la main, si on les juge fondés.

Lit `refs/` via `zyfenutri.refs_data` — le **même** module que
`tests/test_refs.py`, pour que la lecture qu'on regarde et celle qui
échoue ne puissent pas diverger.

Trois choses, dans cet ordre :

1. **Prédit vs mesuré**, nutriment par nutriment, avec la **tolérance
   réglementaire** en regard — le seul seuil qui dise si l'estimation serait
   opposable au contrôle ;
2. ce que la fermentation a **réellement** consommé, en masses absolues, face
   aux coefficients en vigueur ;
3. les références Ciqual et les recettes qui n'en ont pas.

⚠️ **Ne modifie rien.** C'est une lecture ; c'est l'utilisateur qui décide de
reporter une valeur dans les coefficients. La colonne « n » dit sur combien
d'analyses repose chaque moyenne : une seule mesure ne fait pas une consigne.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

from zyfenutri.engine import DEFAULT_COEFFICIENTS  # noqa: E402
from zyfenutri.annexe_xiv import NUTRIENT_FIELDS, tolerance_for  # noqa: E402
from zyfenutri.refs_data import (  # noqa: E402
    fermentation_deviations,
    load_analyses,
    refs_dir,
)

#: Quel coefficient chaque nutriment vérifie, à la fermentation.
FERMENTATION_COEFFICIENT = {
    "carbohydrates_g": "nutrition_fermentation_carbs_pct",
    "sugars_g": "nutrition_fermentation_carbs_pct",
    "fat_g": "nutrition_fermentation_fat_pct",
    "saturates_g": "nutrition_fermentation_fat_pct",
    "protein_g": None,   # attendu : 0 %, les protéines sont hydrolysées
    "fibre_g": None,     # attendu : 0 % — cf. « ce qui reste à améliorer »
    "salt_g": None,      # un minéral ne se consomme pas
}


def _titre(texte: str) -> None:
    print("\n" + "═" * 78)
    print(f" {texte}")
    print("═" * 78)


def main() -> int:
    racine = refs_dir()
    if racine is None:
        print("refs/ introuvable. Lancez ce script depuis le dépôt.")
        return 1

    analyses = load_analyses()

    _titre("Prédit par l'application vs mesuré au laboratoire")
    if not analyses:
        print("\n  Aucune analyse dans refs/analyses/.")
        print("  Copiez MODELE.yml et remplissez-le — même partiellement.")

    cumul: dict[str, list[float]] = {}
    for analysis in analyses:
        marque = "  (exemple — exclu des moyennes)" if analysis.is_example else ""
        print(f"\n▸ {analysis.reference}{marque}")

        if not (analysis.avant.usable and analysis.apres.usable):
            manque = [nom for nom, ech in (("avant", analysis.avant), ("après", analysis.apres))
                      if not ech.usable]
            print(f"    pas exploitable — il manque la masse ou la composition : {', '.join(manque)}")
            continue

        print(f"    {analysis.avant.masse_g:g} g avant → {analysis.apres.masse_g:g} g après "
              f"({(analysis.apres.masse_g / analysis.avant.masse_g - 1) * 100:+.1f} % de masse)")
        print(f"    {'nutriment':22} {'prédit':>8} {'mesuré':>8} {'écart':>8} "
              f"{'tolérance':>10}")

        for ecart in fermentation_deviations(analysis):
            verdict = "" if ecart.within else "   ⚠️ HORS TOLÉRANCE"
            print(f"    {ecart.field:22} {ecart.predicted:8.2f} {ecart.measured:8.2f} "
                  f"{ecart.delta:+8.2f} {ecart.tolerance:10.3f}{verdict}")

        # Ce que la fermentation a réellement consommé, en masses absolues.
        for champ in NUTRIENT_FIELDS:
            avant = analysis.avant.composition.get(champ)
            apres = analysis.apres.composition.get(champ)
            if avant is None or apres is None or avant <= 0:
                continue
            masse_avant = analysis.avant.masse_g * avant / 100
            masse_apres = analysis.apres.masse_g * apres / 100
            if masse_avant <= 0:
                continue
            perte = (1 - masse_apres / masse_avant) * 100
            if not analysis.is_example:
                cumul.setdefault(champ, []).append(perte)

    if cumul:
        _titre("Ce que la fermentation a réellement consommé (analyses réelles)")
        print(f"\n  {'nutriment':22} {'n':>3} {'mesuré':>9} {'en vigueur':>12}")
        for champ, valeurs in cumul.items():
            cle = FERMENTATION_COEFFICIENT.get(champ)
            attendu = DEFAULT_COEFFICIENTS.get(cle) if cle else 0.0
            moyenne = sum(valeurs) / len(valeurs)
            print(f"  {champ:22} {len(valeurs):3d} {moyenne:+8.1f} % {attendu:+11.1f} %")
        print("\n  ⚠️  Rien n'est appliqué automatiquement. Si vous jugez l'écart fondé,")
        print("      reportez la valeur dans les coefficients.")

    # Un exemple de lecture des tolérances, pour situer les ordres de grandeur.
    _titre("Tolérances réglementaires, pour situer")
    print("\n  Sur un tempeh de légumineuses typique :")
    for champ, valeur in (("protein_g", 18.0), ("carbohydrates_g", 12.0),
                          ("fibre_g", 6.0), ("fat_g", 5.0), ("salt_g", 0.02)):
        t = tolerance_for(champ, valeur)
        print(f"    {champ:22} {valeur:5.2f} g  →  ± {t:6.3f} g  ({t / valeur * 100:.0f} %)")
    print("\n  Seules les protéines tombent dans la bande ± 20 % — et c'est le")
    print("  nutriment qu'un contrôle dosera en premier sur un produit vendu")
    print("  pour sa richesse en protéines.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
