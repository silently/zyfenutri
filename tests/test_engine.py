"""Estimation nutritionnelle d'un lot — la chaîne, et ce qu'elle refuse de faire."""
import pytest

from zyfenutri.engine import (
    DEFAULT_COEFFICIENTS,
    calibrate_fermentation,
    estimate_batch_nutrition,
)

SOJA = dict(fat_g=20.0, saturates_g=3.0, carbohydrates_g=30.0, sugars_g=7.0,
            fibre_g=20.0, protein_g=36.0, salt_g=0.02)
RIZ = dict(fat_g=1.0, saturates_g=0.3, carbohydrates_g=80.0, sugars_g=0.5,
           fibre_g=2.0, protein_g=6.0, salt_g=0.0)


def _ing(name, category, net, composition=None, gross=None, dehulled=False, spec="SPEC"):
    return dict(input_type_name=name, category=category, net_weight_g=net,
                gross_weight_g=gross, dehulled=dehulled, spec_identifier=spec,
                composition=composition)


def _soja_seul(**kwargs):
    return estimate_batch_nutrition(
        ingredients=[_ing("Soja", "substrate", 1000, SOJA)], **kwargs
    )


# --- Le cœur : l'eau est portée par la division finale ------------------------

def test_water_uptake_halves_the_values():
    """« Si le poids a fait ×2 grâce à l'eau, toutes les valeurs sont divisées
    par 2 » — c'est la division par le poids récolté qui le fait, à elle seule."""
    sec = _soja_seul(harvest_weight_g=1000)
    double = _soja_seul(harvest_weight_g=2000)

    for champ in ("protein_g", "fat_g", "carbohydrates_g", "fibre_g"):
        assert double.per_100g[champ] == pytest.approx(sec.per_100g[champ] / 2, rel=1e-3)


def test_water_is_never_counted_twice():
    """⚠️ Le piège : ajouter une correction d'hydratation EN PLUS de la division
    compterait l'eau deux fois. Les masses absolues ne dépendent donc pas du
    poids récolté — seul le ramené à 100 g en dépend."""
    a = _soja_seul(harvest_weight_g=1500)
    b = _soja_seul(harvest_weight_g=3000)
    masse_a = a.ingredients[0].nutrients["protein_g"]
    masse_b = b.ingredients[0].nutrients["protein_g"]
    assert masse_a == masse_b


# --- Pertes sélectives -------------------------------------------------------

def test_leaching_hits_carbs_and_salt_not_fat():
    """L'eau de trempage emporte des sucres solubles et des minéraux ; les
    lipides, insolubles, restent."""
    r = _soja_seul(harvest_weight_g=1000)
    n = r.ingredients[0].nutrients

    # Lipides : seule la fermentation les entame.
    attendu_lipides = 1000 * 20.0 / 100 * (1 - DEFAULT_COEFFICIENTS["nutrition_fermentation_fat_pct"] / 100)
    assert n["fat_g"] == pytest.approx(attendu_lipides, rel=1e-6)

    # Glucides : lessivage PUIS fermentation.
    attendu_glucides = (1000 * 30.0 / 100
                        * (1 - DEFAULT_COEFFICIENTS["nutrition_leaching_carbs_pct"] / 100)
                        * (1 - DEFAULT_COEFFICIENTS["nutrition_fermentation_carbs_pct"] / 100))
    assert n["carbohydrates_g"] == pytest.approx(attendu_glucides, rel=1e-6)

    # Sel : lessivé, jamais consommé — un minéral ne se brûle pas.
    attendu_sel = 1000 * 0.02 / 100 * (1 - DEFAULT_COEFFICIENTS["nutrition_leaching_minerals_pct"] / 100)
    assert n["salt_g"] == pytest.approx(attendu_sel, rel=1e-6)


def test_protein_survives_fermentation():
    """Les protéines sont hydrolysées, pas brûlées : leur masse se conserve,
    au lessivage près."""
    r = _soja_seul(harvest_weight_g=1000)
    attendu = 1000 * 36.0 / 100 * (1 - DEFAULT_COEFFICIENTS["nutrition_leaching_protein_pct"] / 100)
    assert r.ingredients[0].nutrients["protein_g"] == pytest.approx(attendu, rel=1e-6)


def test_dehulling_takes_fibre_preferentially():
    """Les pellicules sont presque uniquement des fibres : en retirer 8 % de la
    masse ne retire PAS 8 % des protéines."""
    sans = estimate_batch_nutrition(
        harvest_weight_g=1800,
        ingredients=[_ing("Soja", "substrate", 1000, SOJA)],
    )
    avec = estimate_batch_nutrition(
        harvest_weight_g=1800,
        ingredients=[_ing("Soja", "substrate", 1000, SOJA, gross=1085, dehulled=True)],
    )

    # Le dépelliculage part d'un poids BRUT plus élevé : protéines et lipides
    # y gagnent, puisque presque rien ne s'en va avec les pellicules.
    assert avec.per_100g["protein_g"] > sans.per_100g["protein_g"]
    # Les fibres, elles, sont nettement entamées.
    assert avec.per_100g["fibre_g"] < sans.per_100g["fibre_g"]


def test_an_impossible_hull_loss_is_capped_and_reported():
    """Retirer plus de fibres que le grain n'en contient est impossible : on
    borne ET on le dit, plutôt que de rendre un zéro qui passerait pour une
    mesure."""
    pauvre = {**SOJA, "fibre_g": 2.0}
    r = estimate_batch_nutrition(
        harvest_weight_g=1800,
        ingredients=[_ing("Soja", "substrate", 1000, pauvre, gross=1200, dehulled=True)],
    )
    assert r.per_100g["fibre_g"] >= 0
    assert any("fibres" in w for w in r.warnings)


# --- Qui compte, qui ne compte pas -------------------------------------------

def test_soaking_acid_is_excluded():
    """L'eau de trempage est jetée : ce qu'on y a versé ne finit pas dans le
    produit."""
    vinaigre = dict(fat_g=0.0, saturates_g=0.0, carbohydrates_g=1.0, sugars_g=0.4,
                    fibre_g=0.0, protein_g=0.0, salt_g=0.01)
    r = estimate_batch_nutrition(
        harvest_weight_g=1800,
        ingredients=[_ing("Soja", "substrate", 1000, SOJA),
                     _ing("Vinaigre blanc", "soaking_acid", 20, vinaigre)],
    )
    exclu = [i for i in r.ingredients if not i.counted]
    assert len(exclu) == 1
    assert "eau de trempage" in exclu[0].excluded_reason
    assert r.complete is True          # l'exclusion est voulue, pas un manque


def test_support_and_preinoculation_acid_are_counted_without_leaching():
    """Ajoutés APRÈS la cuisson : ils ne trempent pas, donc ne sont pas lessivés."""
    r = estimate_batch_nutrition(
        harvest_weight_g=1800,
        ingredients=[_ing("Farine de riz", "inoculation_support", 100, RIZ)],
    )
    attendu = (100 * 80.0 / 100
               * (1 - DEFAULT_COEFFICIENTS["nutrition_fermentation_carbs_pct"] / 100))
    assert r.ingredients[0].nutrients["carbohydrates_g"] == pytest.approx(attendu, rel=1e-6)


# --- Honnêteté ---------------------------------------------------------------

def test_a_missing_sheet_makes_it_incomplete():
    """Sans fiche produit, l'estimation est un MINORANT : l'annoncer comme une
    valeur d'étiquette sous-déclarerait."""
    r = estimate_batch_nutrition(
        harvest_weight_g=1800,
        ingredients=[_ing("Soja", "substrate", 1000, SOJA),
                     _ing("Orge", "substrate", 500, None)],
    )
    assert r.complete is False
    assert any("fiche produit" in m for m in r.missing)


def test_no_harvest_weight_no_values():
    """Sans poids récolté il n'y a rien à ramener à 100 g."""
    r = _soja_seul(harvest_weight_g=None)
    assert r.complete is False
    assert all(v is None for v in r.per_100g.values())
    assert r.energy_kj is None
    assert any("récolte" in m for m in r.missing)


def test_energy_is_computed_from_the_result():
    r = _soja_seul(harvest_weight_g=1800)
    p = r.per_100g
    assert r.energy_kj == pytest.approx(
        37 * p["fat_g"] + 17 * p["carbohydrates_g"] + 17 * p["protein_g"] + 8 * p["fibre_g"],
        rel=1e-3,
    )


def test_a_subset_never_exceeds_its_total():
    """« dont sucres » au-dessus des glucides n'a aucun sens physique."""
    bizarre = {**SOJA, "sugars_g": 30.0, "saturates_g": 20.0}
    r = estimate_batch_nutrition(
        harvest_weight_g=1800, ingredients=[_ing("Soja", "substrate", 1000, bizarre)],
    )
    assert r.per_100g["sugars_g"] <= r.per_100g["carbohydrates_g"]
    assert r.per_100g["saturates_g"] <= r.per_100g["fat_g"]


def test_the_chain_is_always_spelled_out():
    """C'est la fiche de calcul : sans elle, l'estimation n'est pas recevable."""
    r = _soja_seul(harvest_weight_g=1800)
    joint = " ".join(r.steps)
    for attendu in ("composition pour 100 g", "Trempage et cuisson", "Fermentation",
                    "100 g de produit fini", "annexe XIV"):
        assert attendu in joint, attendu


# --- Calage de l'activité de fermentation ------------------------------------

def test_calibration_reads_the_gap_against_a_reference():
    """On estime un lot de soja, on compare aux tables, et on lit le
    coefficient qui annulerait l'écart. Une lecture, pas une consigne."""
    # Estimé 15 g de glucides avec un coefficient de 15 %, référence 9 g.
    pct = calibrate_fermentation(estimated_carbs_g=15.0, reference_carbs_g=9.0, current_pct=15.0)
    assert pct > 15.0            # il faut consommer davantage pour tomber à 9

    # Le coefficient trouvé reproduit bien la référence.
    avant = 15.0 / (1 - 0.15)
    assert avant * (1 - pct / 100) == pytest.approx(9.0, rel=1e-2)


def test_calibration_refuses_nonsense():
    with pytest.raises(ValueError):
        calibrate_fermentation(estimated_carbs_g=0, reference_carbs_g=9, current_pct=15)
    with pytest.raises(ValueError):
        calibrate_fermentation(estimated_carbs_g=15, reference_carbs_g=9, current_pct=100)


# --- Le calage : le modèle doit retrouver un couple publié --------------------

#: **USDA 174270** « Soybeans, mature seeds, raw », pour 100 g.
#: ⚠️ Les glucides USDA sont « by difference », **fibres comprises** : les
#: glucides assimilables valent 30,16 − 9,3 = 20,86.
USDA_SOJA_174270 = dict(fat_g=19.94, saturates_g=2.884, carbohydrates_g=20.86,
                        sugars_g=7.33, fibre_g=9.3, protein_g=36.49, salt_g=0.005)

#: **USDA 174272** « Tempeh », pour 100 g. L'USDA ne publie ni fibres ni sucres
#: sur ce produit : `carbohydrates_g` y est donc le total, fibres comprises.
USDA_TEMPEH_174272 = dict(fat_g=10.8, protein_g=20.29, carbohydrates_total_g=7.64)

#: Un rendement de référence. C'est lui qui relie les deux fiches — et il
#: se valide au passage : les protéines seules imposent
#: `rendement = 1,798 × rétention protéique`, soit 1,744 avec nos 3 %.
RENDEMENT_MESURE = 1.75


def test_the_model_reproduces_the_usda_pair():
    """La graine 174270, passée par le modèle, doit redonner le tempeh 174272.

    C'est la seule vérification qui confronte la « tempehisation » à une
    observation extérieure. Elle tient parce que les deux fiches viennent de la
    **même table** : mêmes conventions d'analyse des deux côtés, ce qui manquait
    aux comparaisons précédentes.

    ⚠️ On compare les **glucides totaux** (assimilables + fibres) : l'USDA ne
    publie pas les fibres du tempeh, on ne peut donc pas départager les deux.
    """
    recolte = 1000 * RENDEMENT_MESURE
    estimation = estimate_batch_nutrition(
        ingredients=[_ing("Soja", "substrate", 1000, USDA_SOJA_174270)],
        harvest_weight_g=recolte,
    )
    obtenu = estimation.per_100g

    assert obtenu["protein_g"] == pytest.approx(USDA_TEMPEH_174272["protein_g"], abs=0.1)
    assert obtenu["fat_g"] == pytest.approx(USDA_TEMPEH_174272["fat_g"], abs=0.1)
    glucides_totaux = obtenu["carbohydrates_g"] + obtenu["fibre_g"]
    assert glucides_totaux == pytest.approx(
        USDA_TEMPEH_174272["carbohydrates_total_g"], abs=0.1)


def test_the_dry_matter_loss_matches_what_the_pair_shows():
    """⚠️ Le contrôle qui avait révélé le problème : le modèle ne perdait que
    7,5 % de la matière sèche entrante, quand le couple USDA en perd 22,8 %.

    C'est ce chiffre-là qu'il faut regarder en premier après tout recalage — un
    nutriment peut tomber juste pendant que le bilan d'ensemble est faux.
    """
    entrant = sum(USDA_SOJA_174270[c] for c in
                  ("fat_g", "carbohydrates_g", "fibre_g", "protein_g", "salt_g"))
    estimation = estimate_batch_nutrition(
        ingredients=[_ing("Soja", "substrate", 1000, USDA_SOJA_174270)],
        harvest_weight_g=1000 * RENDEMENT_MESURE,
    )
    sortant = sum(estimation.per_100g[c] for c in
                  ("fat_g", "carbohydrates_g", "fibre_g", "protein_g", "salt_g")) * RENDEMENT_MESURE

    perte = 1 - sortant / entrant
    # Le couple USDA perd 22,8 % (cendres comprises, qu'on ne modélise pas).
    assert 0.17 < perte < 0.25, f"perte de matière sèche : {perte:.1%}"


def test_only_the_product_of_the_two_carb_coefficients_is_pinned():
    """⚠️ Le partage lessivage / fermentation n'est PAS observable.

    Seul leur produit l'est (19,5 % mesuré). Ce test épingle donc le produit et
    **pas** les deux nombres séparément : les redistribuer sans changer le
    produit doit rester possible sans rien casser.
    """
    reste = ((1 - DEFAULT_COEFFICIENTS["nutrition_leaching_carbs_pct"] / 100)
             * (1 - DEFAULT_COEFFICIENTS["nutrition_fermentation_carbs_pct"] / 100))
    assert reste == pytest.approx(0.195, abs=0.02)


# --- T5 · la dilution, pesée ou prédite ---------------------------------------

def test_a_recipe_can_be_costed_before_anything_is_weighed():
    """LA GRANDE IDÉE : sortir une fiche depuis une recette, sans avoir produit.

    Sans pesée, le poids de tempeh se PRÉDIT en multipliant le poids brut de
    chaque substrat par son facteur de rendement. C'est ce qui permettra de
    dire ce que donnerait un tempeh de pois cassés avant d'en avoir fait un.
    """
    estimation = estimate_batch_nutrition(
        harvest_weight_g=None,
        ingredients=[{**_ing("Soja", "substrate", 1000, SOJA), "yield_factor": 1.75}],
    )
    assert estimation.harvest_weight_g == 1750
    assert estimation.harvest_weight_estimated is True
    assert estimation.per_100g["protein_g"] is not None
    # ⚠️ Mais elle n'est PAS complète : on n'étiquette pas avec un dénominateur
    # lui-même estimé.
    assert estimation.complete is False
    assert any("pas pour étiqueter" in m for m in estimation.missing)


def test_a_weighed_harvest_always_beats_a_predicted_one():
    """Une mesure prime sur une prédiction — le facteur ne sert qu'à défaut."""
    estimation = estimate_batch_nutrition(
        harvest_weight_g=2000,
        ingredients=[{**_ing("Soja", "substrate", 1000, SOJA), "yield_factor": 1.75}],
    )
    assert estimation.harvest_weight_g == 2000
    assert estimation.harvest_weight_estimated is False


def test_only_substrates_carry_a_yield_factor():
    """Un support ne fait pas gonfler le produit : sa masse s'y ajoute, c'est tout."""
    estimation = estimate_batch_nutrition(
        harvest_weight_g=None,
        ingredients=[{**_ing("Kinako", "inoculation_support", 30, RIZ), "yield_factor": 1.75}],
    )
    assert estimation.harvest_weight_g is None


# --- Qui subit quoi -----------------------------------------------------------

def test_the_starter_is_left_out_of_the_calculation():
    """Sa part dans la masse finale est négligeable — l'exclure sous-déclare
    légèrement, ce qui est le sens prudent."""
    estimation = estimate_batch_nutrition(
        harvest_weight_g=2000,
        ingredients=[_ing("Soja", "substrate", 1000, SOJA),
                     _ing("Rhizopus", "starter", 5, RIZ)],
    )
    starter = next(c for c in estimation.ingredients if c.input_type_name == "Rhizopus")
    assert starter.counted is False
    assert "négligeable" in starter.excluded_reason


def test_the_pre_inoculation_acid_goes_through_untouched():
    """Ajouté après la cuisson, il ne trempe pas, ne cuit pas, et sa part est
    trop faible pour que la fermentation s'y voie : sa seule règle est sa
    proportion."""
    estimation = estimate_batch_nutrition(
        harvest_weight_g=1000,
        ingredients=[{**_ing("Vinaigre", "inoculation_acid", 100,
                             dict(fat_g=0.0, saturates_g=0.0, carbohydrates_g=1.0,
                                  sugars_g=0.4, fibre_g=0.0, protein_g=0.0, salt_g=0.01))}],
    )
    # 100 g × 1 g/100 g = 1 g de glucides, sans la moindre perte, ÷ 1000 g.
    assert estimation.per_100g["carbohydrates_g"] == 0.1
    vinaigre = estimation.ingredients[0]
    assert vinaigre.transformations == ["aucune — compté au prorata"]


def test_a_support_is_fermented_but_never_leached():
    """Il est ajouté APRÈS l'égouttage : il ne trempe pas, mais il fermente."""
    estimation = estimate_batch_nutrition(
        harvest_weight_g=1000,
        ingredients=[_ing("Farine de riz", "inoculation_support", 100, RIZ)],
    )
    support = estimation.ingredients[0]
    assert support.transformations == ["fermentation"]
    # Les protéines traversent la fermentation intactes : 100 g × 6 % = 6 g.
    assert estimation.per_100g["protein_g"] == pytest.approx(0.6, abs=0.01)


def test_roasting_only_bites_on_sugars():
    """Une torréfaction chasse de l'eau, et l'eau n'est pas un nutriment. Seule
    la réaction de Maillard mord, et sur les sucres."""
    # Un kinako plausible : le soja torréfié est bien plus sucré que le riz,
    # sinon l'écart se perdrait dans l'arrondi au centième.
    KINAKO = dict(fat_g=25.0, saturates_g=3.6, carbohydrates_g=14.0, sugars_g=10.0,
                  fibre_g=18.0, protein_g=37.0, salt_g=0.01)
    brut = estimate_batch_nutrition(
        harvest_weight_g=1000,
        ingredients=[_ing("Kinako", "inoculation_support", 100, KINAKO)])
    torrefie = estimate_batch_nutrition(
        harvest_weight_g=1000,
        ingredients=[{**_ing("Kinako", "inoculation_support", 100, KINAKO),
                      "roasting_required": True}])
    assert torrefie.per_100g["sugars_g"] < brut.per_100g["sugars_g"]
    for champ in ("protein_g", "fat_g", "fibre_g", "carbohydrates_g"):
        assert torrefie.per_100g[champ] == brut.per_100g[champ], champ
    assert "torréfaction" in torrefie.ingredients[0].transformations
