# Valeurs nutritionnelles — réglementation et méthode de calcul

> **Objet.** Établir les valeurs nutritionnelles d'un tempeh **par le calcul**, sans analyse
> de laboratoire, d'une manière qui tienne devant un contrôle. Ce document est la **méthode** :
> il doit pouvoir être présenté tel quel à la DDPP, avec les fiches de calcul (`steps`) que
> produit `zyfenutri`.
>
> Dernière vérification des sources : **11 septembre 2026**.

---

## 1. Ce que la réglementation impose

Le texte applicable est le **règlement (UE) n° 1169/2011**, dit « INCO » (information du
consommateur sur les denrées alimentaires).

### 1.1 Le calcul est une méthode légale — ce n'est pas un pis-aller

C'est le point de départ, et il est explicite. **[Article 31, paragraphe 4](https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX:02011R1169-20180101)** :

> Les valeurs déclarées sont, selon le cas, des valeurs moyennes établies sur la base :
> a) de l'analyse du produit effectuée par le fabricant ;
> b) du calcul effectué à partir des valeurs moyennes connues ou effectives des ingrédients utilisés ; ou
> c) du calcul effectué à partir de données généralement établies et acceptées.

Trois méthodes **à égalité** — le « ou » n'introduit pas de hiérarchie.

**Méthode retenue : un mélange de b) et c)**, ce que « selon le cas » autorise explicitement. La
justification se fait **source par source**, pas une fois pour tout le produit :

| Origine de la composition | Point | Quand |
|---|---|---|
| Fiche technique du fournisseur | **b)** — valeurs effectives des ingrédients utilisés | quand le fournisseur en fournit une |
| Table **Ciqual** (ANSES) | **c)** — données généralement établies et acceptées | par défaut |

Conséquence pour la traçabilité : chaque composition d'intrant doit pouvoir être rattachée à **son
type de source** (fournisseur / table), sa **référence** et sa **date**. Une valeur issue d'une
fiche fournisseur est de plus **liée à ce fournisseur** : un changement d'approvisionnement oblige
à la reprendre, là où une table générique amortit déjà la variabilité des origines.

`zyfenutri` ne conserve pas ces informations : il reçoit des compositions et rend un calcul. Les
archiver revient à qui s'en sert (§ 4).

Les valeurs déclarées sont des **valeurs moyennes**, pas des maxima ni des garanties. Un
laboratoire n'est donc **pas obligatoire** — à condition que le calcul repose sur des données
fiables et qu'il soit documenté (voir §4).

### 1.2 Les sept valeurs obligatoires

L'**article 30, paragraphe 1** fixe le contenu minimal, **pour 100 g**, dans cet ordre :

| | Unité |
|---|---|
| Énergie | **kJ et kcal** (les deux) |
| Matières grasses | g |
| *dont* acides gras saturés | g |
| Glucides | g |
| *dont* sucres | g |
| Protéines | g |
| Sel | g |

Les **fibres** sont facultatives mais autorisées (article 30, paragraphe 2) — et parlantes sur un
produit comme le tempeh. Si on les déclare, elles entrent dans le calcul de l'énergie.

⚠️ **« Glucides » au sens INCO = glucides assimilables**, fibres exclues. Beaucoup de tables
(dont certaines lignes de Ciqual) donnent des glucides *totaux*, fibres comprises. Confondre les
deux gonfle à la fois les glucides et l'énergie.

### 1.3 L'énergie se calcule, elle ne se recopie pas

L'**annexe XIV** fixe les coefficients de conversion. C'est une règle de calcul, pas une donnée
à reprendre d'une table :

| Nutriment | kJ/g | kcal/g |
|---|---|---|
| Matières grasses | 37 | 9 |
| Glucides (assimilables) | 17 | 4 |
| Protéines | 17 | 4 |
| Fibres | 8 | 2 |
| Polyols | 10 | 2,4 |
| Acides organiques | 13 | 3 |

Additionner les énergies lues dans Ciqual au lieu de recalculer donne un chiffre **incohérent avec
ses propres macronutriments** — c'est la première chose qu'un contrôleur recoupe.

### 1.4 Une exemption possible : l'annexe V, point 19

L'**annexe V** liste les denrées dispensées de déclaration nutritionnelle obligatoire. Son
**point 19** vise les denrées, **y compris de fabrication artisanale**, fournies **directement par
le fabricant en faibles quantités** au consommateur final ou à des **commerces de détail locaux**
qui approvisionnent directement le consommateur final.

C'est potentiellement le cas d'une petite production de tempeh (marché, vente directe, dépôts
locaux). **Mais :**

- « faibles quantités » et « local » ne sont **pas chiffrés** dans le règlement — l'appréciation
  revient aux autorités nationales ;
- l'exemption **tombe dès qu'une allégation** nutritionnelle ou de santé est faite (« riche en
  protéines », « source de fibres »…) : dans ce cas la déclaration redevient obligatoire ;
- elle tombe aussi si la distribution sort du circuit local (grossiste, vente en ligne nationale) ;
- **déclarer volontairement reste possible et souvent commercialement souhaitable** — mais dès
  qu'on déclare, on est tenu par les règles ci-dessus, exemption ou pas.

**Conclusion pratique** : l'exemption ne dispense pas de savoir calculer. Elle enlève la
contrainte, pas l'intérêt.

---

## 2. Les tolérances — non, ce n'est pas « ±20 % » partout

C'est la correction la plus importante de ce document.

La référence est le **guide de la Commission européenne** de décembre 2012, *« Guide à l'intention
des autorités compétentes pour le contrôle de la conformité… ayant trait à la fixation de
tolérances pour les valeurs nutritionnelles déclarées sur les étiquettes »*.

⚠️ **Deux avertissements avant de s'appuyer dessus.**

**Ce guide n'a aucune valeur juridique.** Il le dit lui-même en première page : en cas de litige,
l'interprétation de la loi appartient en dernier ressort à la Cour de justice de l'Union
européenne. C'est un outil de **contrôle** à destination des autorités, pas un droit à l'erreur
opposable.

**Ce n'est pas un pourcentage unique.** Le ±20 % n'est qu'**une bande parmi d'autres**, et pour
les petites quantités c'est une tolérance **absolue** qui s'applique, pas un pourcentage.

### Tableau 1 du guide — denrées alimentaires (hors compléments)

*Incertitude de mesure comprise.*

| Nutriment | Tolérance |
|---|---|
| Glucides, sucres, protéines, fibres | < 10 g/100 g : **± 2 g**<br>10 à 40 g/100 g : **± 20 %**<br>> 40 g/100 g : **± 8 g** |
| Matières grasses | < 10 g/100 g : **± 1,5 g**<br>10 à 40 g/100 g : **± 20 %**<br>> 40 g/100 g : **± 8 g** |
| Acides gras saturés | < 4 g/100 g : **± 0,8 g**<br>≥ 4 g/100 g : **± 20 %** |
| Sel | < 1,25 g/100 g : **± 0,375 g**<br>≥ 1,25 g/100 g : **± 20 %** |
| Sodium | < 0,5 g/100 g : **± 0,15 g**<br>≥ 0,5 g/100 g : **± 20 %** |
| Vitamines | + 50 % / − 35 % |
| Minéraux | + 45 % / − 35 % |

### Ce que ça donne pour un tempeh de légumineuses

| Valeur déclarée (ordre de grandeur) | Bande applicable | Tolérance réelle |
|---|---|---|
| Protéines ~ 18 g | 10–40 g | ± 20 % → ~ ± 3,6 g |
| Glucides ~ 12 g | 10–40 g | ± 20 % → ~ ± 2,4 g |
| Fibres ~ 6 g | < 10 g | **± 2 g** (soit ± 33 %) |
| Matières grasses ~ 5 g | < 10 g | **± 1,5 g** (soit ± 30 %) |
| AG saturés ~ 1 g | < 4 g | **± 0,8 g** |
| Sel ~ 0,02 g | < 1,25 g | **± 0,375 g** |

Autrement dit : sur les nutriments **minoritaires**, la tolérance absolue est **plus généreuse**
que 20 %. Sur les protéines — le nutriment qui compte pour le tempeh, et celui qu'un contrôle
dosera en premier — c'est bien ± 20 %, et c'est le plus contraignant du lot.

### Deux subtilités qui jouent en notre faveur

**La tolérance inclut l'incertitude de mesure.** Le guide le précise : inutile de la majorer pour
en tenir compte. Mais c'est aussi dire que l'incertitude du labo de contrôle est *déjà consommée*
par la bande.

**Les arrondis élargissent l'intervalle.** La tolérance se calcule à partir des valeurs extrêmes
qui s'arrondissent à la valeur déclarée. Exemple du guide : « 12 g » de protéines couvre 11,5 à
12,4 g ; la borne haute de tolérance est 12,4 + 20 % = 14,88 → arrondi à 15 g. Une mesure à 15 g
est conforme, 16 g ne l'est pas.

### Règles d'arrondi (point 6 du guide)

| Élément | Règle |
|---|---|
| Énergie | à l'unité de kJ/kcal (aucune décimale) |
| Matières grasses, glucides, sucres, protéines, fibres | ≥ 10 g : au gramme<br>< 10 g et > 0,5 g : au décigramme<br>≤ 0,5 g : « 0 g » ou « < 0,5 g » |
| Sel | ≥ 1 g : au décigramme<br>< 1 g : au centigramme<br>≤ 0,0125 g : « 0 g » ou « < 0,01 g » |

Une étiquette affichant « 12,3456 g » est fautive : elle suggère une précision irréaliste.

---

## 3. La méthode de calcul retenue

### 3.1 Le principe, et pourquoi il est plus solide que l'estimation classique

La méthode habituelle consiste à appliquer un **facteur de gonflement estimé** aux valeurs des
ingrédients secs. Elle est inutile ici : **les deux bouts de la chaîne se pèsent.**

```
  masse de chaque ingrédient (poids NET)        →  weight_g, par intrant
                     ↓
              fabrication
                     ↓
        poids de tempeh récolté                 →  harvested_g
```

Le rapport entre les deux **est** le facteur de dilution. Il n'est pas estimé : il est pesé, lot par
lot, et il porte à lui seul l'eau reprise à l'hydratation. Restent à chiffrer les **nutriments**
perdus en route — à l'eau de trempage, au mycélium —, ce que font les transformations du § 3.2.

C'est doublement préférable : plus juste, et **défendable** — on présente des pesées, pas un
facteur de gonflement emprunté à la littérature.

### 3.2 La chaîne de calcul — cinq transformations, et rien d'autre

Le calcul ne manipule que des **masses absolues de nutriments**, du début à la fin. On part de ce
qui entre dans le lot, on applique à chaque ingrédient les transformations qu'il subit réellement,
on additionne, et on divise **une seule fois** par le poids de tempeh obtenu.

Ce dernier point est la clé de la méthode : c'est cette division finale, et elle seule, qui porte
l'eau reprise au trempage. Un lot qui double de poids en s'hydratant voit mécaniquement toutes ses
valeurs divisées par deux, sans qu'aucun coefficient n'ait à le dire.

#### Qui subit quoi

| Ingrédient | Transformations appliquées |
|---|---|
| **Substrat** (soja, pois chiche, pois cassés…) | T1 dépelliculage *(si pratiqué)* → T2a trempage et cuisson → T2b fermentation |
| **Support d'inoculation** (farine de riz, kinako) | T3 torréfaction *(si pratiquée)* → T2b fermentation |
| **Acidifiant pré-inoculation** (vinaigre) | aucune — ajouté après cuisson, compté au prorata de sa masse |
| **Acidifiant de trempage** | **exclu** — il part avec l'eau de trempage, qui est jetée |
| **Starter** | **exclu** — quelques grammes pour plusieurs kilos de produit |

Les deux exclusions **sous-déclarent** légèrement le produit fini : un peu d'acide pénètre le
grain, le starter pèse quelque chose. C'est le sens prudent, celui qui n'expose pas.

Le support d'inoculation ne trempe ni ne cuit : il est ajouté **après l'égouttage**. Il fermente en
revanche, puisqu'il est dans le bloc pendant toute l'incubation. C'est pourquoi la « tempehisation »
se décompose en deux étapes qui ne concernent pas les mêmes ingrédients.

#### T1 — Dépelliculage

La pellicule d'une légumineuse est presque uniquement de la fibre. Retirer 8 % de la masse ne
retire donc pas 8 % de chaque nutriment : la pesée voit la masse partir, elle ne voit pas que ce
qui est parti n'avait pas la composition moyenne du grain.

| | Règle |
|---|---|
| Fibres | on retire **85 %** de la masse de pellicule |
| Protéines, lipides, glucides, sucres, AGS, sel | on retire les 15 % restants, au prorata de la composition |

La masse de pellicule n'est **pas** supposée : c'est l'écart entre le poids brut et le poids net,
tous deux pesés et enregistrés. Effet net : le produit fini est **plus riche** en protéines et en
lipides qu'un calcul naïf ne le dirait.

#### T2a — Trempage et cuisson

L'eau de trempage et l'eau de cuisson sont **jetées**. Ce qui s'y dissout est perdu.

| Nutriment | Perte | Pourquoi |
|---|---|---|
| Glucides assimilables et sucres | **− 50 %** | les glucides du soja sont du saccharose et des oligosaccharides (raffinose, stachyose), tous très solubles |
| Sel et minéraux | **− 35 %** | lixiviation ; les tables mesurent 25 à 42 % de cendres en moins |
| Protéines | **− 3 %** | seule la fraction soluble part |
| Lipides, fibres | **aucune** | insolubles |

Un seul coefficient couvre les deux étapes, volontairement : la pesée ne permet pas d'attribuer la
perte à l'une plutôt qu'à l'autre, et deux nombres dont un seul écart est observable, ce sont deux
nombres à régler pour en corriger un.

#### T2b — Fermentation

Le mycélium respire : il brûle des glucides pour son énergie et entame les lipides via ses lipases.

| Nutriment | Perte |
|---|---|
| Glucides assimilables et sucres | **− 60 %** |
| Lipides (et AGS, qui suivent) | **− 5 %** |
| Protéines | **aucune** — elles sont hydrolysées en peptides et acides aminés, pas consommées ; leur masse se conserve |
| Fibres, sel | **aucune** |

#### T3 — Torréfaction (supports uniquement)

Une torréfaction chasse surtout de l'**eau**, et l'eau n'est pas un nutriment : en masses absolues,
elle ne déplace donc presque rien. Le seul effet réel sur les sept valeurs déclarées est la
**réaction de Maillard**, qui consomme des sucres réducteurs : **− 15 % de sucres**, le reste
inchangé.

#### T4 — Pasteurisation : pourquoi elle ne figure pas ici

La pasteurisation n'est pas une étape systématique du tempeh. La question mérite pourtant d'être
tranchée : **une pasteurisation ne modifie aucune des sept valeurs déclarées**.

Une chauffe douce ne déplace aucune masse de protéines, de lipides, de glucides, de fibres ni de
sel — elle dénature des protéines, ce qui change leur structure et non leur masse. Elle détruit en
revanche des vitamines thermosensibles (B1, B9, C) et réduit la flore : ni les unes ni l'autre ne
figurent parmi les valeurs déclarées. Si elle se pratiquait à découvert, elle ferait perdre de l'eau, donc
concentrerait le produit — mais cette concentration serait déjà portée par la pesée finale.

Qu'elle soit pratiquée ou non, il n'y a donc rien à modéliser sur les sept valeurs.

#### T5 — La dilution : division par le poids de tempeh

```
valeur pour 100 g = masse de nutriment obtenue ÷ poids de tempeh × 100
```

Le poids de tempeh est **pesé**, et c'est ce qui donne sa solidité à la méthode : l'hydratation
n'est pas estimée, elle est mesurée.

À défaut de pesée — pour concevoir une recette avant de l'avoir produite — le calcul prédit ce
poids en multipliant le poids brut de chaque substrat par son **facteur de rendement**. Ce facteur
absorbe d'un coup les pertes au tri et au dépelliculage (en moins) et l'hydratation (en plus).
⚠️ Une fiche obtenue ainsi est explicitement marquée **incomplète** : on n'étiquette pas un produit
avec un dénominateur lui-même estimé.

#### Ce qui fonde ces coefficients

Ils ne sont pas repris d'un manuel : ils sont **calés sur trois couples graine → tempeh** publiés
par des tables nationales, chaque couple provenant d'une seule table pour que les conventions
d'analyse soient les mêmes des deux côtés — USDA 174270→174272, Nouvelle-Zélande X230→X10030,
Norvège. Les fiches sont conservées dans `refs/official/`.

Deux résultats se confirment sur les trois sources :

- **le rapport lipides / protéines ne bouge pas** (0,546→0,532 · 0,514→0,517 · 0,518→0,532, soit
  ±3 %) : protéines et lipides traversent la transformation ensemble, et presque intacts ;
- **les minéraux partent à l'eau** : les cendres ne retiennent que 58 à 75 %.

Une contradiction apparente se résout : la perte de matière sèche semblait osciller de 10 % à 23 %
selon la source. Elle est en réalité **imposée** par l'eau du tempeh et le rendement, qui sont liés.
Trois sources sur quatre donnent un tempeh frais à 59–60 % d'eau ; avec un facteur de rendement de
**1,75**, la perte de matière sèche vaut nécessairement 22 %. Les glucides en
portent l'essentiel.

#### Deux réserves, énoncées ici plutôt que tues

⚠️ **Les acides gras saturés sont probablement sous-estimés.** Les trois couples donnent une
rétention de 128 à 186 %, ce qui est impossible — on ne crée pas d'acide gras saturé. Ces chiffres
sont donc inutilisables. Mais leur **direction** est unanime : la part saturée des lipides augmente
de 4 à 11 points, ce qui s'explique (le mycélium oxyde de préférence les insaturés). Notre modèle
garde ce rapport constant, faute d'une amplitude fiable. C'est le sens défavorable, et c'est assumé
en toute connaissance.

⚠️ **Les fibres sont un majorant.** La frontière entre fibres et glucides est une convention
d'analyse, pas une propriété du produit : la même graine en déclare 9,3 g (USDA, Nouvelle-Zélande)
ou 16,0 g (Norvège). Aucune rétention n'en est tirable, et les fibres sont donc tenues pour
conservées. Toute allégation « source de fibres » devrait s'appuyer sur un dosage, pas sur ce
calcul.

### 3.3 Du lot à l'étiquette

Une étiquette porte une **valeur moyenne** (article 31, paragraphe 4), pas la valeur d'un lot.
La valeur retenue est donc la **moyenne des lots libérés** d'une même recette, et le dossier indique
combien de lots la composent et sur quelle période. `zyfenutri` calcule **un lot** : la moyenne se
fait sur ses résultats, à la charge de qui les conserve.

Plus il y a de lots, plus la moyenne est robuste — et plus l'écart-type observé renseigne sur la
marge réelle face aux tolérances du §2. **En dessous de trois lots, considérer la valeur comme
provisoire.**

---

## 4. Ce qu'il faut pouvoir montrer en cas de contrôle

Le calcul n'est recevable que s'il est **documenté et reproductible**. À conserver :

1. **Les sources de composition**, par ingrédient : soit la fiche technique du fournisseur
   (référence, date, fournisseur), soit la table Ciqual (version, ligne exacte, date de
   consultation).
2. **Les mesures** : masses des intrants et poids récoltés des lots ayant servi à la moyenne,
   datées, et protégées contre une modification après coup.
3. **Les coefficients de perte** appliqués — ceux par défaut ou ceux passés en `coefficients` — et
   l'historique de leurs changements.
4. **Le présent document**, qui explicite la méthode.
5. **La fiche de calcul** (`steps`) rendue par `zyfenutri`, qui déroule la chaîne pour un lot.

À refaire lorsque : la recette change, un **fournisseur change** (la composition varie d'une
origine à l'autre), le procédé change de façon sensible (durée de fermentation, égouttage), ou
qu'assez de lots nouveaux se sont accumulés pour déplacer la moyenne.

---

## 5. Limites assumées

- **Les sucres** sont mal couverts par le calcul : la fermentation en consomme une partie, et
  aucune table ne le reflète. La valeur calculée est un **majorant**. Sur un produit à sucres bas,
  la tolérance absolue (± 2 g) absorbe largement l'écart.
- **Les vitamines B, en particulier la B12**, ne sont pas calculables de façon fiable : le
  *Rhizopus* n'en produit pas, mais les bactéries qui l'accompagnent parfois si.
  **Recommandation : ne pas déclarer la B12 par le calcul.** Elle ne devrait figurer sur une
  étiquette que si un dosage en laboratoire la met en évidence sur un lot représentatif — et ce
  dosage devrait être renouvelé périodiquement. C'est le point le plus sensible commercialement pour un produit
  végétal, et le plus surveillé.
- **Le sel** dépend du procédé, pas des ingrédients : tout sel ajouté doit figurer parmi les
  intrants pour être compté.
- La **teneur en eau du substrat sec** varie (une légumineuse stockée en cave n'est pas celle d'un
  entrepôt sec). L'effet est faible mais il joue dans le même sens que les autres approximations.

**Si une valeur doit être exacte — pour une allégation, ou parce qu'un client la demande —
c'est un dosage en laboratoire, pas un calcul.** Un dosage sur un lot représentatif (de l'ordre de
500 à 1 000 €) permet ensuite de **caler** le modèle : l'écart mesuré entre calcul et dosage
devient un facteur de correction réutilisable tant que le procédé ne change pas.

---

## 6. Sources

**Textes**

- Règlement (UE) n° 1169/2011 (INCO), version consolidée —
  <https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX:02011R1169-20180101>
  *(article 30 : contenu obligatoire ; article 31 § 4 : méthodes d'établissement ; annexe V
  point 19 : exemption ; annexe XIV : coefficients de conversion)*
- Synthèse officielle « Déclaration nutritionnelle » (Your Europe / Commission) —
  <https://europa.eu/youreurope/business/product-requirements/food-labelling/nutrition-declaration/index_fr.htm>

**Tolérances et arrondis**

- Commission européenne, DG Santé et Consommateurs, décembre 2012 — *Guide à l'intention des
  autorités compétentes… fixation de tolérances pour les valeurs nutritionnelles déclarées sur les
  étiquettes* (version française) —
  <https://food.ec.europa.eu/system/files/2021-11/labelling_nutrition-vitamins_minerals-guidance_tolerances_1212_fr.pdf>
  *(tableau 1 : tolérances ; point 6 et tableau 4 : arrondis)*
- Page « Nutrition labelling » de la Commission (point d'entrée, tableau de synthèse) —
  <https://food.ec.europa.eu/food-safety/labelling-and-nutrition/food-information-consumers-legislation/nutrition-labelling_en>

**Données de composition — pour les INGRÉDIENTS**

- **Ciqual** (ANSES), table de référence française — <https://ciqual.anses.fr/>
- USDA FoodData Central, en complément quand Ciqual n'a pas la ligne —
  <https://fdc.nal.usda.gov/>

**Données de composition — pour juger nos estimations de TEMPEH**

Gardées dans `refs/official/`, en **couples graine → tempeh** issus
d'une même table : USDA, Nouvelle-Zélande, Norvège (plus un tempeh suédois sans
contrepartie).

> ⚠️ **La ligne « Tempeh » de Ciqual (20917) n'en fait pas partie, et c'est
> délibéré.** Elle annonce **4,7 g de lipides** là où l'USDA et la
> Nouvelle-Zélande en donnent 10,8 et 9,78 : un tempeh n'étant que du soja
> (~20 g de lipides), en perdre 60 % n'a aucun mécanisme — les lipases
> hydrolysent les graisses, elles ne les font pas disparaître. Elle annonce par
> ailleurs **0,098 g de sel**, vingt fois la graine de départ : ce tempeh-là est
> **salé**, ce que n'est pas un tempeh sans sel ajouté. Ce n'est donc pas le même produit.
>
> ⚠️ **Cela ne disqualifie en rien Ciqual pour les ingrédients**, où elle reste
> la source par défaut (méthode c) : la réserve porte sur **une ligne**, celle
> du produit fini, pas sur la table.

**Guides professionnels**

- Guide ANIA-ACTIA, *Étiquetage nutritionnel en application du règlement (UE) n° 1169/2011* —
  méthodologie détaillée du calcul et du recours au laboratoire.
- DGCCRF, fiche pratique « Déclaration nutritionnelle sur les denrées alimentaires » —
  <https://www.economie.gouv.fr/dgccrf/les-fiches-pratiques/declaration-nutritionnelle-sur-les-denrees-alimentaires>

---

## 7. À faire avant de mettre un chiffre sur un emballage

1. **Décider si l'on déclare**, exemption de l'annexe V point 19 ou pas (§ 1.4). Déclarer
   volontairement, c'est être tenu par toutes les règles ci-dessus.
2. Renseigner la **composition** de chaque intrant — fiche fournisseur ou Ciqual —, avec sa source.
3. Accumuler **au moins trois lots libérés** par recette.
4. Générer la fiche de calcul et la **classer avec le PMS**.
5. Si une allégation est envisagée (« riche en protéines » : ≥ 20 % de l'énergie apportée par les
   protéines) : **dosage en laboratoire**, l'exemption tombe et la tolérance se resserre.


---

## Annexe — Arrondis de l'étiquetage (tableau 4, guide de décembre 2012)

Relevé sur le document source le **2026-09-12**, point 6 « Règles d'arrondi des valeurs pour les denrées alimentaires ». Implémenté dans `zyfenutri/label.py`, fonction `declared()`.

| Élément | Quantité | Arrondi |
|---|---|---|
| Énergie | — | à l'unité de kJ/kcal, sans décimale |
| Matières grasses, glucides, sucres, protéines, fibres, polyols, amidon | ≥ 10 g / 100 g | au gramme |
| | < 10 g et > 0,5 g | au décigramme |
| | indétectable ou ≤ 0,5 g | « 0 g » ou « < 0,5 g » |
| Acides gras saturés, mono-insaturés, polyinsaturés | ≥ 10 g / 100 g | au gramme |
| | < 10 g et > 0,1 g | au décigramme |
| | indétectable ou ≤ 0,1 g | « 0 g » ou « < 0,1 g » |
| Sodium | ≥ 1 g / 100 g | au décigramme |
| | < 1 g et > 0,005 g | au centigramme |
| | indétectable ou ≤ 0,005 g | « 0 g » ou « < 0,005 g » |
| **Sel** | ≥ 1 g / 100 g | au décigramme |
| | < 1 g et > 0,0125 g | au centigramme |
| | indétectable ou ≤ 0,0125 g | « 0 g » ou « < 0,01 g » |
| Vitamines et minéraux | vit. A, acide folique, chlorure, calcium, phosphore, magnésium, iode, potassium | 3 chiffres significatifs |
| | tous les autres | 2 chiffres significatifs |

### Le cas du sel

`sel = sodium × 2,5` (annexe I, point 11 du règlement INCO). Le sodium étant **naturellement présent** dans les légumineuses, les céréales et l'eau, le sel d'un tempeh sans sel ajouté n'est **jamais nul** — le déclarer à « 0 g » serait faux.

`zyfenutri` applique le tableau tel quel : **« < 0,01 g »** jusqu'à 0,0125 g (`SALT_NEGLIGIBLE_G`, `SALT_DECLARED_MENTION`), une valeur au centigramme au-delà, au décigramme à partir de 1 g. Jamais « 0 g ».

Un exploitant peut préférer imprimer **« < 0,1 g »** en dessous de 0,1 g. Ce choix est défendable, pour trois raisons :

1. la mention reste **vraie** : elle majore la valeur réelle, elle ne la sous-déclare pas ;
2. elle n'affiche pas une précision au **centigramme** qu'une valeur *calculée* — et non dosée — ne mérite pas ;
3. la tolérance du sel sous 1,25 g/100 g est de **± 0,375 g** (§ 2) : l'écart entre « < 0,01 » et « < 0,1 » est sans aucune conséquence au contrôle.

Le guide de la Commission **n'a pas de valeur juridique** — il le dit lui-même. Ce choix reste pourtant celui de l'exploitant, pas du calcul : `label` rend la mention du tableau 4. Et il cesse de valoir dès qu'une recette comporte du sel ajouté, car la valeur n'est alors plus négligeable.


---

## Ce que cette méthode ne sait pas faire

Une méthode qui tait ses faiblesses se défend mal. Celles-ci sont connues, assumées, et n'empêchent pas la déclaration — elles disent seulement jusqu'où le chiffre engage.

**1. Le calcul n'est pas validé contre un dosage.** Il est reproductible et documenté ; cela ne prouve pas qu'il soit juste. C'est la limite qui domine toutes les autres, et la seule qui se lève simplement : quelques analyses de laboratoire (`refs/analyses/`) suffisent à mesurer l'écart réel.

**2. La précision affichée est supérieure à la précision réelle.** Chaque étage apporte son incertitude — la composition de l'intrant, les pesées, les coefficients de perte — et rien ne les cumule. Les arrondis réglementaires en masquent une partie, ils ne la suppriment pas.

**3. Les coefficients de perte sont les mêmes pour tous les substrats.** Le soja et le pois chiche ne se comportent pas identiquement au trempage, ni à la fermentation. Sept constantes globales, donc une approximation assumée.

**4. La composition d'un intrant est supposée constante.** Une légumineuse varie de 10 à 15 % en protéines selon l'année et l'origine. La fiche produit fige une valeur ; la réalité bouge sous elle. C'est précisément pourquoi la réglementation parle de **valeurs moyennes** et prévoit des tolérances larges.

**5. Les pertes ne dépendent pas du procédé.** Durée de trempage, volume d'eau, température d'incubation changent réellement ce qui s'en va — le calcul applique pourtant les mêmes pourcentages à tous les lots.

**6. Une seule pesée porte tout.** Les valeurs pour 100 g s'obtiennent en divisant par le poids récolté : une erreur de balance à la récolte se propage intégralement aux neuf valeurs, et rien d'autre ne vient la contredire.

**7. La cohérence d'une fiche produit n'est pas vérifiée.** Le contrôle habituel — macros + eau + cendres ≈ 100 g — demande l'humidité et les cendres, que le calcul ne reçoit pas. `zyfenutri.check()` sait refuser une fiche physiquement impossible (valeur négative, « dont » supérieur à son total, macros au-delà de 102 g), mais `compute()` ne l'applique pas aux intrants : une fiche fournisseur erronée passerait donc sans alerte.

> Aucune de ces limites n'interdit de déclarer : l'article 31 § 4 admet le calcul, et les tolérances (§ 2) sont conçues pour absorber cette variabilité. Elles fixent en revanche l'ordre des priorités — **faire doser un lot** est ce qui ferait le plus progresser la fiabilité, loin devant tout raffinement du modèle.
