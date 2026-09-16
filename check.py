#!/usr/bin/env python3
"""Hold laboratory analyses up against the calculation.

    python check.py

Reads `refs/analyses/` through `zyfenutri.refs_data` — the SAME module as
`tests/test_refs.py`, so the reading one looks at and the one that fails
cannot drift apart.

Three things, in this order:

1. **predicted vs measured**, nutrient by nutrient, next to the **regulatory
   tolerance** — the only threshold that says whether the estimate would
   stand up to an inspection;
2. what fermentation **actually** consumed, in absolute masses, against the
   default coefficients;
3. the tolerances on a typical tempeh, to give a sense of scale.

⚠️ **Changes nothing.** It is a reading: deciding to carry a value over to
`coefficients:` is the user's call. The "n" column says how many analyses each
average rests on — a single measurement is not a setting.
"""
from __future__ import annotations

from zyfenutri.label import tolerance
from zyfenutri.nutrients import NUTRIENTS
from zyfenutri.refs_data import fermentation_deviations, load_analyses, refs_dir
from zyfenutri.transforms import DEFAULTS

#: Which coefficient each nutrient checks, at fermentation.
FERMENTATION_COEFFICIENT = {
    "carbs": "fermentation_carbs",
    "sugars": "fermentation_carbs",
    "fat": "fermentation_fat",
    "saturates": "fermentation_fat",
    "protein": None,   # expected 0%: protein is hydrolysed, not consumed
    "fibre": None,     # expected 0%: not calibrated, for lack of data
    "salt": None,      # a mineral is not consumed
}


def _title(text: str) -> None:
    print("\n" + "═" * 78)
    print(f" {text}")
    print("═" * 78)


def main() -> int:
    if refs_dir() is None:
        print("refs/ introuvable. Lancez ce script depuis le dépôt, "
              "ou indiquez le dossier dans ZYFENUTRI_REFS.")
        return 1

    analyses = load_analyses()

    _title("Prédit par le calcul vs mesuré au laboratoire")
    if not analyses:
        print("\n  Aucune analyse dans refs/analyses/.")
        print("  Copiez MODELE.yml et remplissez-le — même partiellement.")

    losses: dict[str, list[float]] = {}
    for analysis in analyses:
        mark = "  (exemple — exclu des moyennes)" if analysis.is_example else ""
        print(f"\n▸ {analysis.reference}{mark}")

        if not (analysis.avant.usable and analysis.apres.usable):
            lacking = [name for name, sample in (("avant", analysis.avant),
                                                 ("après", analysis.apres))
                       if not sample.usable]
            print(f"    pas exploitable — il manque la masse ou la composition : "
                  f"{', '.join(lacking)}")
            continue

        print(f"    {analysis.avant.masse_g:g} g avant → {analysis.apres.masse_g:g} g après "
              f"({(analysis.apres.masse_g / analysis.avant.masse_g - 1) * 100:+.1f} % de masse)")
        print(f"    {'nutriment':22} {'prédit':>8} {'mesuré':>8} {'écart':>8} "
              f"{'tolérance':>10}")

        for deviation in fermentation_deviations(analysis):
            verdict = "" if deviation.within else "   ⚠️ HORS TOLÉRANCE"
            print(f"    {deviation.field:22} {deviation.predicted:8.2f} "
                  f"{deviation.measured:8.2f} {deviation.delta:+8.2f} "
                  f"{deviation.tolerance:10.3f}{verdict}")

        # What fermentation actually consumed, in absolute masses.
        for name in NUTRIENTS:
            before = analysis.avant.composition.get(name)
            after = analysis.apres.composition.get(name)
            if before is None or after is None or before <= 0:
                continue
            mass_before = analysis.avant.masse_g * before / 100
            mass_after = analysis.apres.masse_g * after / 100
            if not analysis.is_example:
                losses.setdefault(name, []).append((1 - mass_after / mass_before) * 100)

    if losses:
        _title("Ce que la fermentation a réellement consommé (analyses réelles)")
        print(f"\n  {'nutriment':22} {'n':>3} {'mesuré':>9} {'par défaut':>12}")
        for name, values in losses.items():
            key = FERMENTATION_COEFFICIENT.get(name)
            expected = DEFAULTS.get(key) if key else 0.0
            mean = sum(values) / len(values)
            print(f"  {name:22} {len(values):3d} {mean:+8.1f} % {expected:+11.1f} %")
        print("\n  ⚠️  Rien n'est appliqué automatiquement. Si vous jugez l'écart fondé,")
        print("      passez la valeur dans le bloc `coefficients:` du document.")

    _title("Tolérances réglementaires, pour situer")
    print("\n  Sur un tempeh de légumineuses typique :")
    for name, value in (("protein", 18.0), ("carbs", 12.0), ("fibre", 6.0),
                        ("fat", 5.0), ("salt", 0.02)):
        margin = tolerance(name, value)
        print(f"    {name:22} {value:5.2f} g  →  ± {margin:6.3f} g  "
              f"({margin / value * 100:.0f} %)")
    print("\n  Entre 10 et 40 g, la bande est de ± 20 % : c'est la plus serrée, et")
    print("  c'est celle des protéines — le nutriment qu'un contrôle dosera en")
    print("  premier. En dessous, la tolérance absolue est bien plus large.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
