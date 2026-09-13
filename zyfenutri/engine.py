"""Valeurs nutritionnelles estimées d'un lot — la chaîne complète.

Méthode et réglementation : `refs/methode.md`. Ce module en est la mise en œuvre ; il n'invente
aucune règle, il applique celles qui y sont écrites et **dit ce qu'il fait** à
chaque étape (`steps`), pour qu'un contrôle puisse dérouler le calcul.

Le principe qui porte tout : **on raisonne en masses absolues de nutriments**,
pas en pourcentages, jusqu'à la toute dernière division.

    pour chaque intrant : masse nette pesée × sa composition pour 100 g
      − ce qui part avec les pellicules au dépelliculage
      − ce qui part dans l'eau de trempage et de cuisson
      − ce que le mycélium consomme
    ÷ poids de tempeh récolté  →  valeurs pour 100 g de produit fini

⚠️ **La dernière division porte l'hydratation à elle seule.** Si le lot a fait
×2 en poids grâce à l'eau reprise, diviser par le poids récolté divise
mécaniquement toutes les valeurs par 2. Il ne faut donc **surtout pas** ajouter
une correction d'hydratation : elle compterait l'eau deux fois. C'est la même
idée que le facteur de rendement, mais ici le nombre est **pesé**, pas décidé.

⚠️ Ce qui reste à corriger explicitement, ce sont les pertes **sélectives** :
la pesée voit bien que de la masse est partie, mais pas que ce qui est parti
n'avait pas la composition moyenne du grain. Les pellicules sont presque
uniquement des fibres ; l'eau de trempage emporte surtout des sucres solubles
et des minéraux ; le mycélium brûle surtout des glucides.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from zyfenutri.annexe_xiv import NUTRIENT_FIELDS, energy_kcal, energy_kj

SUBSTRATE = "substrate"
SOAKING_ACID = "soaking_acid"

#: Hypothèses de perte, en %. Toutes **modifiables par l'appelant**
#: et historisées à chaque changement — ce sont des hypothèses documentées, pas
#: des vérités. Volontairement prudentes.
DEFAULT_COEFFICIENTS: dict[str, float] = {
    # ── T1 · Dépelliculage ───────────────────────────────────────────────────
    # Les pellicules de légumineuse sont presque intégralement des fibres.
    # Retirer 12 % de la masse ne retire donc PAS 12 % de chaque nutriment.
    "nutrition_hull_fibre_pct": 85.0,

    # ── T2a · Trempage + cuisson (lessivage) ─────────────────────────────────
    # Un seul coefficient pour les deux étapes : la pesée ne permet pas
    # d'attribuer la perte à l'une plutôt qu'à l'autre. Deux nombres dont un
    # seul écart est observable, c'est deux nombres à régler pour en corriger un.
    "nutrition_leaching_carbs_pct": 50.0,     # sucres et oligosaccharides
    "nutrition_leaching_protein_pct": 3.0,    # fraction soluble
    "nutrition_leaching_minerals_pct": 35.0,  # sel et minéraux

    # ── T2b · Fermentation ───────────────────────────────────────────────────
    # Le mycélium respire : il brûle des glucides pour son énergie, et entame
    # les lipides via ses lipases. Les protéines sont hydrolysées, pas
    # consommées — leur masse se conserve pour l'essentiel.
    "nutrition_fermentation_carbs_pct": 60.0,
    "nutrition_fermentation_fat_pct": 5.0,

    # ── T3 · Torréfaction (supports d'inoculation) ───────────────────────────
    # ⚠️ Une torréfaction chasse surtout de l'EAU, et l'eau n'est pas un
    # nutriment : en masses absolues, elle ne change donc presque rien. Le seul
    # effet réel sur les sept valeurs est la réaction de Maillard, qui consomme
    # des sucres réducteurs.
    "nutrition_roasting_sugars_pct": 15.0,
}

# ══════════════════════════════════════════════════════════════════════════════
#  D'OÙ VIENNENT CES SEPT NOMBRES — calage du 2026-09-13
# ══════════════════════════════════════════════════════════════════════════════
#  Trois couples graine → tempeh, chacun issu d'une SEULE table (mêmes
#  conventions d'analyse des deux côtés) : USDA 174270→174272,
#  Nouvelle-Zélande X230→X10030, Norvège. Voir `refs/official/`.
#
#  ── Ce que les trois confirment ──────────────────────────────────────────
#
#  **Le rapport lipides/protéines ne bouge pas** : 0,546→0,532 (USDA),
#  0,514→0,517 (NZ), 0,518→0,532 (Norvège) — ±3 %. C'est le résultat le plus
#  robuste du lot : protéines et lipides traversent la tempehisation ensemble,
#  et presque intacts. D'où 3 % et 5 %, confirmés plutôt que déduits.
#
#  **Les minéraux partent à l'eau** : les cendres retiennent 58 à 75 %. D'où
#  35 % de perte (le coefficient valait 12 % — trop doux).
#
#  ── La contradiction apparente, et sa résolution ─────────────────────────
#
#  La perte de matière sèche semblait osciller de 10 % (NZ) à 23 % (USDA). Elle
#  est en fait **imposée par l'eau du tempeh et le rendement**, qui sont liés :
#
#      matière sèche sortante = rendement × (100 − eau du tempeh)
#
#  Trois sources sur quatre donnent un tempeh frais à **59–60 % d'eau** (USDA
#  59,6 · Norvège 59,0 · Suède 59,6) ; la NZ est l'exception à 56,2. Avec le
#  rendement **1,75** et 59,6 % d'eau, la perte de matière
#  sèche vaut nécessairement **22 %** — et non 10. Les glucides en portent
#  l'essentiel, d'où 50 % puis 60 %.
#
#  ── Ce qu'on refuse de caler ─────────────────────────────────────────────
#
#  ⚠️ **Les AG saturés.** Les trois couples donnent une rétention de 128 à
#  186 % : on ne crée pas d'acide gras saturé. Les chiffres sont inutilisables.
#  Leur DIRECTION, en revanche, est unanime — la part saturée des lipides monte
#  de +3,8 à +10,8 points (le mycélium oxyde de préférence les insaturés).
#  Notre modèle garde le rapport constant, ce qui **sous-estime probablement les
#  AGS**. C'est le sens défavorable pour une étiquette, et c'est l'inconnue n° 1.
#
#  ⚠️ **Les fibres seules.** La frontière fibres / glucides est une convention
#  d'analyse : la graine en déclare 9,3 g (USDA, NZ) ou 16,0 (Norvège) sans que
#  le produit change. Aucune rétention n'en est tirable. Elles sont donc tenues
#  pour conservées, ce qui en fait un **majorant** — le sens défavorable pour
#  une allégation « source de fibres ».
#
#  ⚠️ **La graine norvégienne** annonce 20 g d'eau (8,5 à 8,8 ailleurs) et ne
#  publie pas ses cendres : inexploitable pour un bilan de masse. Seuls ses
#  rapports ont servi.
# ══════════════════════════════════════════════════════════════════════════════

#: Les deux « dont » : ils suivent leur total, ils n'ont pas de règle propre.
#: ⚠️ Les AGS en particulier — cf. l'avertissement du bloc de calage.
SUBSET_FOLLOWS = {"saturates_g": "fat_g", "sugars_g": "carbohydrates_g"}


# ══════════════════════════════════════════════════════════════════════════════
#  LES TRANSFORMATIONS
# ══════════════════════════════════════════════════════════════════════════════
#  Chacune est une fonction PURE : des masses absolues de nutriments entrent,
#  d'autres sortent. Une règle par nutriment et par transformation, et rien
#  d'autre — l'énergie n'y figure pas, elle se recalcule à la fin depuis les
#  macros (annexe XIV), comme le règlement l'impose sur un produit fini.
#
#  ⚠️ On raisonne en MASSES ABSOLUES du début à la fin. Aucune transformation ne
#  touche à l'eau : l'hydratation est portée par la division finale, et une
#  seule fois. C'est la règle qui empêche de compter l'eau deux fois.
# ══════════════════════════════════════════════════════════════════════════════

def _ratios(coef: dict[str, float], regles: dict[str, str | None]) -> dict[str, float]:
    """Une règle par nutriment → la fraction qui SURVIT à l'étape."""
    return {champ: 1.0 - coef.get(cle, 0.0) / 100.0 if cle else 1.0
            for champ, cle in regles.items()}


#: T2a — trempage et cuisson. L'eau est jetée : ce qui y passe est perdu.
_TREMPAGE_CUISSON = {
    "fat_g": None,                                    # insoluble
    "saturates_g": None,
    "carbohydrates_g": "nutrition_leaching_carbs_pct",
    "sugars_g": "nutrition_leaching_carbs_pct",
    "fibre_g": None,                                  # insolubles pour l'essentiel
    "protein_g": "nutrition_leaching_protein_pct",
    "salt_g": "nutrition_leaching_minerals_pct",
}

#: T2b — fermentation. Le mycélium respire.
_FERMENTATION = {
    "fat_g": "nutrition_fermentation_fat_pct",
    "saturates_g": "nutrition_fermentation_fat_pct",
    "carbohydrates_g": "nutrition_fermentation_carbs_pct",
    "sugars_g": "nutrition_fermentation_carbs_pct",
    "fibre_g": None,                                  # cf. calage : non calable
    "protein_g": None,                                # hydrolysées, pas brûlées
    "salt_g": None,                                   # un minéral ne se consomme pas
}

#: T3 — torréfaction. Seule la réaction de Maillard mord, et sur les sucres.
_TORREFACTION = {
    "fat_g": None, "saturates_g": None,
    "carbohydrates_g": None,
    "sugars_g": "nutrition_roasting_sugars_pct",
    "fibre_g": None, "protein_g": None, "salt_g": None,
}


def appliquer(masses: dict[str, float], regles: dict[str, str | None],
              coef: dict[str, float]) -> dict[str, float]:
    """Une transformation : chaque nutriment perd la fraction qui lui est due."""
    survie = _ratios(coef, regles)
    return {champ: masse * survie.get(champ, 1.0) for champ, masse in masses.items()}


def depelliculage(masses: dict[str, float], *, composition: dict[str, float],
                  hull_mass_g: float, coef: dict[str, float]) -> tuple[dict[str, float], str | None]:
    """T1 — retirer la pellicule, qui n'a pas la composition moyenne du grain.

    ⚠️ C'est tout l'objet de cette étape : la pesée voit bien qu'il manque de la
    masse, elle ne voit pas que ce qui est parti était presque uniquement des
    fibres. Appliquer la composition moyenne au poids net sous-estimerait les
    protéines et les lipides du produit fini.
    """
    part_fibres = coef["nutrition_hull_fibre_pct"] / 100.0
    sortie = dict(masses)
    alerte = None

    retire = hull_mass_g * part_fibres
    fibres = masses.get("fibre_g")
    if fibres is not None:
        # ⚠️ On ne peut pas retirer plus de fibres que le grain n'en contient.
        # Si la borne mord, la fiche et les poids se contredisent — on le DIT,
        # plutôt que de rendre un zéro qui passerait pour une mesure.
        if retire > fibres * 0.95:
            alerte = ("les pellicules retirées emporteraient plus de fibres que la fiche "
                      "produit n'en déclare. Vérifiez la fiche ou les poids brut/net — "
                      "la valeur de fibres est un plancher, pas une mesure.")
            retire = fibres * 0.95
        sortie["fibre_g"] = max(0.0, fibres - retire)

    # Le reste de la pellicule (15 %) emporte les autres nutriments au prorata.
    reste = hull_mass_g * (1 - part_fibres)
    for champ, masse in masses.items():
        if champ == "fibre_g":
            continue
        sortie[champ] = max(0.0, masse - reste * composition.get(champ, 0.0) / 100.0)
    return sortie, alerte


# ══════════════════════════════════════════════════════════════════════════════
#  QUI SUBIT QUOI
# ══════════════════════════════════════════════════════════════════════════════
#  ⚠️ Le support d'inoculation ne trempe pas et ne cuit pas : il est ajouté
#  APRÈS l'égouttage. Il fermente, en revanche, puisqu'il est dans le bloc
#  pendant l'incubation. « Tempehisation » recouvre donc deux étapes qui ne
#  s'appliquent pas au même monde.
#
#  ⚠️ La PASTEURISATION ne figure pas ici, et ce n'est pas un oubli : une
#  chauffe douce ne déplace aucune masse de protéines, de lipides, de glucides,
#  de fibres ni de sel. Elle détruit des vitamines (B1, B9, C) et de la flore —
#  ni les unes ni l'autre ne sont déclarées. Si elle se fait à découvert, elle
#  fait perdre de l'eau : c'est une concentration, déjà portée par la pesée
#  finale. Tant qu'elle n'est pas pratiquée, rien à modéliser ; le jour où elle
#  le sera, il n'y aura toujours rien à modéliser sur les sept valeurs.
PIPELINE: dict[str, tuple[str, ...]] = {
    "substrate": ("depelliculage", "trempage_cuisson", "fermentation"),
    "inoculation_support": ("torrefaction", "fermentation"),
    "inoculation_acid": (),          # tel quel, au prorata de sa masse
}

#: Exclus du calcul, et pourquoi.
EXCLUS = {
    "soaking_acid": "part avec l'eau de trempage, qui est jetée",
    "starter": "part négligeable dans la masse du produit fini",
}

@dataclass
class IngredientContribution:
    """Ce qu'un intrant apporte, et ce qui lui a été appliqué."""
    input_type_name: str
    category: str | None
    spec_identifier: str | None
    net_weight_g: float | None
    gross_weight_g: float | None
    dehulled: bool = False
    counted: bool = True
    #: Les transformations subies, dans l'ordre — c'est la ligne qu'on montre.
    transformations: list[str] = field(default_factory=list)
    #: Pourquoi il ne compte pas, quand il ne compte pas.
    excluded_reason: str | None = None
    #: Masses de nutriments apportées, après corrections (g).
    nutrients: dict[str, float] = field(default_factory=dict)


@dataclass
class BatchNutrition:
    complete: bool
    harvest_weight_g: float | None
    per_100g: dict[str, float | None]
    energy_kj: float | None
    energy_kcal: float | None
    ingredients: list[IngredientContribution]
    #: Ce qui manque pour que l'estimation soit complète, en clair.
    missing: list[str]
    #: Incohérences détectées — le calcul a abouti, mais il faut regarder.
    warnings: list[str]
    #: La chaîne déroulée, étape par étape — c'est la fiche de calcul.
    steps: list[str]
    coefficients: dict[str, float]
    #: Vrai quand le poids récolté a été PRÉDIT par le facteur de rendement,
    #: faute d'avoir été pesé. La valeur reste une estimation d'estimation.
    harvest_weight_estimated: bool = False


def estimate_batch_nutrition(
    *,
    harvest_weight_g: float | None,
    ingredients: list[dict],
    coefficients: dict[str, float] | None = None,
) -> BatchNutrition:
    """Valeurs pour 100 g de tempeh fini.

    `ingredients` : une entrée par ligne du lot — `input_type_name`,
    `category`, `net_weight_g`, `gross_weight_g`, `dehulled`,
    `spec_identifier`, et `composition` (les 7 valeurs pour 100 g, ou None).
    """
    coef = {**DEFAULT_COEFFICIENTS, **(coefficients or {})}
    steps: list[str] = []
    missing: list[str] = []
    warnings: list[str] = []
    contributions: list[IngredientContribution] = []
    totals: dict[str, float] = {f: 0.0 for f in NUTRIENT_FIELDS}

    for item in ingredients:
        contribution = IngredientContribution(
            input_type_name=item["input_type_name"],
            category=item.get("category"),
            spec_identifier=item.get("spec_identifier"),
            net_weight_g=item.get("net_weight_g"),
            gross_weight_g=item.get("gross_weight_g"),
            dehulled=bool(item.get("dehulled")),
        )

        # ── L'eau de trempage est jetée : ce qu'on y a versé ne finit pas dans
        #    le produit. L'exclure sous-déclare légèrement (un peu d'acide
        #    pénètre le grain) — c'est le sens prudent.
        # ── Ce qui ne compte pas, et pourquoi (cf. EXCLUS) ─────────────────
        # ⚠️ Exclure sous-déclare légèrement — un peu d'acide pénètre le grain,
        # le starter pèse quelques grammes. C'est le sens prudent.
        raison = EXCLUS.get(item.get("category") or "")
        if raison:
            contribution.counted = False
            contribution.excluded_reason = raison
            contributions.append(contribution)
            continue

        composition = item.get("composition")
        net = item.get("net_weight_g")
        if not composition or not any(v is not None for v in composition.values()):
            contribution.counted = False
            # ⚠️ Message ACTIONNABLE : l'absence de fiche fournisseur n'est pas
            # une impasse. L'article 31 § 4 admet la méthode c) — « données
            # généralement établies et acceptées », c'est-à-dire Ciqual. Sans
            # cette indication, on croit devoir attendre un document qui ne
            # viendra jamais, et l'estimation reste bloquée indéfiniment.
            contribution.excluded_reason = (
                "aucune fiche produit sur la spécification reçue — à défaut de "
                "fiche fournisseur, reprenez la ligne Ciqual (méthode c)"
            )
            missing.append(
                f"{item['input_type_name']} — pas de fiche produit "
                "(à défaut du fournisseur : Ciqual)"
            )
            contributions.append(contribution)
            continue
        if not net:
            contribution.counted = False
            contribution.excluded_reason = "aucun poids saisi pour cet intrant"
            missing.append(f"{item['input_type_name']} — pas de poids")
            contributions.append(contribution)
            continue
        absent = [f for f in NUTRIENT_FIELDS if composition.get(f) is None]
        if absent:
            missing.append(
                f"{item['input_type_name']} — fiche produit incomplète "
                f"({len(absent)} valeur{'s' if len(absent) > 1 else ''} manquante"
                f"{'s' if len(absent) > 1 else ''})"
            )

        categorie = item.get("category") or ""
        # ⚠️ La catégorie décide des transformations — sauf si l'appelant les
        # impose. Ce n'est pas une porte dérobée : un échantillon de laboratoire
        # prélevé APRÈS cuisson n'a plus qu'à fermenter, et aucune catégorie du
        # référentiel ne décrit cet état. Mieux vaut le déclarer que de
        # détourner une catégorie voisine.
        etapes_intrant = (tuple(item["transformations"])
                          if item.get("transformations") is not None
                          else PIPELINE.get(categorie, ()))
        gross = item.get("gross_weight_g")
        # Le dépelliculage n'a lieu que s'il a été PESÉ : c'est l'écart
        # brut − net qui donne la masse de pellicule, pas une hypothèse.
        dehulled = (bool(item.get("dehulled")) and "depelliculage" in etapes_intrant
                    and gross is not None and gross > net)
        contribution.dehulled = dehulled

        # ⚠️ Quand le grain est dépelliculé, la fiche décrit le grain TEL
        # QU'ACHETÉ, pellicules comprises : on part donc du poids BRUT.
        base = gross if dehulled else net
        masses = {champ: base * composition[champ] / 100.0
                  for champ in NUTRIENT_FIELDS if composition.get(champ) is not None}

        if dehulled:
            masses, alerte = depelliculage(
                masses, composition=composition, hull_mass_g=gross - net, coef=coef)
            if alerte:
                warnings.append(f"{item['input_type_name']} : {alerte}")
            contribution.transformations.append("dépelliculage")

        if "trempage_cuisson" in etapes_intrant:
            masses = appliquer(masses, _TREMPAGE_CUISSON, coef)
            contribution.transformations.append("trempage et cuisson")
        if "torrefaction" in etapes_intrant and item.get("roasting_required"):
            masses = appliquer(masses, _TORREFACTION, coef)
            contribution.transformations.append("torréfaction")
        if "fermentation" in etapes_intrant:
            masses = appliquer(masses, _FERMENTATION, coef)
            contribution.transformations.append("fermentation")
        if not etapes_intrant:
            # Acidifiant pré-inoculation : ajouté après cuisson, il traverse
            # sans rien perdre. Sa seule règle est sa proportion.
            contribution.transformations.append("aucune — compté au prorata")

        for champ, masse in masses.items():
            contribution.nutrients[champ] = round(masse, 3)
            totals[champ] += masse

        contributions.append(contribution)

    counted = [c for c in contributions if c.counted]
    if counted:
        steps.append(
            "Apport de chaque intrant : masse pesée × sa composition pour 100 g "
            f"({len(counted)} intrant{'s' if len(counted) > 1 else ''} compté"
            f"{'s' if len(counted) > 1 else ''})"
        )
    for exclu in (c for c in contributions if not c.counted):
        steps.append(f"{exclu.input_type_name} : non compté — {exclu.excluded_reason}")

    if any(c.dehulled for c in counted):
        steps.append(
            f"T1 · Dépelliculage : on part du poids BRUT, puis on retire la pellicule, "
            f"comptée à {coef['nutrition_hull_fibre_pct']:g} % de fibres — elle n'emporte "
            "donc presque pas de protéines ni de lipides"
        )
    if any("trempage et cuisson" in c.transformations for c in counted):
        steps.append(
            f"T2a · Trempage et cuisson (substrats) : −{coef['nutrition_leaching_carbs_pct']:g} % "
            f"de glucides, −{coef['nutrition_leaching_protein_pct']:g} % de protéines, "
            f"−{coef['nutrition_leaching_minerals_pct']:g} % de sel et minéraux partis à l'eau, "
            "qui est jetée. Lipides et fibres : insolubles, rien ne part"
        )
    if any("torréfaction" in c.transformations for c in counted):
        steps.append(
            f"T3 · Torréfaction (supports) : −{coef['nutrition_roasting_sugars_pct']:g} % de "
            "sucres consommés par la réaction de Maillard. Le reste ne bouge pas — une "
            "torréfaction chasse de l'eau, et l'eau n'est pas un nutriment"
        )
    if any("fermentation" in c.transformations for c in counted):
        steps.append(
            f"T2b · Fermentation (substrats et supports) : "
            f"−{coef['nutrition_fermentation_carbs_pct']:g} % de glucides et "
            f"−{coef['nutrition_fermentation_fat_pct']:g} % de lipides consommés par le "
            "mycélium ; les protéines sont hydrolysées, pas brûlées"
        )
    if any(not c.transformations or c.transformations == ["aucune — compté au prorata"]
           for c in counted):
        steps.append(
            "Acidifiant pré-inoculation : ajouté après la cuisson, il traverse sans "
            "rien perdre — sa seule règle est sa proportion"
        )

    # ══════════════════════════════════════════════════════════════════════
    #  T5 · LA DILUTION — division par le poids de tempeh
    # ══════════════════════════════════════════════════════════════════════
    #  ⚠️ C'est ICI, et nulle part ailleurs, que l'eau reprise entre dans le
    #  calcul. Un lot qui a fait ×2 en reprenant de l'eau voit toutes ses
    #  valeurs divisées par 2. Ajouter un « facteur d'hydratation » en plus
    #  compterait l'eau deux fois — la faute à ne jamais commettre ici.
    #
    #  Deux façons de connaître ce poids, et elles ne se valent pas :
    #    • PESÉ (`harvest_weight_g`) — c'est une mesure, on s'y tient ;
    #    • PRÉDIT par le facteur de rendement de chaque substrat, quand rien
    #      n'a encore été pesé. C'est ce qui permet de sortir une fiche depuis
    #      une simple recette, avant d'avoir produit quoi que ce soit.
    #
    #  ⚠️ Le facteur de rendement s'applique au poids BRUT du substrat, et à
    #  lui seul : il absorbe déjà le dépelliculage (en moins) et l'hydratation
    #  (en plus). Un support ou un acidifiant n'a pas de rendement — sa masse
    #  s'ajoute au produit sans le faire gonfler.
    predit = False
    if not harvest_weight_g:
        attendu = sum(
            (item.get("gross_weight_g") or item.get("net_weight_g") or 0.0)
            * (item.get("yield_factor") or 0.0)
            for item in ingredients
            if item.get("category") == SUBSTRATE and item.get("yield_factor")
        )
        if attendu > 0:
            harvest_weight_g = round(attendu, 1)
            predit = True
            steps.append(
                f"Poids de tempeh PRÉDIT — aucune pesée : {harvest_weight_g:g} g, "
                "obtenus en multipliant le poids brut de chaque substrat par son "
                "facteur de rendement. C'est une estimation d'estimation"
            )

    per_100g: dict[str, float | None] = {f: None for f in NUTRIENT_FIELDS}
    if harvest_weight_g and harvest_weight_g > 0 and counted:
        for nutrient in NUTRIENT_FIELDS:
            per_100g[nutrient] = round(totals[nutrient] / harvest_weight_g * 100.0, 2)
        # Un « dont » au-dessus de son total n'a aucun sens physique : il ne peut
        # venir que d'un arrondi ou d'une fiche incohérente.
        for subset, total in SUBSET_FOLLOWS.items():
            if per_100g[subset] is not None and per_100g[total] is not None:
                per_100g[subset] = min(per_100g[subset], per_100g[total])
        steps.append(
            f"Ramené à 100 g de produit fini : ÷ {harvest_weight_g:g} g récoltés. "
            "C'est cette division qui porte l'eau reprise — un lot qui a fait ×2 "
            "voit toutes ses valeurs divisées par 2"
        )
        steps.append("Énergie calculée depuis les macronutriments (annexe XIV), jamais recopiée")
    elif not harvest_weight_g:
        missing.append("Poids de récolte du lot")
    if predit:
        missing.append(
            "Poids de récolte non pesé — prédit par le facteur de rendement, "
            "utilisable pour concevoir une recette, pas pour étiqueter"
        )

    return BatchNutrition(
        # ⚠️ Une récolte PRÉDITE ne rend pas la fiche complète : on ne met pas
        # sur un emballage un chiffre dont le dénominateur est lui-même estimé.
        complete=not missing and bool(counted) and bool(harvest_weight_g) and not predit,
        harvest_weight_g=harvest_weight_g,
        harvest_weight_estimated=predit,
        per_100g=per_100g,
        energy_kj=energy_kj(per_100g["fat_g"], per_100g["carbohydrates_g"],
                            per_100g["protein_g"], per_100g["fibre_g"]),
        energy_kcal=energy_kcal(per_100g["fat_g"], per_100g["carbohydrates_g"],
                                per_100g["protein_g"], per_100g["fibre_g"]),
        ingredients=contributions,
        missing=missing,
        warnings=warnings,
        steps=steps,
        coefficients=coef,
    )


def calibrate_fermentation(*, estimated_carbs_g: float, reference_carbs_g: float,
                           current_pct: float) -> float:
    """Coefficient de fermentation qui ferait coïncider l'estimation et une référence.

    L'usage prévu : on estime un lot de tempeh de **soja**, dont la composition
    est bien documentée dans les tables, et on lit l'écart sur les glucides —
    le nutriment que le mycélium consomme le plus. Le coefficient qui annule
    cet écart est une mesure de l'activité de fermentation.

    ⚠️ Le résultat ne s'applique **pas** tout seul : c'est une lecture, qu'on
    reporte à la main dans les coefficients si on la juge fondée. Une seule
    mesure ne fait pas une consigne.
    """
    if estimated_carbs_g <= 0 or reference_carbs_g < 0:
        raise ValueError("Les glucides estimés doivent être strictement positifs")
    remaining = 1.0 - current_pct / 100.0
    if remaining <= 0:
        raise ValueError("Le coefficient courant ne peut pas atteindre 100 %")
    # glucides_avant_fermentation = estimé / (1 − courant)
    # coefficient cherché = 1 − référence / glucides_avant_fermentation
    before = estimated_carbs_g / remaining
    return round(max(0.0, min(99.0, (1.0 - reference_carbs_g / before) * 100.0)), 1)
