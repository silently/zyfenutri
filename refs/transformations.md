# Les transformations — état des connaissances

Document **de travail**. Pour chaque transformation, il consigne ce qu'on sait,
d'où on le tient, et ce qui contredit le modèle actuel. Il s'enrichit à chaque
lecture. Quand une règle est stabilisée, elle passe dans
[`methode.md`](methode.md), qui est le document présenté à un contrôle.

Les sources sont numérotées dans [`references.md`](references.md).

**L'objectif :** trouver dans la littérature **tous** les coefficients de toutes
les transformations. Ceux qui manquent à la fin sont calés sur les couples
graine → tempeh de `official/`, dans les limites fixées par `methode.md`
(§ 3.2, « D'où vient chaque coefficient »). Ce qui reste est une hypothèse,
marquée comme telle.

---

## 0. État du modèle dans le code

Après lecture de [12] et [19], toutes les transformations ont un
coefficient pour chaque nutriment. Chacun est commenté dans
`zyfenutri/transforms.py` avec sa source, ou marqué `HYPOTHESIS`.

| Transformation | Ce qui est sourcé | Ce qui reste hypothèse | Lacune (`None`) |
|---|---|---|---|
| **Dépelliculage** — sans réglage ; sa perte de **masse** est dans le facteur de rendement | pellicule à 9 % de la graine [1, p. 60], [12, p. 189], à 8,8 % de protéines, 1 % de lipides, 4,3 % de cendres [12, p. 188] ; moitié des fibres [1, p. 60] | sodium comme les cendres ; mêmes proportions pour d'autres graines | germe |
| **Trempage** — **toujours une nuit, 10 à 15 h** | sucres −27 % (saccharose, 25 °C [14]) ; protéines −3 % [14] ; minéraux −5 %, au rythme des solides ([14], [13]) | lipides −1,2 % (moitié des −2,5 % à 24 h [12, p. 193]) ; azote non protéique ≈ moitié de l'azote perdu ; fibres et amidon conservés ; sodium comme les cendres | température ; acidification |
| **Cuisson** | sucres −44 % (reste des −59 % de Shallenberger [12], après le trempage de [14]) ; protéines ~8 % ([12], [15]) ; minéraux −2 % ([15]) | fibres et amidon conservés ; τ = 20 min | — |
| **Fermentation** | **lipides −12 % de 26 à 60 h, −59 % à 120 h, −67 % à 180 h** [16] ; part saturée des lipides +7,9 points, **calée sur `official/`** ; protéines 1-4 % ([16], [9]) ; minéraux conservés [16] ; sucres −17 % à 48 h [12, p. 194] ; amidon −31 % à 37,5 h, −39 % à 48 h ([15], borne haute) | fibres conservées (elles montent en général [12], [15]) ; formes linéaires entre les points | sucres et amidon au-delà de 48 h ; protéines au-delà de 72 h ; lipides au-delà de 180 h ; température |
| **Torréfaction** — oui ou non, sans intensité | fibres −16 % en matière sèche [19] ; sucres −8 %, **calés sur `official/`** (soja → kinako, MEXT) ; amidon, protéines, lipides, cendres inchangés en matière sèche ([13], [19]) | seule l'eau part (volatils négligés) ; une torréfaction forte traitée comme celle à 120 °C de [19] | — |

**Contrôle de cohérence, pas une validation.** Graine néo-zélandaise, 12 h de
trempage, 30 min de cuisson, 36 h de fermentation, 1000 g → 1750 g de
tempeh ; les valeurs de la table pour le tempeh sont entre parenthèses :

| | lipides | glucides | sucres | fibres | protéines |
|---|---|---|---|---|---|
| calcul | 9,3 | 2,3 | 1,3 | 5,3 | 18,6 |
| tempeh NZ | (9,8) | (2,4) | (2,2) | (7,7) | (18,9) |

⚠️ Ce n'est **pas** une validation : le coefficient de l'amidon s'appuie en
partie sur ce même couple, et le procédé du tempeh de la table est inconnu.
Seule une analyse de laboratoire validera.

## 0 bis. Ce qu'il reste à faire

### ⭐ Les trois publications à obtenir en priorité

Les trois précédentes sont lues : Ruiz-Terán & Owens 1996 [16], Wang et al. 1979
[14], Erkan et al. 2020 [17].

| | Publication | Ce qu'elle débloque |
|---|---|---|
| **1** | **[4] Wang N., Hatcher D. W., Toews R., Gawalko E. J. (2009).** Influence of cooking and dehulling on nutritional composition of several varieties of lentils (*Lens culinaris*). *LWT* 42, 842-848. <https://doi.org/10.1016/j.lwt.2008.10.007> | La **lentille**, substrat visé, n'a aucune donnée de composition avant et après transformation : [17] ne donne que des tempehs finis, en extraits aqueux. Celle-ci mesure dépelliculage et cuisson de lentilles. |
| **2** | **Robinson R. J., Kao C. (1977).** Tempeh and miso from chickpea, horse bean and soybean. *Cereal Chemistry* 54, 1192-1197. | Composition de tempehs de **pois chiche, féverole et soja**, citée par [15] : un second bilan hors soja, pour recouper [15], dont le protocole (graines concassées, trempage chaud) perd beaucoup de lipides. Les archives anciennes de *Cereal Chemistry* sont peut-être en accès libre. |
| **3** | **Smith A. K., Rackis J. J., Hesseltine C. W., Robbins D. J., Booth A. N. (1964).** Tempeh: nutritive value in relation to processing. *Cereal Chemistry* 41, 173. | Les pertes d'azote et de solides **étape par étape**, que [12] ne reprend qu'en résumé : de quoi séparer vraiment protéines au trempage et à la cuisson (aujourd'hui −3 % et −8 %, par différence). Même archive. |

**Torréfaction** : elle a désormais un effet chiffré (§ 6) — sucres −8 %,
calés sur les couples soja → kinako de la table japonaise, et fibres −16 %
[19]. Reste à trouver une mesure sur **un même lot** de soja sec, cru puis
torréfié fort.

### À affiner — une valeur existe, mais elle est fragile

| Point | Aujourd'hui | Pourquoi c'est fragile |
|---|---|---|
| Protéines à la cuisson | −8 % | déduit par différence : total 14 % [12] moins pellicule, trempage [14] et fermentation [16] ; l'**acidification**, qui limite les pertes [1, p. 74], n'est pas prise en compte |
| ⚠️ **Lipides** | −1,2 % au trempage, −12 % à la fermentation (source primaire [16]) | la fermentation est désormais solide ; l'écart restant est avec [15], qui mesure 47 à 70 % de pertes après 24 h de trempage à 30 °C sur graines concassées : le modèle ne vaut que pour un trempage d'une nuit à température ambiante |
| Sucres au trempage | −27 %, saccharose mesuré [14] | une seule variété, à 25 °C ; une part des sucres est hydrolysée par les enzymes de la graine, pas lessivée [14, p. 1512] |
| Sucres à la cuisson | −44 % | déduit de deux études différentes (Shallenberger dans [12], et [14]) |
| Amidon à la fermentation | −75 % à 48 h | deux données secondaires, forme linéaire supposée |
| Minéraux | −5 % au trempage, −2 % à la cuisson | [15] mesure 92-98 % des cendres conservées ; les couples de `official/` suggèrent 58-75 % : les deux ne concordent pas ; sodium supposé suivre les cendres |
| Fibres | conservées au trempage, à la cuisson et à la fermentation | dépend de la méthode de la table (oligosaccharides comptés ou non) ; les fibres brutes gagnent 15 à 31 % de la graine au tempeh [15] : le modèle sous-déclare |
| Pellicule | moitié des fibres ; protéines et lipides de Cowan 1969 | composition d'une seule étude ; proportionnalité à la part de pellicule supposée |
| AGS | part saturée +7,9 points à la fermentation | calé sur trois couples dispersés (+3,8 à +10,8) ; implique plus d'AGS en masse qu'au départ, sans source sur la synthèse par le mycélium ; [2] trouve l'inverse en laboratoire |
| Formes dans le temps | lignes droites, τ de 20 min pour la cuisson | hypothèses de forme, pas de cinétique mesurée hors [3] |
| Validation | contrôle de cohérence avec le couple NZ | **aucune analyse de laboratoire** : rien n'est validé |
| `methode.md` § 3.2 | décrit un ancien modèle | à réécrire avant toute étiquette |

### Manque complètement — aucune valeur

- **Substrats autres que le soja** : les coefficients viennent du soja. [15]
  montre que les fractions se comportent de la même façon sur soja, pois
  chiche, pois et féverole (§ 0 ter), mais il n'y a **aucune donnée pour la
  lentille, les céréales ni les oléagineux**, et [3] montre que le plafond de
  perte au trempage varie de 16 à 70 % selon la graine.
- **Torréfaction forte, sur un même lot.** Les sucres sont calés sur deux
  lots japonais différents (graine et kinako), les fibres sur une
  torréfaction douce de quinoa [19]. Une mesure crue puis torréfiée d'un même
  soja sec, à la température d'un kinako, confirmerait les deux. Poids
  réel : quelques grammes par lot, l'effet sur l'étiquette reste faible.
- **Au-delà des durées connues** : fermentation de plus de 48 h (72 h pour les
  protéines). Le trempage, lui, est toujours d'une nuit (10 à 15 h).
- **La température** du trempage et de la fermentation : premier facteur selon
  [14] et [2], ce n'est pas un réglage.
- **L'acidification** du trempage ou de la cuisson.
- **Le mode de cuisson** : vapeur, ou absorption sans eau jetée.
- **La perte du germe** au dépelliculage (3 % du soja [1, p. 60]).
- **La souche** de *Rhizopus* : elle change la consommation des sucres
  [10, p. 1728].
- **Les bornes Codex** (protéines ≥ 15 %, lipides ≥ 7 %…) comme avertissements
  dans `compute()`.

## 0 quater. Les substrats visés, et ce qui ne tient pas encore pour eux

Substrats prévus : **soja, orge, lentilles, pois chiche, pois cassés**. Presque
tous les coefficients viennent du soja, qui a peu d'amidon et une pellicule de
9 %.

| Transformation | Tient hors soja ? |
|---|---|
| Dépelliculage | ⚠️ **propre au soja** : 9 % de pellicule et composition de Cowan 1969. La pellicule du pois chiche, de la lentille ou de l'orge n'est pas la même. Les pois cassés sont vendus dépelliculés : ne pas l'appliquer. |
| Trempage | en partie : raisonne par fractions, mais [3] montre un plafond de perte de 16 à 70 % selon la graine |
| Cuisson | inconnu hors soja ; la lentille cuit 1 min chez [17], là où τ = 20 min |
| Fermentation — amidon | **recalé sur trois légumineuses amylacées** [15] (voir ci-dessous) |
| Torréfaction | sans objet pour les substrats |

**L'amidon à la fermentation — recalé.** L'ancien coefficient (−75 % à 48 h)
venait d'un soja presque sans amidon et d'une féverole citée de seconde main
[8]. Sur une légumineuse amylacée, il ne laissait que ~44 % des glucides de la
graine au tempeh, contre 62-76 % d'extrait non azoté conservé mesurés par
[15]. Le coefficient est maintenant calé sur [15] : **−31 % d'amidon à 37,5 h,
−39 % à 48 h** (prolongé en ligne droite). Les pois cassés, pois chiches et
lentilles gardent ~69 % de leurs glucides (trempage, cuisson 30 min,
fermentation 36 h).

- **C'est une borne haute de la perte** : tout l'extrait non azoté perdu est
  attribué à l'amidon de la fermentation, alors qu'une partie part à l'eau.
- **Le soja n'y perd presque rien** : son amidon est faible. Contrôle sur les
  couples officiels : glucides NZ 3,0 g (table 2,4), Norvège 3,2 g (table 5,5,
  encore 0,2 g hors tolérance).
- **La taille de la graine n'est pas un réglage** : [3] donne le même rythme
  de fuite au trempage pour des graines de tailles très différentes, et aucune
  source lue ne mesure l'effet du calibre à la cuisson.

**La souche.** La fermentation est calée sur ***R. oligosporus*** (celle de [15]
et [16], et celle utilisée en pratique). Avec *R. oryzae*, les acides gras
baissent nettement plus au-delà de ~40 h à 30 °C : à 46 h, ~−34 % en teneur
contre ~−6 % pour *R. oligosporus* [2, tableau 1]. Non modélisé.

**L'orge** n'a aucune donnée : pellicule (orge vêtue ou perlée), trempage,
cuisson, fermentation d'une céréale.

---

## 0 ter. Quatre légumineuses, un même comportement [15]

Poids [tableau 1, p. 73] × matière sèche × teneur [tableau 2, p. 76] donne la
part **conservée en masse**, de la graine dépelliculée crue au tempeh (calcul
fait ici). Protocole : graines concassées, trempage 24 h à 30 °C, cuisson dans
l'eau de trempage, fermentation 35-40 h à 30 °C, sans acidification.

| | rendement | matière sèche | protéines | lipides | fibres brutes | cendres | extrait non azoté |
|---|---|---|---|---|---|---|---|
| soja | 2,00 | 73 % | 81 % | 53 % | 116 % | 93 % | 68 % |
| pois chiche | 1,72 | 72 % | 77 % | 48 % | 115 % | 98 % | 70 % |
| pois | 1,82 | 80 % | 91 % | 50 % | 131 % | 97 % | 76 % |
| féverole | 1,76 | 78 % | 82 % | 30 % | 125 % | 92 % | 62 % |

**Ce que ça établit.** Pour une même fraction, le comportement est le même d'une
graine à l'autre : protéines ~80 %, cendres ~95 %, extrait non azoté ~70 %,
fibres en hausse. C'est l'argument le plus fort, à ce jour, pour des
transformations qui raisonnent **par fraction et non par espèce**. Seuls les
lipides varient beaucoup (30 à 53 %), et d'autant plus que la graine en
contient peu.

**Ce que ça ne permet pas.** Isoler une étape : le tableau ne donne que la
graine crue et le tempeh. Et ce protocole (graines concassées, trempage long
et chaud) perd plus qu'un trempage d'une nuit de graines entières.

---

Les sections suivantes gardent le raisonnement source par source, dans
l'ordre des lectures : certains « à combler » y sont désormais comblés.

---

## 1. La liste retenue

| Transformation | Substrats concernés | Réglages envisagés |
|---|---|---|
| **Dépelliculage** | légumineuses, certains oléagineux | voie sèche ou humide ; part de pellicule |
| **Trempage** | légumineuses, certaines céréales | **toujours une nuit, 10 à 15 h** ; température, acidifié ou non, graine entière, fendue ou concassée |
| **Cuisson** | tous | durée ; eau jetée, vapeur ou absorption |
| **Fermentation** | tous | durée, température |
| **Torréfaction** | supports : farines, kinako | aucun : oui ou non |

**Elle suffit** pour les sept valeurs déclarées. Les autres opérations d'un
atelier ne changent aucune masse de nutriment, ou sont déjà prises en compte
ailleurs :

| Opération | Pourquoi ce n'est pas une transformation |
|---|---|
| **Rinçage** après trempage | déjà compté : les coefficients du trempage sont mesurés DANS l'eau, ils supposent qu'on la retire en entier (`methode.md`, § 3.2) |
| **Égouttage** après cuisson | déjà compté : les coefficients de cuisson viennent de bilans graine → tempeh, qui l'englobent |
| Séchage superficiel, refroidissement | de l'eau seulement : le facteur de rendement s'en charge |
| Pasteurisation | ne déplace aucune masse de nutriment (`methode.md`, T4) |
| Vinaigre ajouté à l'inoculation | un ingrédient du **mélange** |
| Vinaigre du trempage ou de la cuisson | part avec l'eau jetée : c'est un **réglage** du trempage ou de la cuisson, pas un ingrédient |
| Concassage | un **réglage** du trempage : il multiplie les pertes (§ 2) |
| Pré-fermentation lactique au trempage | un **réglage** du trempage : elle consomme des sucres (§ 5) |

⚠️ **Le germe.** Chez le soja, le germe (hypocotyle) pèse 3 % de la graine et
se perd souvent au dépelliculage [1, p. 60]. Sa perte est une perte de masse
de composition à peu près moyenne : elle relève du **dépelliculage**, pas
d'une transformation à part.

---

## 2. Une seule transformation pour le soja et la lentille ?

**Oui pour la forme, à une condition : raisonner sur ce qui se dissout, pas sur
l'espèce.**

Les pertes au trempage et à la cuisson sont celles du **soluble** : sucres
simples, minéraux, une fraction des protéines. L'amidon, les lipides et les
fibres insolubles restent dans la graine. C'est l'hypothèse de travail. [5]
irait dans ce sens, d'après ce qu'en rapporte un moteur de recherche : en % de
matière sèche, la cuisson du haricot et du pois chiche ferait monter les
protéines, l'amidon et les fibres, et baisser les cendres et les sucres.
**À vérifier en lisant [5].**

Or le soja et la lentille ne rangent pas leurs glucides au même endroit :

| | Soja | Lentille, pois chiche |
|---|---|---|
| Glucides assimilables | **peu**, surtout du saccharose | **beaucoup**, surtout de l'amidon |
| Ce qui part à l'eau | une grande part des glucides | une petite part des glucides |

⚠️ **Le coefficient actuel, `leaching_carbs` = −50 % des glucides, ne peut donc
valoir que pour le soja.** Appliqué à une lentille, il ferait fondre la moitié
de son amidon, ce qu'aucun mécanisme n'explique.

**La piste :** la fiche distingue déjà `sugars` de `carbs`. On en déduit
`amidon ≈ carbs − sugars`, et le trempage applique
- une perte **forte** aux sucres ;
- une perte **nulle ou faible** à l'amidon ;
- puis recompose `carbs = amidon restant + sucres restants`.

Écrite ainsi, la même transformation donne une grosse perte de glucides sur le
soja et une petite sur la lentille, **sans connaître l'espèce** : c'est la
fiche de l'ingrédient qui porte la différence. Cette transformation n'est plus
une simple `Retention` (un facteur par nutriment) : elle implémente directement
le protocole `Transform`, comme le dépelliculage.

**État :** implémentée dans `transforms.Soaking()`, **pour une nuit (10 à
15 h)** : le trempage n'est pas un réglage. L'état chiffré est au § 0 ; le
tableau ci-dessous garde la cinétique de [3] qui a servi à fixer les sucres.

**Ce que [3] établit pour le trempage** (graines entières, 22 °C, raffinose,
3 h puis 12 h) :

| Légumineuse | Perte à 3 h | à 12 h | Perte max ajustée | τ ajusté |
|---|---|---|---|---|
| soja | 33 % | 56 % | 58 % | 3,5 h |
| pois chiche | 42 % | 68 % | 70 % | 3,3 h |
| lentille Pardina | 15 % | 26 % | 27 % | 3,7 h |
| lentille Crimson | 32 % | 57 % | 60 % | 3,8 h |
| pois jaune | 10 % | 15 % | 16 % | 3,1 h |
| pois vert | 20 % | 76 % | — | pas de plateau |

Pertes calculées sur [3, tableau II, p. 431] ; ajustement de
`perte(t) = perte_max × (1 − e^(−t/τ))` par deux points, fait ici.

1. **La forme saturante tient** sur 5 légumineuses sur 6.
2. **Le rythme se transpose d'une graine à l'autre, le plafond non.** τ reste
   entre 3,1 et 3,8 h, mais la perte maximale va de 16 à 70 %, et fait plus que
   doubler entre deux variétés de lentille. Une transformation commune porte
   donc bien la durée ; **le plafond dépend de la graine**, et c'est une
   limite réelle de l'objectif « une transformation pour tous ». La piste :
   c'est surtout la pellicule qui freine, et un substrat de tempeh est en
   général dépelliculé et fendu. À vérifier.
3. **Le pois vert ne suit pas la courbe** : il perd peu à 3 h et beaucoup à
   12 h, comme si l'eau devait d'abord traverser la pellicule.

⚠️ **Les réserves sur ces chiffres :**
- [3] exprime les teneurs en mg/g de graine **séchée après trempage** ; la
  matière sèche perdue au trempage n'est pas corrigée. Les pertes réelles, en
  masse absolue, sont un peu **plus fortes** que celles-ci.
- **Graines entières, non dépelliculées**, à **22 °C** : un substrat fendu, ou
  un trempage chaud, perd sans doute plus vite.
- **Le raffinose n'est pas une valeur déclarée** : il sert d'indicateur de la
  vitesse à laquelle un petit sucre soluble quitte la graine.

⚠️ **Les oligosaccharides.** Ils pèsent lourd : 70,7 à 144,9 mg/g dans les
légumineuses crues, 95,1 mg/g dans le soja [3, tableau I, p. 429], et le trempage
en retire jusqu'à 56 % dans le soja et 75 % dans le pois chiche en 12 h
[3, p. 430]. Au sens du règlement INCO, ce ne sont **pas des sucres**
(mono- et disaccharides seulement), ni des glucides assimilables.

En revanche, la définition des **fibres** de l'annexe I, point 12, couvre les
polymères glucidiques d'au moins trois unités ni digérés ni absorbés :
raffinose (3) et stachyose (4) en relèvent. **Qu'ils figurent ou non dans la
valeur « fibres » d'une fiche dépend de la méthode d'analyse** de la table.

Deux conséquences :
- l'ancienne version de `methode.md` justifiait −50 % de **glucides** par la
  solubilité des oligosaccharides : c'est corrigé, le trempage (T2a) ne retire
  plus que des sucres mesurés, saccharose et fructose [14] ;
- **si la fiche compte les oligosaccharides dans ses fibres, le trempage fait
  perdre des fibres**, que le modèle tient pour conservées. **Piste à
  vérifier :** c'est peut-être ce qui sépare les 9,3 g de fibres de la graine
  USDA des 16,0 g de la graine norvégienne (`methode.md`, § 3.2).

**Ce qui reste propre à la graine**, et qu'un réglage devra porter : la
**surface d'échange**. Une graine entière, fendue ou concassée ne perd pas au
même rythme. Chez le soja, des grits perdent 43 % des solides contre 27 % pour
des graines entières [1, p. 80, citant Smith et al. 1964].

---

## 3. Dépelliculage

**Ce qu'on sait**

- **La pellicule du soja :** 8 à 10 % du poids de la graine, et la moitié de
  ses fibres [1, p. 60]. Le germe fait 3 %, les cotylédons 87 à 89 % [1, p. 60].
- **La perte de solides :** environ 8 % à sec, 9,6 % par voie humide
  [1, p. 72, citant Steinkraus 1964].

**Ce que ça dit du modèle actuel**

- `hull_fibre = 85 %` suppose une pellicule composée à 85 % de fibres. Avec
  une pellicule de 9 % qui porte la moitié des fibres de la graine, on obtient
  un chiffre du même ordre si les fibres de la graine sont des **fibres
  alimentaires** ; il serait bien plus bas en **fibres brutes**, la méthode de
  1980. [1] ne précise pas laquelle : **non vérifiable avec [1] seul**.
- **La perte du germe n'est pas modélisée.**
- **À lire :** [4], pour la lentille.

---

## 4. Trempage et cuisson

Deux transformations distinctes, parce que les réglages le sont : on peut
cuire sans tremper (grains concassés), tremper à chaud, cuire à la vapeur.

**Ce qu'on sait**

- **Soja dépelliculé, trempé puis cuit 120 min à 100 °C :** 12,2 % des solides
  perdus [1, p. 80, citant Steinkraus 1964].
- **Durée de cuisson :** 40 à 60 min en général, 45 min en moyenne dans les
  ateliers américains [1, p. 75]. De 15 min à 2 h, le tempeh reste
  satisfaisant [1, p. 75, citant Steinkraus et al. 1965].
- **L'acidification** réduit les pertes de protéines dans l'eau de cuisson
  [1, p. 74].
- **La vapeur** réduit les pertes de nutriments et de solides par rapport à
  l'ébullition [1, p. 72 et 75].
- **Poids, pour 1 livre de soja entier** [1, p. 80, citant Steinkraus et al. 1961] :

  | Étape | Poids |
  |---|---|
  | trempé | 2,33 livres |
  | dépelliculé | 2,02 livres |
  | cuit | 1,90 livre |
  | tempeh | 1,74 livre |

**Ce que ça dit du modèle actuel**

- ⚠️ **Les protéines.** Le modèle perd **3 %** des protéines au
  trempage-cuisson et **0 %** à la fermentation. Smith et al. (1964) mesurent
  **19,7 %** de pertes d'azote sur tout le procédé, graines entières
  dépelliculées à la main [1, p. 80]. Une part tient au germe et aux débris
  perdus au dépelliculage, une autre à l'ammoniac dégagé pendant la
  fermentation. Mais l'écart est trop grand pour être ignoré : **c'est le
  premier point à éclaircir**, parce que les protéines ont la tolérance la plus
  serrée (± 20 %) et sont le nutriment qu'un contrôle dose en premier.
- ⚠️ **Les glucides :** voir § 2.
- **La durée :** la forme saturante est étayée par [3] pour le trempage (§ 2).
- **L'eau prise au trempage** (graines entières, 22 °C), qui intéresse le
  facteur de rendement et non les transformations : à saturation en 12 h,
  +125 % pour le soja, +108 % pour le pois chiche, +102 à +103 % pour les pois ;
  la lentille Crimson sature dès 6 h à +119 % [3, p. 430]. Pour le soja, c'est
  cohérent avec les 2,33 livres trempées par livre sèche de [1, p. 80].
- **La cuisson n'est pas monotone.** Cuire 30 min des graines non trempées
  **augmente** la teneur mesurée en oligosaccharides, sauf pour la lentille
  Crimson [3, p. 431]. Les auteurs l'attribuent à des oligosaccharides liés,
  libérés par la chaleur, et à la fuite d'autres solubles (sucres, protéines,
  fibres solubles). Après trempage, la cuisson retire encore 32 à 61 % chez la
  lentille, mais pas chez le soja (+12 à +29 %) [3, p. 431]. **Une
  transformation « cuisson » calquée sur le trempage serait donc fausse** ;
  il faut une source qui mesure les sucres et les minéraux, pas les seuls
  oligosaccharides : [4], [5].

---

## 5. Fermentation

**Ce qu'on sait**

- **Les lipides : la perte dépend surtout de la température et de la durée**
  [2, p. 172-174]. Avec *R. oligosporus* à 30 °C, les acides gras totaux
  oscillent pendant la croissance active, de 22,4 % de la matière sèche à 0 h
  à 25,0 % à 28 h [2, tableau 1, p. 173], puis baissent. À 37 °C, les auteurs
  mesurent une perte de 54 % du niveau initial après 69 h [2, p. 173].
- **Le moment où ça bascule :** le champignon puise dans les lipides **après**
  sa phase de croissance active, vers 20-30 h [2, p. 175], et d'autant plus que
  les glucides fermentescibles ont été épuisés en amont, par exemple par une
  acidification lactique au trempage [2, p. 174].
- **Les solides :** 1,7 % perdus à la fermentation
  [1, p. 80, citant Steinkraus 1964]. Les sources plus récentes donnent
  **environ 10 %** : Van der Riet et al. 1987, cités dans [6, p. 2238] ; 10 %
  pendant la croissance du mycélium (0-32 h), selon Ruiz-Teran & Owens 1996,
  cités dans [9, p. 797].
- **Le bilan de matière le plus complet** (Ruiz-Teran & Owens 1996, cités dans
  [9, p. 797]), en % de la matière sèche **initiale** :

  | Phase | Matière sèche perdue | dont lipides | dont protéines | dont non identifié |
  |---|---|---|---|---|
  | croissance, 0-32 h | 10 % | 3 % | 0,5 % | 6,5 % |
  | sénescence, 60-180 h | 12 % | presque tout | — | — |

- **Les protéines : l'hydrolyse n'est pas une perte.** Pour l'étiquette, les
  protéines se calculent à partir de l'azote, et l'effet de la fermentation sur
  l'azote total est « négligeable » (Nowak & Szebiotko 1992, cités dans
  [6, p. 2235] ; Winarno & Reddy 1986, cités dans [8, p. 624]). À 46 h, 25 % des
  protéines sont hydrolysées : environ 65 % restent dans le tempeh en acides
  aminés et peptides, 25 % passent dans le mycélium, **10 % sont oxydés**
  [9, p. 797]. L'oxydation, estimée d'après l'ammoniac, vaut 5 g à 28 h, 10 g à
  46 h et 20 g à 72 h par kg de cotylédons secs [9, p. 797]. Rapporté à des
  protéines à 45 % de la matière sèche [6, tableau 2], cela fait **environ
  1 % à 28 h, 2 % à 46 h, 4 % à 72 h** (calcul fait ici).
- **Les lipides pendant la croissance :** −3 % de la matière sèche initiale en
  32 h (Ruiz-Teran & Owens, cités dans [9, p. 797]). Avec des lipides autour de
  25 % de la matière sèche ([2], [7]), cela représente **environ 12 % des
  lipides** (calcul fait ici).
- **Les lipases coupent peu jusqu'au bout :** presque pas de glycérol libre ;
  les triglycérides deviennent surtout des glycérides partiels [9, p. 797].
  L'hydrolyse seule ne fait donc presque rien perdre à la valeur « matières
  grasses ».
- **Les lipides selon la température du lit** [7, tableau 1, p. 208], en % de
  matière sèche, *R. oligosporus* : de 28,1 à 25,0 % en 72 h dans un lit à
  25 °C ; stables (28,2 → 28,7 %) dans un lit à 30 °C.
- **L'amidon est consommé quand il y en a :** dans le soja, il passe de 0,4 à
  0,1 % de la matière sèche en 48-72 h ; dans un tempeh de féverole, il baisse
  de 74 % (études citées dans [8, p. 624-625]). Pour une céréale ou une
  légumineuse riche en amidon, la fermentation doit donc consommer de
  l'amidon, pas seulement des sucres.
- **Les oligosaccharides** partent surtout au trempage et à la cuisson
  [9, p. 797]. Plusieurs souches de *Rhizopus* ne savent pas s'en nourrir
  comme seule source de carbone (Graffham et al. 1995, cités dans [9, p. 795]).
- **Une troisième lecture de Ruiz-Terán & Owens (1996)** départage peut-être
  [9] et [10] : comparé au soja dépelliculé non fermenté, le tempeh montre
  « une légère baisse des lipides », principale cause de la baisse de matière
  sèche, « une légère hausse des glucides », et **pas de différence
  significative** en protéines et en cendres (Murata et al. 1967 et Ruiz-Terán
  & Owens 1996, cités dans [11, p. 268-269]). « Légère » va dans le sens des
  3 % de matière sèche de [9] plutôt que des 30 % des lipides de [10]. Ce n'est
  **pas un chiffre**, et la base (% de matière sèche ?) n'est pas dite : la
  lacune reste ouverte.
- **À 37 °C** (Steinkraus et al. 1960, cités dans [11, p. 268]) : germination
  des spores pendant les 20 premières heures, croissance rapide pendant les
  5 heures suivantes, avec une température du produit qui monte jusqu'à
  43-44 °C ; au-delà, sporulation et ammoniac. Le pH monte de 5,0 à 7,6 ;
  l'optimum pour un bon tempeh est à 6,3-6,5.
- **Le tempeh frais**, en matière sèche : 48,1 % de protéines, 24,7 % de
  lipides, 23,9 % de glucides, 3,3 % de cendres, composition « similaire au
  soja dépelliculé cuit » (Wang 1986, cité dans [11, p. 273]). ⚠️ Une
  composition de tempeh seule ne cale aucun coefficient.
- **État dans le code — lipides à la fermentation : environ 11 % perdus de
  32 à 48 h, vers 30 °C** (`FERMENTATION_FAT_LOST`). Trois lectures
  concordent :

  | Lecture | Calcul | Lipides perdus |
  |---|---|---|
  | 3 % de la matière sèche initiale à 32 h [9, p. 797] | ÷ lipides à 28,1 % de la matière sèche [7, tableau 1] | 11 % à 32 h |
  | lipides en % de matière sèche, 28,2 → 29,1 à 48 h [7, tableau 1] | × (1 − 10 % de matière sèche perdue [6, p. 2238]) | 7 % à 48 h |
  | acides gras en % de matière sèche, 22,4 → 21,0 à 46 h, 30 °C [2, tableau 1] | idem | 16 % à 46 h |

  [11, p. 268-269] parle d'une « légère baisse ». Les 30 % de [10, p. 1733],
  seuls contre trois, sont écartés jusqu'à lecture de la source primaire.
  **Hypothèses :** perte linéaire jusqu'à 32 h, AGS qui suivent les lipides,
  10 % de matière sèche perdue. **Lacune :** au-delà de 48 h, la sénescence
  brûle vite les lipides [9, p. 797]. Les deux lectures à 46-48 h (7 % et
  16 %) donnent l'ordre de l'incertitude, **± 5 points** : sur un tempeh autour
  de 10 g de lipides pour 100 g, environ ± 0,5 g, bien moins que la tolérance
  d'étiquette (± 1,5 g sous 10 g, ± 20 % au-delà).
- **Les réglages usuels** [10, p. 1721-1722] : cuisson de 20 à 30 min ;
  incubation à 25-38 °C pendant 18 à 72 h. Phases à 30-32 °C : croissance
  jusqu'à 30-32 h, maturation jusqu'à 46 h, vieillissement jusqu'à 72 h
  [10, p. 1725-1726].
- ⚠️ **Deux citations d'une même source primaire ne concordent pas.** Pour la
  phase de croissance (0-32 h, 30 °C), Ruiz-Terán & Owens (1996) donnent selon
  [9, p. 797] une perte de lipides de **3 % de la matière sèche initiale**
  (environ 12 % des lipides), et selon [10, p. 1733] une perte de **30 % des
  lipides bruts**. L'écart est d'un facteur 2 à 3 : **seule la source primaire
  tranchera**.
- **Sur d'autres substrats** [10, p. 1731-1733], la fermentation :
  - fait **monter la teneur en protéines** : soja +9,6 à 16 %, pois chiche
    +6,2 %, féverole +4,6 %, pois +12,1 %, haricot noir +9,5 % ;
  - fait **baisser les lipides bruts** : soja −27,6 %, pois chiche −38,9 %,
    féverole −60,8 %, pois −37,5 %, haricot noir −12,5 à −25 %, pois bambara
    −73,2 % ;
  - fait **monter les cendres** : soja +21,6 %, pois chiche +26,2 %, pois
    +17,4 %, féverole +15,2 % ;
  - fait **baisser les glucides** : haricot −10,3 %, pois bambara −50 % ;
    l'amidon de l'épeautre baisse.

  **La base de ces pourcentages n'est pas précisée**, probablement des
  teneurs. Lue comme telle, la tendance est cohérente sur tous les
  substrats : protéines et minéraux restent pendant que la matière sèche
  s'en va, donc leur teneur monte. **Les pertes de lipides, elles, varient
  du simple au sextuple selon la graine** : un pourcentage de perte fixe ne
  se transpose pas d'un substrat à l'autre.
- **Le trempage consomme aussi des sucres :** saccharose, stachyose et
  raffinose baissent sous l'effet des enzymes de la graine, de la diffusion
  dans l'eau **et des micro-organismes du trempage** (Mulyowidarso et al. 1991,
  cités dans [10, p. 1721]). Un trempage long ou tiède perd donc plus qu'un
  simple lessivage.
- **La souche change la consommation des sucres :** *R. microsporus* var.
  *chinensis* hydrolyse saccharose et raffinose, *R. oligosporus* non
  (Schwertz et al. 1997, cités dans [10, p. 1728]).
- ⚠️ **La température qui compte est celle du produit.** Dans un lit statique,
  la chaleur du métabolisme porte le cœur **jusqu'à 12 °C au-dessus de
  l'étuve** [7, p. 206]. Un réglage « température » doit donc désigner la
  température du produit, pas celle de l'étuve.
- **L'eau :** l'humidité des graines passe de 60 à 57 % pendant la
  fermentation [7, p. 206]. C'est la légère perte d'eau portée par le facteur
  de rendement.

**Ce que ça dit du modèle actuel**

- `fermentation_fat = 5 %` est **plausible pour une incubation courte**
  (30-36 h vers 30 °C) et **très sous-estimé** pour une incubation longue ou
  chaude. La fermentation doit recevoir **la durée et la température**.
- ⚠️ **Les AGS : [2] ne tranche pas.** Avec *R. oryzae*, la part saturée des
  acides gras liés augmente [2, p. 171]. Avec *R. oligosporus*, la souche
  usuelle, elle **baisse** : palmitique et stéarique font 14,4 % des acides gras
  liés à 0 h et 12,2 % à 69 h, à 30 °C [2, tableau 1, p. 173]. La réserve de
  `methode.md`, qui tient les AGS pour sous-estimés, ne trouve donc pas
  d'appui ici pour la souche usuelle.
- `fermentation_fat = 5 %` est **probablement sous-estimé, même en
  incubation courte** : le bilan de Ruiz-Teran & Owens donne environ 12 % des
  lipides en 32 h (voir plus haut). Ce chiffre repose sur une étude
  secondaire et une teneur en lipides supposée : à confirmer.
- **Protéines à la fermentation :** le modèle ne perd rien. Les sources disent
  1 à 2 % aux durées usuelles (28-46 h), 4 % à 72 h. **Le modèle est donc
  proche** ; une perte qui croît avec la durée serait plus juste.
- `fermentation_carbs = 60 %` : le bilan de Ruiz-Teran & Owens attribue 6,5 %
  de la matière sèche initiale à des composants « non identifiés », très
  probablement surtout des glucides. Rapporté aux glucides assimilables d'un
  soja cuit, faibles, **une perte de cet ordre n'est pas absurde**. Mais les
  enzymes du champignon solubilisent aussi une partie des parois cellulaires
  (arabinogalactanes, pectines) [9, p. 797-798] : **pas de conclusion sans la
  source primaire**.
- ⚠️ **Les fibres ne sont pas conservées : elles augmentent.** Les fibres
  alimentaires passent de 3,7 à 5,8 % de la matière sèche « du fait de la
  croissance du mycélium » (Karyadi, cité dans [9, p. 798]). Le modèle, qui les
  tient pour conservées, les **sous-estime** donc plutôt à la fermentation, ce
  qui est le sens prudent pour une étiquette.
- **Ce que ça dit des protéines sur toute la chaîne :** si la fermentation ne
  perd que 1 à 2 %, les 19,7 % de pertes d'azote de Smith et al. (1964)
  [1, p. 80] viennent surtout **d'avant** : germe et débris au dépelliculage,
  trempage et cuisson. Or le trempage acidifié fait tomber l'azote soluble de
  45,7 % à 7,4 % de l'azote total, et la cuisson à 2,0 % [6, tableau 1] :
  l'acidification rend les protéines insolubles, donc moins lessivables.
  **Piste :** un trempage acidifié perd peu de protéines, un trempage neutre
  beaucoup plus. Ce serait un réglage de `Soaking`.
- ⚠️ **Piège de lecture de [2] :** les teneurs y sont en % de matière sèche, et
  la matière sèche diminue elle-même. Pour en tirer un coefficient en masse
  absolue, il faut la perte de matière sèche du même essai, que [2] ne donne pas.

---

## 6. Torréfaction

Tout se lit **en matière sèche** : la torréfaction chasse de l'eau, et une
teneur « telle quelle » monte mécaniquement. On suppose que seule l'eau part.

**Sucres — calés sur `official/`.** La table japonaise (MEXT 2020) publie la
graine sèche et son kinako, en sucres pesés :

| | graine | kinako | en matière sèche |
|---|---|---|---|
| soja jaune (04023 → 04029) | 6,0 g (eau 12,4) | 6,1 g (eau 4,0) | 6,85 → 6,35 : **− 7 %** |
| soja vert (04104 → 04082) | 7,5 g (eau 12,5) | 7,4 g (eau 5,9) | 8,57 → 7,86 : **− 8 %** |

Les sucres réducteurs du soja vert (glucose 0,2, fructose 0,2) disparaissent
de son kinako : c'est la signature de Maillard. Retenu : **− 8 %**. [18] ne
trouvait pas de baisse significative du saccharose, mais sur du soja trempé
puis grillé, et avec une extraction que la torréfaction facilite.

**Fibres — [19].** Quinoa, graines entières, 8 min à 120 °C : 18,81 → 15,83 g
pour 100 g de matière sèche, **− 16 %** [19, tableau 1]. Couple soja jaune →
kinako, Prosky des deux côtés : 20,43 → 18,85, − 8 %. Le couple vert ne se
compare pas (AOAC 2011.25 pour la graine, Prosky pour le kinako). Retenu :
− 16 %, la plus forte baisse, qui sous-déclare les fibres.

**Le reste — inchangé.** Protéines, lipides, cendres et amidon ne bougent pas
de façon significative en matière sèche ([13], [19]). Les couples japonais
disent autre chose — lipides +10 à +19 % — mais ce sont deux lots : ils ne
calent que ce qui bouge dans le même sens sur les deux.

**À chercher :** un même lot de soja sec, cru puis torréfié à la manière d'un
kinako (150-200 °C) ; sésame, arachide.

---

## 7. Priorités de lecture

1. ~~**[3]**~~ — lu : il fixe la forme et le rythme du trempage, pas son
   plafond (§ 2).
2. **Les études primaires citées par [1]** (Steinkraus 1960-1965, Smith 1964),
   pour la perte de protéines. Et **Ruiz-Teran & Owens (1996)**, cité par [9],
   pour le bilan de matière de la fermentation : c'est la source primaire qui
   calerait `Fermentation`.
3. **[4]** et **[5]**, pour le dépelliculage et la cuisson hors soja.
4. **Une source sur les céréales** (riz, orge, avoine en tempeh), qui manque
   entièrement.

### Pistes en accès libre, non lues

Repérées par recherche bibliographique ; ni lues ni numérotées. À déposer dans
`docs/`, puis à lire avant d'en citer quoi que ce soit.

| Sujet | Référence | Pourquoi |
|---|---|---|
| **Ce qui part dans l'eau** | « Chickpeas' and Lentils' Soaking and Cooking Wastewaters Repurposed for Growing Lactic Acid Bacteria », *Foods* 12 (2023) 2324 — <https://doi.org/10.3390/foods12122324> | mesure le lessivé **dans l'eau** : protéines, sucres, minéraux, en absolu |
| Trempage et cuisson de haricots | « Effects of soaking and thermal treatment on nutritional quality of three varieties of common beans (*Phaseolus vulgaris* L.) from Madagascar », *Legume Science* 4 (2022) — <https://doi.org/10.1002/leg3.143> | effet de la durée et de la chaleur sur plusieurs nutriments |
| **Pellicule** | « Chemical composition of dehulled seeds of selected lupin cultivars in comparison to pea and soya bean », *LWT* 59 (2014) 587-590 — <https://doi.org/10.1016/j.lwt.2014.05.026> | composition avec et sans pellicule : cale `hull_fibre` |
| Céréales | « Evaluation of biochemical and antioxidant dynamics during the co-fermentation of dehusked barley with *Rhizopus oryzae* and *Lactobacillus plantarum* », *Journal of Food Biochemistry* 44 (2019) e13106 — <https://doi.org/10.1111/jfbc.13106> | le seul essai céréales trouvé |
| Revue | « Fermentation of Cereals and Legumes: Impact on Nutritional Constituents and Nutrient Bioavailability », *Fermentation* 8 (2022) 63 — <https://doi.org/10.3390/fermentation8020063> | pour trouver des sources primaires hors soja |

### Bornes de contrôle

La norme Codex du tempeh de soja (CXS 313R-2013) fixe, en masse fraîche :
**protéines ≥ 15 %, humidité ≤ 65 %, lipides ≥ 7 %, fibres brutes ≤ 2,5 %**
[10, p. 1719]. La norme indonésienne SNI 3144:2009 demande 1 point de
protéines et 3 points de lipides de plus [10, p. 1719]. **Piste :** un
avertissement dans `compute()` quand un tempeh de soja calculé sort de ces
bornes, parce que c'est le signe d'une fiche ou d'un coefficient faux.

