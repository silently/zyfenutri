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
  masse de chaque ingrédient, telle qu’achetée  →  weight_g, par intrant
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

⚠️ **Ce raisonnement vaut pour juger UN LOT.** Pour une **étiquette**, le poids
de tempeh se **prédit** par le facteur de rendement, et ce n'est pas un repli :
le § 3.3 dit pourquoi. Dans les deux cas, c'est la même division finale qui
porte l'eau reprise — seul change ce qu'on met au dénominateur, et donc ce que
la fiche décrit.

#### Ce qu'il faut fournir

| Donnée | Pour qui | Remarque |
|---|---|---|
| Composition pour 100 g | tout ingrédient **sauf le starter** | le starter est exclu du calcul : ni sa fiche ni son poids n'entrent nulle part |
| Masse mise en œuvre | tout ingrédient | base de pesée ci-dessous |
| **Dépelliculage**, oui ou non | substrat | *fait par nous*, après réception |
| **Torréfaction**, oui ou non | support d'inoculation | *faite par nous* — une farine achetée déjà torréfiée porte le résultat dans sa composition |
| Durée de **cuisson** | **chaque substrat** | cf. ci-dessous |
| Durée de **fermentation** | le lot | collective par nature |
| **Facteur de rendement** | chaque substrat | cf. § 3.3 |

⚠️ **La cuisson appartient au SUBSTRAT, pas au lot.** Un soja, une lentille et
un pois chiche ne cuisent pas le même temps, et pas dans la même casserole.
Une durée unique appliquée à une recette mixte ferait subir à l'un une cuisson
qu'il n'a pas eue — et tous les coefficients de cuisson sont fonction du temps.
Le document peut porter une durée par défaut ; celle de l'intrant l'emporte.

⚠️ **La fermentation, elle, est un fait du LOT.** Tout le bloc incube ensemble,
les mêmes heures. La régler par intrant n'aurait aucun sens physique.

⚠️ **Le dépelliculage et la torréfaction se déclarent sur « qui les fait », pas
sur « l'ingrédient est-il dans cet état ».** Une graine achetée déjà décortiquée
se déclare **non dépelliculée** : sa composition et son poids en tiennent déjà
compte, et la déclarer dépelliculée retirerait une pellicule une seconde fois.

#### Sur quelle base on pèse

C'est le point où une erreur de lecture coûte le plus cher, parce qu'elle est
invisible dans le résultat.

| Rôle | Base |
|---|---|
| **Substrat** | la graine **telle qu'achetée**, sèche, **avant toute transformation** — pellicule comprise si on la retire soi-même |
| Support, acidifiant | le produit **tel quel**, eau comprise |

⚠️ **« Sèche » ne veut pas dire « matière sèche ».** Une légumineuse sèche
contient encore de l'ordre de 10 % d'eau, et c'est ce poids-là qu'on saisit —
celui de la balance, pas celui qu'on obtiendrait après dessiccation. Retirer
cette eau fausserait tout le calcul d'autant.

⚠️ **La base de la masse et celle de la composition doivent être la même.** Une
fiche donnée pour 100 g de produit tel quel, appliquée à une masse hors eau,
mesure deux choses différentes. C'est la raison pour laquelle un acidifiant se
pèse tel quel : sa fiche l'est aussi.

### 3.2 La chaîne de calcul — cinq transformations, et rien d'autre

> ⚠️ **Aucun coefficient n'est encore validé par une analyse de laboratoire.** Plusieurs restent
> des hypothèses, marquées comme telles ci-dessous et dans `zyfenutri/transforms.py`. Le détail,
> source par source, est dans [`transformations.md`](transformations.md).

Le calcul ne manipule que des **masses absolues de nutriments**, du début à la fin. On part de ce
qui entre dans le lot, on applique à chaque ingrédient les transformations qu'il subit réellement,
on additionne, et on divise **une seule fois** par le poids de tempeh obtenu.

Ce dernier point est la clé de la méthode : c'est cette division finale, et elle seule, qui porte
l'eau reprise au trempage. Un lot qui double de poids en s'hydratant voit mécaniquement toutes ses
valeurs divisées par deux, sans qu'aucun coefficient n'ait à le dire.

⚠️ **Rinçage et égouttage ne sont pas des coefficients à part.** Ils sont
compris dans les pertes du trempage et de la cuisson, qui se font toutes deux
« dans une eau qu'on jette » : c'est cette eau, et ce qu'elle emporte, qui est
chiffrée. Les compter séparément compterait la même perte deux fois.

Chaque transformation raisonne **pour 100 g d'ingrédient tel qu'il a été pesé, avant toute
transformation**, et rend des grammes de nutriment, jamais une teneur « pour 100 g de ce qui
reste ». Aucune ne touche à l'eau. Une valeur qu'une transformation ne sait pas traiter — une
durée au-delà des mesures publiées, par exemple — ressort **inconnue**, jamais estimée.

Les coefficients raisonnent **par fraction** (sucres ou amidon, soluble ou non), jamais par
espèce : c'est la fiche de l'ingrédient qui porte la différence entre un soja et une lentille.

#### Qui subit quoi

| Ingrédient | Transformations appliquées |
|---|---|
| **Substrat** (soja, pois chiche, pois cassés…) | T1 dépelliculage *(si pratiqué)* → T2a trempage → T2b cuisson → T2c fermentation |
| **Support d'inoculation** (farine de riz, kinako) | T3 torréfaction *(si pratiquée)* → T2c fermentation |
| **Acidifiant pré-inoculation** (vinaigre) | aucune — ajouté après cuisson, compté au prorata de sa masse |
| **Acidifiant de trempage** | **exclu** — il part avec l'eau de trempage, qui est jetée |
| **Starter** | **exclu** — quelques grammes pour plusieurs kilos de produit |

Les deux exclusions **sous-déclarent** légèrement le produit fini : un peu d'acide pénètre le
grain, le starter pèse quelque chose. C'est le sens prudent, celui qui n'expose pas.

Le support d'inoculation ne trempe ni ne cuit : il est ajouté **après l'égouttage**. Il fermente en
revanche, puisqu'il est dans le bloc pendant toute l'incubation. C'est pourquoi la « tempehisation »
se décompose en étapes qui ne concernent pas les mêmes ingrédients.

#### T1 — Dépelliculage

La pellicule d'une légumineuse est surtout de la fibre. La retirer n'enlève donc pas la même part de
chaque nutriment. La transformation ne dit que **ce qui part avec elle** ; la **masse** de
pellicule, elle, est portée par le facteur de rendement (T5), jamais deux fois.

| | Règle | Source |
|---|---|---|
| Part de pellicule | 9 % de la graine | 8 à 10 % [1, p. 60] ; 7,9 % à la main, 9,5 % à la machine (Smith 1964, cité dans [12, p. 189]) |
| Protéines | 8,8 g pour 100 g de pellicule | Cowan 1969, cité dans [12, p. 188] |
| Lipides (et AGS, qui suivent) | 1,0 g pour 100 g de pellicule | *idem* |
| Fibres | la **moitié** des fibres de la fiche | [1, p. 60] |
| Sel | au prorata des cendres : 4,3 % dans la pellicule, 4,87 % dans la graine | [12, p. 188] ; hypothèse : le sodium suit les cendres |
| Sucres, amidon | inchangés | hypothèse |

Pour un soja à 40 g de protéines, c'est 0,8 g de protéines en moins pour 100 g de graine (− 2 %).
Le germe (3 % du soja [1, p. 60]) part parfois aussi : non modélisé, cela dépend de la machine.
⚠️ Ces proportions sont celles du **soja** : une lentille ou un pois chiche n'a pas la même
pellicule, et des pois cassés sont vendus déjà dépelliculés.

#### T2a — Trempage (toujours une nuit, 10 à 15 h)

L'eau de trempage est **jetée** : ce qui s'y dissout est perdu. Le trempage n'est pas un réglage —
un tempeh trempe une nuit —, chaque coefficient est la part conservée après 10 à 15 h.

| Nutriment | Perte | Source |
|---|---|---|
| Sucres | **− 27 %** | saccharose et fructose restant dans la graine à 25 °C [14, tableau 2, p. 1512] |
| Protéines | **− 3 %** | protéines solubles dans l'eau de trempage [14, tableau 1, p. 1511], plus l'azote non protéique (Lo et al. 1968, cité dans [14, p. 1510]) |
| Sel | **− 5 %** | les cendres partent au rythme des solides ([14], [13, tableau 1]) ; hypothèse : le sodium suit les cendres |
| Lipides (et AGS) | **− 1,2 %** | hypothèse : moitié des − 2,5 % mesurés à 24 h [12, p. 193] |
| Amidon, fibres | aucune | hypothèse : insolubles |

#### T2b — Cuisson (durée)

L'eau de cuisson est **jetée**. La perte monte vite puis plafonne, une fois la part soluble partie :
`conservé = 1 − perte maximale × (1 − e^(−durée / 20 min))`. La constante de 20 min est une
hypothèse : la cuisson usuelle dure 20 à 60 min [10, p. 1721].

| Nutriment | Perte maximale | À 30 min | Source |
|---|---|---|---|
| Sucres | **− 44 %** | − 34 % | saccharose − 59 % sur trempage et cuisson (Shallenberger 1976, cité dans [12, p. 194]), déduction faite du trempage |
| Protéines | **− 8 %** | − 6 % | ce qui reste des ~14 % perdus de la graine au tempeh ([12, p. 188-192], [15]), une fois retirés pellicule, trempage et fermentation |
| Sel | **− 2 %** | − 1,6 % | cendres conservées à 92-98 % de la graine au tempeh [15], moins le trempage |
| Lipides, amidon, fibres | aucune | — | hypothèse : insolubles |

#### T2c — Fermentation (durée)

Le mycélium respire : il brûle des glucides pour son énergie et entame les lipides via ses lipases.
Entre deux durées mesurées, on interpole en ligne droite ; **au-delà de la dernière, la valeur
ressort inconnue**.

| Nutriment | Perte | Source |
|---|---|---|
| Lipides | **− 6 %** à 12 h, **− 12 %** de 26 à 60 h, − 59 % à 120 h, − 67 % à 180 h | [16, tableau 1, p. 529] |
| AGS | leur part dans les lipides monte de **7,9 points**, atteints à 26 h ; au-delà de 60 h, inconnue | calé sur `refs/official/` (voir plus bas) |
| Protéines | − 1,1 % à 28 h, − 2,2 % à 46 h, − 4,4 % à 72 h | [16, p. 523], [9, p. 797] |
| Sucres | − 17 % à 48 h | Shallenberger 1976, cité dans [12, p. 194] ; hypothèse : linéaire |
| Amidon | − 31 % à 37,5 h, − 39 % à 48 h | [15, tableaux 1-2], borne haute |
| Fibres | aucune | hypothèse — elles montent dans la plupart des études [12, p. 195], [15] : les tenir constantes les sous-déclare |
| Sel | aucune | cendres constantes pendant toute la fermentation [16, p. 526] |

À 36 h : lipides − 12 %, protéines − 1,6 %, sucres − 13 %, amidon − 30 %. Les coefficients sont
ceux de *Rhizopus oligosporus* ; la température du produit compte autant que la durée ([2], [7]),
mais aucune source lue ne l'a encore chiffrée : ce n'est pas un réglage.

#### T3 — Torréfaction (supports uniquement)

`roasted: true` veut dire que **l'atelier torréfie lui-même** : la composition et le poids donnés
sont ceux du produit **cru**, avant torréfaction. Un kinako acheté tout fait est déjà torréfié —
sa fiche le dit — et s'entre avec `roasted: false`, sans quoi la torréfaction serait comptée deux
fois.

**Pourquoi les protéines et les lipides n'augmentent pas.** La torréfaction chasse de l'eau :
100 g de farine crue à 12 % d'eau donnent environ 92 g de farine torréfiée à 4 %. Les 34 g de
protéines qu'elle portait sont toujours là — ils pèsent simplement dans 92 g au lieu de 100, d'où
37 g « pour 100 g » sur la fiche d'un kinako. La **teneur** monte, la **masse** ne bouge pas. Or le
calcul suit des masses, et ne divise qu'une fois, à la fin, par le poids de tempeh récolté. Faire
aussi monter les protéines à la torréfaction compterait l'eau perdue deux fois — l'erreur que la
méthode est construite pour rendre impossible (§ 3.2). L'eau chassée ici revient d'ailleurs dans le
bloc, prise aux graines humides : seule la pesée finale sait ce qu'il en reste.

**Pourquoi les sucres et les fibres baissent.** Eux ne sont pas concentrés, ils sont **détruits**.
La réaction de Maillard lie des sucres réducteurs aux acides aminés et en fait des pigments bruns
et des arômes — l'odeur de la torréfaction, c'est un peu de matière qui s'en va ; la caramélisation
attaque le saccharose. La chaleur coupe aussi une part des fibres en fragments que le dosage ne
compte plus. Les protéines, elles, restent comptées : elles se dosent par leur azote, qui reste
dans les produits de Maillard.

Pour séparer ces deux effets, on lit les mesures **en matière sèche** : l'eau n'y figure plus, et
ce qui y bouge encore est chimique. On suppose que seule l'eau part (hypothèse : les composés
volatils sont négligés).

| Nutriment | Effet | Source |
|---|---|---|
| Sucres | **− 8 %** | calé sur les deux couples soja → kinako de la table japonaise (MEXT 2020, `refs/official/`) : − 7 % (soja jaune), − 8 % (soja vert). Les sucres réducteurs du soja vert (0,4 g) disparaissent de son kinako. [18] ne trouve pas de baisse significative sur du soja trempé puis grillé : la littérature ne donne pas de chiffre, les couples en donnent un |
| Fibres | **− 16 %** | quinoa torréfié 8 min à 120 °C : 18,81 → 15,83 g pour 100 g de matière sèche [19, tableau 1]. Même sens sur le couple soja jaune → kinako, méthode Prosky des deux côtés : − 8 %. On retient la plus forte baisse, qui sous-déclare les fibres : c'est le sens prudent |
| Amidon | aucun | amidon total inchangé en matière sèche [19, tableau 1] ; les glucides ne baissent donc que des sucres perdus |
| Lipides (et AGS), protéines, sel | aucun | inchangés en matière sèche à 110-120 °C [13, tableau 1], [19, tableau 1] |

⚠️ **Les couples japonais sont deux lots, pas un lot torréfié.** Leurs lipides montent de 10 à 19 %
en matière sèche, ce qu'une torréfaction ne peut pas faire. Ils ne calent donc que les sucres, qui
baissent nettement et dans le même sens sur les deux couples, avec la disparition des sucres
réducteurs attendue de Maillard. ⚠️ Baisser les sucres est le sens **risqué** (on en déclare
moins) : c'est pourquoi on ne retient que ce que les deux couples disent ensemble, et rien au-delà.

⚠️ **Ces coefficients valent pour toute graine** : ils portent sur des fractions (sucres, fibres),
pas sur l'espèce. La torréfaction reste un oui ou non, sans intensité : un kinako torréfié fort
est traité comme la torréfaction à 120 °C de [19]. Sur un lot, l'effet est minime — quelques
grammes de support pour des kilos de tempeh.

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
poids en multipliant le poids brut de chaque substrat par son **facteur de rendement** : la masse
de l'ingrédient dans le tempeh fini, rapportée à sa masse brute **avant toute transformation**.

C'est **un seul facteur**, qui agrège tout ce qui fait varier la masse du grain sec au tempeh :

- les **pertes de matière au dépelliculage** (pellicule, germe, débris), quand il est pratiqué ;
- l'**hydratation**, forte au trempage, puis à la cuisson ;
- la **légère perte d'eau** pendant l'incubation.

Pour 1 livre de soja entier : 2,33 livres trempé, 2,02 dépelliculé, 1,90 cuit, 1,74 de tempeh
[1, p. 80, citant Steinkraus et al. 1961]. Le facteur de rendement vaut ici 1,74. Il ne se découpe
pas par étape, et il n'entre qu'une fois, dans la division. Les **nutriments** partis avec la
pellicule, eux, relèvent de la transformation T1 : la masse et la composition sont comptées
séparément, jamais deux fois.
⚠️ Une fiche obtenue ainsi est explicitement marquée **incomplète** : on n'étiquette pas un produit
avec un dénominateur lui-même estimé.

#### D'où vient chaque coefficient — l'ordre des sources

Chaque coefficient de chaque transformation est cherché dans cet ordre, et **porte son origine**
dans le code et dans la doc :

| Ordre | Origine | Marque |
|---|---|---|
| **1** | **la littérature**, lue : la mesure directe de l'étape concernée | `[n, p. x]` (`references.md`) |
| **2** | à défaut, **un calage sur les couples** de `refs/official/` (graine → tempeh, graine → kinako), pour ce que la littérature laisse ouvert | « calé sur `refs/official/` » |
| **3** | à défaut, **une hypothèse**, présentée comme telle et jamais comme une donnée | « hypothèse » |

Les **analyses de laboratoire** (`refs/analyses/`) ne sont pas un quatrième recours : elles
**jugent** le résultat des trois autres, face aux tolérances réglementaires.

**Pourquoi c'est défendable.** L'article 31 § 4 c) admet le calcul « à partir de données
généralement établies et acceptées » ; les tables nationales de composition en sont l'exemple
même. Caler sur elles ce que la littérature ne donne pas, c'est rester dans ce cadre, **à condition
que le calage soit documenté, reproductible, et que ses limites soient dites**. Une valeur choisie
sans trace, elle, ne l'est pas.

**Les limites du calage sur les couples**, qui en fixent l'usage :

- **Un couple ne donne qu'une équation par nutriment** : ce qui reste entre la graine et le tempeh,
  sur toute la chaîne. Il ne peut caler **qu'une inconnue par nutriment**. Si deux transformations
  restent inconnues pour le même nutriment, le couple ne les départage pas : on ne répartit pas la
  perte au hasard, on l'écrit comme une hypothèse.
- **Les rapports entre nutriments sont robustes, les pertes absolues ne le sont pas.** Le rapport
  lipides / protéines se lit directement sur les deux fiches. Une perte en masse absolue exige, elle,
  le rendement du tempeh de la table, qu'aucune table ne publie : on retient 1,75 [1, p. 80], et le
  coefficient calé hérite de cette hypothèse. Sa sensibilité au rendement doit être indiquée.
- **Le procédé du tempeh de table est inconnu** : dépelliculé ou non, durée et température
  d'incubation. Un coefficient calé vaut pour un procédé **courant**, pas pour un réglage précis.
- **Chaque couple vient d'une seule table** et les glucides ne se comparent que si les deux fiches
  suivent la même convention (`convention_glucides`).
- **Trois couples donnent trois valeurs** : on garde leur **dispersion** comme incertitude, pas
  seulement leur moyenne.
- **Les couples sont tous du soja.** Un coefficient calé dessus n'est pas démontré pour une lentille
  ou une céréale. C'est pourquoi les transformations raisonnent sur des fractions (sucres, amidon…)
  et jamais sur l'espèce.
- **Pas de validation circulaire.** Un coefficient calé sur ces couples ne peut plus être « vérifié »
  par ces mêmes couples. Seule une analyse de laboratoire, ou une source indépendante, le valide.

#### Ce que disent les couples de `refs/official/`

Les couples **graine → tempeh** publiés par une même table — USDA 174270 → 174272,
Nouvelle-Zélande X230 → X10030, Norvège — et les couples **soja → kinako** de la table japonaise
(MEXT 2020) sont conservés dans `refs/official/`. Ils servent à **deux calages seulement**, là où la
littérature lue ne donne pas de chiffre : la part saturée des lipides à la fermentation, et les
sucres à la torréfaction. Le reste vient de la littérature (§ 3.2, T1 à T3).

Les couples graine → tempeh montrent aussi que **le rapport lipides / protéines bouge peu**
(0,546 → 0,532 · 0,514 → 0,517 · 0,518 → 0,532, soit ± 3 %) : protéines et lipides traversent la
chaîne ensemble, et presque intacts. Leurs cendres, en revanche, ne retiennent que 58 à 75 %, bien
moins que les 92-98 % mesurés par [15] : ce calage-là est **écarté** en attendant un bilan mesuré,
les procédés des tempehs de table étant inconnus.

#### Deux réserves, énoncées ici plutôt que tues

⚠️ **Les acides gras saturés.** Les trois couples graine → tempeh montrent une part saturée des
lipides qui augmente de 3,8 à 10,8 points de la graine au tempeh. Le calcul applique la moyenne,
**+7,9 points**, à la fermentation (calage sur `official/`). Cela implique plus d'AGS en masse que
dans la graine : la synthèse de lipides par le mycélium l'expliquerait, mais aucune source lue ne
l'établit. Ce choix est retenu parce que sous-déclarer les AGS serait le sens défavorable.

⚠️ **Les fibres sont probablement sous-estimées.** La frontière entre fibres et glucides est une
convention d'analyse, pas une propriété du produit : la même graine en déclare 9,3 g (USDA,
Nouvelle-Zélande) ou 16,0 g (Norvège). Le calcul ne retire des fibres qu'avec la pellicule (T1) et
à la torréfaction (T3) ; il les tient pour conservées au trempage, à la cuisson et à la
fermentation, où les études les voient plutôt monter. Toute allégation « source de fibres »
devrait s'appuyer sur un dosage, pas sur ce calcul.

### 3.3 Le poids de tempeh : pesé, ou prédit

La division finale a besoin d'un poids de tempeh. Il s'obtient de **deux
façons**, et le choix n'est pas cosmétique : il décide de ce que la fiche
représente.

| | D'où vient le poids | Ce que la fiche représente |
|---|---|---|
| **Pesé** (`harvested_g`) | la balance, après récolte | **ce lot-là**, et lui seul |
| **Prédit** (facteur de rendement) | `masse mise en œuvre × facteur`, par substrat | **la recette**, indépendamment des fournées |

#### Le facteur de rendement

Un nombre par substrat : kg de tempeh pour 1 kg de graines telles qu'achetées.
Il porte **toute** l'évolution de masse de ce substrat sur la fabrication :

- les **pertes** — dépelliculage s'il est fait après réception, pertes de
  matière aux manipulations, eau perdue pendant la fermentation ;
- les **gains**, plus importants — l'eau reprise au trempage et à la cuisson.

⚠️ **Un facteur par substrat, jamais un facteur global.** Un soja et une
lentille ne gonflent pas pareil ; un mélange calé sur une moyenne fausserait la
part de chacun dans le produit.

⚠️ **Le facteur ne porte que la MASSE.** Ce que la pellicule emporte en
nutriments appartient à la transformation « dépelliculage » (§ 3.2). Masse et
composition se comptent séparément — sinon la perte est comptée deux fois.

#### Pourquoi prédire vaut mieux pour une étiquette

C'est contre-intuitif : une pesée est une mesure, une prédiction une hypothèse.
Mais une étiquette ne décrit pas une fournée, elle décrit un produit.

- **Le poids récolté porte sa propre incertitude** : la pesée elle-même, et
  surtout l'humidité du jour, qui déplace le dénominateur sans que la
  composition sèche ait bougé.
- **Une étiquette imprimée ne change pas d'un lot à l'autre.** Recalculer par
  fournée produirait des valeurs qui bougent sans qu'on puisse les imprimer.
- **Le facteur de rendement est une consigne d'atelier**, réglée et relue par
  l'exploitation ; ce n'est pas une approximation subie.
- **Les tolérances du § 2 absorbent l'écart** d'une fournée à l'autre, très
  largement sous les seuils absolus.

⚠️ **`zyfenutri` marque quand même la fiche prédite comme incomplète** :
`missing` porte alors « harvest weight predicted, not weighed — fine to design
a recipe, not to label a product ». La bibliothèque a raison de le dire : elle
ne sait pas si son appelant conçoit une recette ou étiquette un lot.

**C'est à l'appelant de lever cette réserve, et à lui seul de le justifier.**
La page web le fait — elle n'a pas de champ « poids récolté » et rend une fiche
de recette —, et elle ne lève **que** celle-là : une composition manquante ou
une durée absente laissent la fiche incomplète. Le rendement y devient donc
**obligatoire**, puisqu'il est le seul dénominateur.

⚠️ **Le pesé reste le bon choix pour juger une fournée** : confronter un lot
réel à ce qu'on attendait, ou comparer à une analyse de laboratoire. Les deux
usages coexistent ; ils ne répondent pas à la même question.

---

### 3.4 Du lot à l'étiquette

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
3. **Les coefficients de perte** appliqués — `zyfenutri` les rend dans sa sortie, sous
   `coefficients` —, la version de `zyfenutri` qui a calculé, et l'historique de leurs changements.
4. **Le présent document**, qui explicite la méthode.
5. **La fiche de calcul** (`steps`) rendue par `zyfenutri`, qui déroule la chaîne pour un lot.

À refaire lorsque : la recette change, un **fournisseur change** (la composition varie d'une
origine à l'autre), le procédé change de façon sensible (durée de fermentation, égouttage), ou
qu'assez de lots nouveaux se sont accumulés pour déplacer la moyenne.

---

## 5. Limites assumées

- **Les sucres** sont les moins bien couverts : la perte à la fermentation n'est mesurée que
  jusqu'à 48 h (au-delà, la valeur ressort inconnue), et la baisse à la torréfaction est calée sur
  deux lots différents, pas mesurée sur un même lot. Sur un produit à sucres bas, la tolérance
  absolue (± 2 g) absorbe largement l'écart.
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

Les sources scientifiques des transformations sont numérotées dans
[`references.md`](references.md), et discutées une à une dans
[`transformations.md`](transformations.md).

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
contrepartie) ; et en **couples soja → kinako** de la table japonaise (MEXT 2020), pour la
torréfaction.

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

**3. Les coefficients de perte sont les mêmes pour tous les substrats.** Ils raisonnent par fraction (sucres, amidon, protéines…) et non par espèce, ce que [15] appuie sur quatre légumineuses. Mais ils sont presque tous mesurés sur le soja : rien ne les établit encore pour la lentille, l'orge ou les oléagineux, et la pellicule retirée est celle du soja.

**4. La composition d'un intrant est supposée constante.** Une légumineuse varie de 10 à 15 % en protéines selon l'année et l'origine. La fiche produit fige une valeur ; la réalité bouge sous elle. C'est précisément pourquoi la réglementation parle de **valeurs moyennes** et prévoit des tolérances larges.

**5. Les pertes ne dépendent que de deux réglages.** Les durées de cuisson et de fermentation entrent dans le calcul. Le reste n'y entre pas, alors qu'il change réellement ce qui s'en va : température d'incubation, acidification, volume d'eau, graine concassée ou entière, souche. Le trempage, lui, est toujours compté comme une nuit.

**6. Une seule pesée porte tout.** Les valeurs pour 100 g s'obtiennent en divisant par le poids récolté : une erreur de balance à la récolte se propage intégralement aux neuf valeurs, et rien d'autre ne vient la contredire.

**7. La cohérence d'une fiche produit n'est pas vérifiée.** Le contrôle habituel — macros + eau + cendres ≈ 100 g — demande l'humidité et les cendres, que le calcul ne reçoit pas. `zyfenutri.check()` sait refuser une fiche physiquement impossible (valeur négative, « dont » supérieur à son total, macros au-delà de 102 g), mais `compute()` ne l'applique pas aux intrants : une fiche fournisseur erronée passerait donc sans alerte.

> Aucune de ces limites n'interdit de déclarer : l'article 31 § 4 admet le calcul, et les tolérances (§ 2) sont conçues pour absorber cette variabilité. Elles fixent en revanche l'ordre des priorités — **faire doser un lot** est ce qui ferait le plus progresser la fiabilité, loin devant tout raffinement du modèle.
