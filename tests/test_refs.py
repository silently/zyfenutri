"""Les données de `refs/` comme jeu d'essai.

Deux raisons de faire passer les tests par ces fichiers plutôt que par des
nombres écrits dans le code :

1. **Ce qu'on y saisit devient une vérification.** Ajouter une analyse de
   laboratoire étend la couverture sans toucher au code — et si l'estimation
   sort des tolérances réglementaires face à un dosage réel, la suite le dit.
2. **Le format est vérifié pour de bon.** Une clé mal orthographiée dans un
   fichier de référence serait sinon ignorée en silence, et l'analyse
   compterait pour rien.

⚠️ Ces tests lisent `refs/` via `zyfenutri.refs_data`. Absent, tout se **skip**
plutôt que d'échouer — le dépôt doit rester testable sans lui.
"""
import pytest

from zyfenutri.annexe_xiv import NUTRIENT_FIELDS, tolerance_for
from zyfenutri.refs_data import (
    fermentation_deviations,
    load_analyses,
    refs_dir,
)

pytestmark = pytest.mark.skipif(refs_dir() is None, reason="refs/ absent")


# --- Le format tient ---------------------------------------------------------

def test_every_reference_file_parses():
    """Le simple fait de charger vérifie déjà l'indentation et les décimales."""
    assert load_analyses() is not None


def test_no_unknown_field_in_any_reference_file():
    """Une faute de frappe (« proteine_g » pour « proteines_g ») ne lève rien :
    la valeur est juste ignorée, et l'analyse compte pour rien."""
    for doc in load_analyses():
        assert not doc.unknown_fields, (
            f"{doc.path.name} : champ(s) inconnu(s) {doc.unknown_fields}. "
            "Vérifiez l'orthographe contre MODELE.yml."
        )


def test_compositions_stay_physically_possible():
    for analysis in load_analyses():
        for nom, echantillon in (("matiere_premiere", analysis.matiere_premiere),
                                 ("avant", analysis.avant), ("apres", analysis.apres)):
            for champ, valeur in echantillon.composition.items():
                assert 0 <= valeur <= 100, f"{analysis.path.name}/{nom}/{champ} = {valeur}"
            for sous, total in (("saturates_g", "fat_g"), ("sugars_g", "carbohydrates_g")):
                if sous in echantillon.composition and total in echantillon.composition:
                    assert echantillon.composition[sous] <= echantillon.composition[total] + 1e-9, (
                        f"{analysis.path.name}/{nom} : {sous} dépasse {total}"
                    )
            if echantillon.masse_g is not None:
                assert echantillon.masse_g > 0, f"{analysis.path.name}/{nom} : masse ≤ 0"


# --- La chaîne complète, sur l'exemple ---------------------------------------

def test_the_worked_example_round_trips():
    """L'exemple est construit à l'envers : ses valeurs « après » sortent des
    coefficients appliqués aux valeurs « avant ». L'application doit donc les
    retrouver — ce qui vérifie d'un coup la lecture du YAML, la correspondance
    des noms français, le moteur, et la division par la masse récoltée."""
    exemples = [a for a in load_analyses() if a.is_example and a.avant.usable]
    assert exemples, "l'exemple pédagogique a disparu de refs/analyses/"

    for analysis in exemples:
        ecarts = fermentation_deviations(analysis)
        assert ecarts, f"{analysis.path.name} : rien à comparer"
        for ecart in ecarts:
            assert abs(ecart.delta) < 0.01, (
                f"{analysis.path.name}/{ecart.field} : prédit {ecart.predicted}, "
                f"fichier {ecart.measured}"
            )


# --- Les analyses réelles, face aux tolérances réglementaires ----------------

def test_real_analyses_fall_within_the_regulatory_tolerances():
    """Le seul seuil qui ait un sens : l'estimation serait-elle opposable au
    contrôle face à ce dosage ? Un « écart de 30 % » ne dit rien tant qu'on ne
    sait pas sur quelle quantité il porte.

    Tant qu'aucune analyse réelle n'est saisie, ce test se **skip** — il
    s'activera de lui-même au premier fichier rempli.
    """
    reelles = [a for a in load_analyses()
               if not a.is_example and a.avant.usable and a.apres.usable]
    if not reelles:
        pytest.skip("aucune analyse de laboratoire réelle dans refs/analyses/")

    hors_tolerance = []
    for analysis in reelles:
        for ecart in fermentation_deviations(analysis):
            if not ecart.within:
                hors_tolerance.append(
                    f"{analysis.reference}/{ecart.field} : prédit {ecart.predicted} g, "
                    f"mesuré {ecart.measured} g, écart {ecart.delta:+} g "
                    f"pour une tolérance de ± {ecart.tolerance} g"
                )
    assert not hors_tolerance, (
        "L'estimation sort des tolérances réglementaires face à un dosage :\n  "
        + "\n  ".join(hors_tolerance)
        + "\n→ les coefficients sont à caler (check.py)."
    )


# --- La table des tolérances elle-même ---------------------------------------

def test_the_tolerance_table_matches_the_commission_guide():
    """⚠️ Ce n'est PAS « ± 20 % » partout — l'idée reçue la plus répandue sur le
    sujet. Tableau 1 du guide de décembre 2012, vérifié le 2026-09-12."""
    # Glucides, sucres, protéines, fibres : < 10 g → ± 2 g
    for champ in ("carbohydrates_g", "sugars_g", "protein_g", "fibre_g"):
        assert tolerance_for(champ, 6) == 2.0
        assert tolerance_for(champ, 18) == pytest.approx(3.6)      # 10–40 g → ± 20 %
        assert tolerance_for(champ, 45) == 8.0                     # > 40 g → ± 8 g
    # Matières grasses : < 10 g → ± 1,5 g
    assert tolerance_for("fat_g", 5) == 1.5
    assert tolerance_for("fat_g", 20) == pytest.approx(4.0)
    # Acides gras saturés : < 4 g → ± 0,8 g
    assert tolerance_for("saturates_g", 1.7) == 0.8
    assert tolerance_for("saturates_g", 6) == pytest.approx(1.2)
    # Sel : < 1,25 g → ± 0,375 g — énorme au regard d'un tempeh
    assert tolerance_for("salt_g", 0.02) == 0.375
    assert tolerance_for("salt_g", 2.0) == pytest.approx(0.4)


def test_every_declared_nutrient_has_a_tolerance():
    for champ in NUTRIENT_FIELDS:
        assert tolerance_for(champ, 10) > 0, champ
