# Références bibliographiques

L'index des sources scientifiques sur lesquelles s'appuient les transformations.

## La convention

- **Un numéro par source, attribué une fois pour toutes.** On ne renumérote
  jamais et on ne réutilise jamais un numéro, même si une source est
  abandonnée : elle reste listée, marquée *retirée*, avec la raison.
- **On cite la page imprimée**, pas celle du PDF : `[1, p. 80]`. Quand les deux
  diffèrent, le décalage est noté ci-dessous.
- **Dans le code**, en commentaire anglais : `# [1, p. 80]: 21.9% of solids lost overall`.
  Dans la doc, en français : « … 21,9 % des solides [1, p. 80] ».
- **Les titres restent dans leur langue d'origine**, jamais traduits : c'est
  ce qu'on retrouve dans une base bibliographique.
- **Une source citée par une autre** ne reçoit pas de numéro tant qu'on ne l'a
  pas lue : on écrit « Steinkraus (1964), cité dans [1, p. 80] ».
- **Les PDF sont dans `docs/`**, ignoré par git : on ne les redistribue pas. Le
  nom du fichier local est noté pour les retrouver.

## Statut

| | |
|---|---|
| **lu** | le texte intégral a été lu ; on peut en citer des chiffres |
| **résumé** | seul le résumé a été lu ; on peut citer une tendance, **pas un chiffre** |
| **non lu** | seules les métadonnées sont vérifiées (DOI, titre, revue) ; on ne cite **rien** du contenu |
| **retirée** | n'est plus utilisée — la raison est donnée |

---

## Index

### [1] Shurtleff & Aoyagi, 1980 — *Tempeh Production*

W. Shurtleff, A. Aoyagi. *Tempeh Production: The Book of Tempeh, Volume 2 — A
Craft and Technical Manual*. New-Age Foods Study Center, Lafayette (Californie), 1980.

- **Statut :** lu, par passages (voir ci-dessous).
- **Fichier :** `docs/Tempeh Production_ The Book of Tempeh_ Volume 2_ … New-Age Foods.pdf`
- **Pages :** page imprimée = page du PDF **+ 2**.
- **Ce qu'on en tire :**
  - la structure de la graine de soja : pellicule, germe, cotylédons (p. 60) ;
  - les pertes au dépelliculage (p. 72) ;
  - la cuisson : durées, acidification, vapeur (p. 74-75) ;
  - les rendements et les pertes de solides par étape (p. 80).
- **Réserve :** c'est un manuel de production, pas un article évalué par des
  pairs. Ses chiffres de pertes viennent d'études qu'il cite (Steinkraus
  1960-1965, Smith 1964, Murata 1967) ; les lire directement vaudrait mieux.

### [2] de Reu et al., 1994 — *Changes in soya bean lipids during tempe fermentation*

J. C. de Reu, D. Ramdaras, F. M. Rombouts, M. J. R. Nout. « Changes in soya bean
lipids during tempe fermentation ». *Food Chemistry* 50 (1994) 171-175.
<https://doi.org/10.1016/0308-8146(94)90116-3>

- **Statut :** lu.
- **Fichier :** `docs/439179.pdf`
- **Ce qu'on en tire :** la perte de lipides dépend fortement de la
  **température** et de la **durée** d'incubation, ainsi que de la méthode
  d'acidification (p. 172-174).
- **Réserve :** les teneurs sont données en **% de la matière sèche**, qui
  diminue elle-même pendant la fermentation. Une baisse en % de matière sèche
  n'est donc pas une perte en masse absolue. Le texte est aussi incohérent sur
  la baisse maximale de lipides bruts : « 30 % de la valeur initiale » (p. 172)
  contre « 39 % » (p. 174).

### [3] Han & Baik, 2006 — *Oligosaccharide content and composition of legumes and their reduction by soaking, cooking, ultrasound, and high hydrostatic pressure*

I. H. Han, B.-K. Baik. « Oligosaccharide content and composition of legumes and
their reduction by soaking, cooking, ultrasound, and high hydrostatic pressure ».
*Cereal Chemistry* 83 (2006) 428-433. <https://doi.org/10.1094/CC-83-0428>

- **Statut :** lu.
- **Fichier :** `docs/Oligosaccharide_Content_and_Composition_of_Legumes.pdf`
- **Pages :** page imprimée = page du PDF **+ 427** (le PDF couvre les p. 428-433).
- **Ce qu'on en tire :**
  - la **cinétique** du trempage (3 h et 12 h, 22 °C, graines entières) sur
    lentille, pois chiche, pois et soja [tableau II, p. 431]. Le rythme est commun
    (τ ≈ 3,5 h), le plafond propre à chaque graine ;
  - la **prise d'eau** au trempage [p. 430] ;
  - l'effet **non monotone** de la cuisson [p. 431].
- **Réserves :**
  - il mesure des **oligosaccharides**, qui ne sont pas des sucres au sens INCO.
    Ils servent ici d'indicateur de la fuite des petits sucres solubles ;
  - les teneurs sont en mg/g de graine **séchée après traitement**, sans
    correction de la matière sèche perdue ;
  - **graines entières**, non dépelliculées.

### [4] Wang et al., 2009 — *Influence of cooking and dehulling on nutritional composition of several varieties of lentils (Lens culinaris)*

N. Wang, D. W. Hatcher, R. Toews, E. J. Gawalko. « Influence of cooking and
dehulling on nutritional composition of several varieties of lentils (*Lens
culinaris*) ». *LWT — Food Science and Technology* 42 (2009) 842-848.
<https://doi.org/10.1016/j.lwt.2008.10.007>

- **Statut :** non lu. Le DOI est vérifié ; ce qui suit vient d'un moteur de recherche, pas de l'article. Le PDF est à déposer dans `docs/`.
- **Pourquoi :** il mesure l'effet du **dépelliculage** et de la **cuisson** sur
  les protéines, l'amidon, les fibres, les sucres et les minéraux d'une
  légumineuse autre que le soja.

### [5] Wang et al., 2010 — *Effect of cooking on the composition of beans (Phaseolus vulgaris L.) and chickpeas (Cicer arietinum L.)*

N. Wang, D. W. Hatcher, R. T. Tyler, R. Toews, E. J. Gawalko. « Effect of cooking
on the composition of beans (*Phaseolus vulgaris* L.) and chickpeas (*Cicer
arietinum* L.) ». *Food Research International* 43 (2010) 589-594.
<https://doi.org/10.1016/j.foodres.2009.07.012>

- **Statut :** non lu. Le DOI est vérifié ; ce qui suit vient d'un moteur de recherche, pas de l'article. Le PDF est à déposer dans `docs/`.
- **Ce qu'en rapporte le moteur de recherche (à vérifier) :** en % de la matière sèche, la cuisson à l'eau
  **augmente** les protéines, l'amidon et les fibres, et **diminue** les
  cendres, le potassium, le magnésium, le saccharose et les oligosaccharides.
  Autrement dit, ce qui part à l'eau, c'est le soluble.

### [6] de Reu et al., 1995 — *Protein hydrolysis during soybean tempe fermentation with Rhizopus oligosporus*

J. C. de Reu, R. M. ten Wolde, J. de Groot, M. J. R. Nout, F. M. Rombouts,
H. Gruppen. « Protein hydrolysis during soybean tempe fermentation with
*Rhizopus oligosporus* ». *Journal of Agricultural and Food Chemistry* 43 (1995)
2235-2239. <https://doi.org/10.1021/jf00056a050>

- **Statut :** lu. **Accès libre** : <https://edepot.wur.nl/439178>
- **Fichier :** `docs/deReu1995-protein-hydrolysis.pdf`
- **Pages :** page imprimée = page du PDF **+ 2233**.
- **Ce qu'on en tire :**
  - les protéines (N × 6,25) en % de matière sèche à chaque étape, et après
    65 h à 25, 30 et 37 °C [tableau 2, p. 2236] ;
  - la part d'azote soluble dans l'eau, qui s'effondre au trempage acidifié
    puis à la cuisson [tableau 1, p. 2236] ;
  - une synthèse de la littérature sur les protéines pendant la fermentation
    [p. 2238].
- **Réserve :** teneurs en % de matière sèche, sans la perte de matière sèche
  de l'essai.

### [7] Han, Kiers & Nout, 1999 — *Solid-substrate fermentation of soybeans with Rhizopus spp.: comparison of discontinuous rotation with stationary bed fermentation*

B. Han, J. L. Kiers, M. J. R. Nout. « Solid-substrate fermentation of soybeans
with *Rhizopus* spp.: comparison of discontinuous rotation with stationary bed
fermentation ». *Journal of Bioscience and Bioengineering* 88 (1999) 205-209.
<https://doi.org/10.1016/S1389-1723(99)80203-5>

- **Statut :** lu. **Accès libre** : <https://edepot.wur.nl/436233>
- **Fichier :** `docs/Han1999-rotation-vs-stationary.pdf`
- **Pages :** page imprimée = page du PDF **+ 203**.
- **Ce qu'on en tire :**
  - lipides bruts, ammoniac et azote soluble à 0, 24, 48 et 72 h [tableaux 1
    et 2, p. 208] ;
  - la **température au cœur d'un lit statique**, jusqu'à 12 °C au-dessus de
    l'étuve [p. 206] ;
  - l'humidité des graines, de 60 à 57 % pendant la fermentation [p. 206].
- **Réserve :** teneurs en % de matière sèche, sans perte de matière sèche.

### [8] Nout & Rombouts, 1990 — *Recent developments in tempe research*

M. J. R. Nout, F. M. Rombouts. « Recent developments in tempe research ».
*Journal of Applied Bacteriology* 69 (1990) 609-633.
<https://doi.org/10.1111/j.1365-2672.1990.tb01555.x>

- **Statut :** lu, par passages (p. 615, 624-625). **Accès libre** :
  <https://edepot.wur.nl/549810>
- **Fichier :** `docs/Nout1990-recent-developments-tempe.pdf`
- **Pages :** page imprimée = page du PDF **+ 607**.
- **Ce qu'on en tire :** les pertes de solides par étape [p. 615] et les
  changements chimiques à la fermentation, y compris hors soja [p. 624-625].
- **Réserve :** revue ; ses chiffres viennent des études qu'elle cite. Le PDF
  est un scan : deux fourchettes de la p. 615 sont **illisibles** et ne sont pas
  citées.

### [9] Nout & Kiers, 2005 — *Tempe fermentation, innovation and functionality: update into the third millenium*

M. J. R. Nout, J. L. Kiers. « Tempe fermentation, innovation and functionality:
update into the third millenium ». *Journal of Applied Microbiology* 98 (2005)
789-805. <https://doi.org/10.1111/j.1365-2672.2004.02471.x>

- **Statut :** lu, par passages (p. 792, 795, 797-798). **Accès libre** :
  <https://edepot.wur.nl/23742>
- **Fichier :** `docs/NoutKiers2005-tempe-update.pdf`
- **Pages :** page imprimée = page du PDF **+ 787**.
- **Ce qu'on en tire :** le **bilan de matière de la fermentation** : ce que
  deviennent protéines, lipides et glucides, et en quelle quantité [p. 797,
  citant Ruiz-Teran & Owens 1996].
- **Réserve :** revue ; le bilan chiffré vient de Ruiz-Teran & Owens (1996),
  que nous n'avons pas lu.

### [10] Ahnan-Winarno et al., 2021 — *Tempeh: a semicentennial review on its health benefits, fermentation, safety, processing, sustainability, and affordability*

A. D. Ahnan-Winarno, L. Cordeiro, F. G. Winarno, J. Gibbons, H. Xiao. « Tempeh:
a semicentennial review on its health benefits, fermentation, safety,
processing, sustainability, and affordability ». *Comprehensive Reviews in Food
Science and Food Safety* 20 (2021) 1717-1767. <https://doi.org/10.1111/1541-4337.12710>

- **Statut :** lu, par passages (p. 1718-1719, 1721-1722, 1725-1728,
  1731-1733). Les parties santé, sécurité et durabilité ont été sautées.
- **Fichier :** `docs/Tempeh A semicentennial review.pdf`
- **Pages :** page imprimée = page du PDF **+ 1716**.
- **Ce qu'on en tire :**
  - la norme Codex du tempeh (CXS 313R-2013) : bornes de composition [p. 1719] ;
  - les réglages usuels du procédé et les phases de la fermentation
    [p. 1721-1722, 1725-1727] ;
  - **les effets de la fermentation sur plusieurs substrats** : soja, pois
    chiche, féverole, pois, haricot noir, pois bambara, épeautre, quinoa
    [tableau 5 et p. 1731-1733].
- **Réserves :**
  - revue ; ses chiffres viennent des études qu'elle cite. **Elle ne dit pas
    toujours sur quelle base** (% de matière sèche, masse absolue) les
    variations sont exprimées ;
  - elle cite Ruiz-Terán & Owens (1996) autrement que [9] sur les lipides
    (voir `transformations.md`, § 5).

### [11] Liu, 1997 — *Soybeans: Chemistry, Technology, and Utilization*

K. Liu. *Soybeans: Chemistry, Technology, and Utilization*. Chapman & Hall, New
York, 1997. ISBN 0-412-08121-0. Réédition Springer :
<https://doi.org/10.1007/978-1-4615-1763-4>. Chapitre « Fermented Oriental
Soyfoods ».

- **Statut :** lu, par extraits : p. 268-271 et 273 (tempeh : changements
  pendant la fermentation, vitamines, valeur nutritionnelle).
- **Fichiers :** `docs/extract-soybeans-1.pdf` (p. 268-271),
  `docs/extract-soybeans-2.pdf` (p. 273). **Scans sans texte exploitable** :
  lus sur l'image des pages.
- **Ce qu'on en tire :**
  - la cinétique de Steinkraus et al. (1960) à 37 °C : température du produit,
    pH, apparition de l'ammoniac [p. 268] ;
  - le bilan qualitatif tempeh / soja dépelliculé non fermenté : lipides en
    légère baisse, principaux responsables de la baisse de matière sèche,
    protéines et cendres sans différence significative [p. 268-269] ;
  - la composition du tempeh frais en matière sèche : 48,1 % de protéines,
    24,7 % de lipides, 23,9 % de glucides, 3,3 % de cendres, « similaire au soja
    dépelliculé cuit » [p. 273, citant Wang 1986].
- **Réserves :**
  - ouvrage de synthèse : tout vient d'études citées ;
  - le tableau 5.1 cité p. 273 n'est pas dans l'extrait ;
  - la base des « légères » variations (% de matière sèche ou masse) n'est
    pas précisée ;
  - une composition de tempeh seule ne cale rien (`CLAUDE.md`).

### [12] Shurtleff & Aoyagi, 1979 — *The Book of Tempeh*, Appendix E

W. Shurtleff, A. Aoyagi. *The Book of Tempeh*, édition professionnelle. Harper &
Row, New York, 1979. Appendice E, « The Microbiology and Chemistry of Tempeh
Fermentation ».

- **Statut :** lu, extrait p. 186-196. **Scan sans texte exploitable** : lu sur
  l'image des pages.
- **Fichier :** `docs/book of tempeh - appendix e.pdf`
- **Ce qu'on en tire — c'est la source la plus dense du lot :**
  - les pertes de solides et d'azote **étape par étape** : Smith et al. 1964
    [fig. E.10, p. 189], Steinkraus et al. 1961 et 1964 [p. 188] ;
  - la moyenne de huit études : 100 g de soja entier → 173 g de tempeh, 26,5 %
    des solides et 16,7 % des protéines perdus [p. 188] ;
  - la **composition de la pellicule** (Cowan 1969) [p. 188] ;
  - saccharose, raffinose et stachyose au trempage-cuisson et à la fermentation
    (Shallenberger et al. 1976) [p. 194, fig. E.13 p. 195] ;
  - lipides au trempage et à la fermentation [p. 188, 193] ; fibres [p. 195] ;
    cendres [p. 196] ; protéines [p. 192].
- **Réserves :**
  - synthèse : tout vient d'études des années 1946-1977, citées ;
  - les pourcentages sont tantôt des pertes absolues, tantôt des variations de
    teneur en matière sèche, et la base n'est pas toujours dite ;
  - les pertes d'azote par étape de Smith (9,5 + 10,0 + 1,7) ne somment pas au
    total annoncé (19,7) ;
  - fibres des années 1960-1970 : **fibres brutes**, pas fibres alimentaires.

### [13] Agume, Njintang & Mbofung, 2017 — *Effect of Soaking and Roasting on the Physicochemical and Pasting Properties of Soybean Flour*

A. S. N. Agume, N. Y. Njintang, C. M. F. Mbofung. « Effect of Soaking and
Roasting on the Physicochemical and Pasting Properties of Soybean Flour ».
*Foods* 6 (2017) 12. <https://doi.org/10.3390/foods6020012>

- **Statut :** lu (méthode, tableau 1 et discussion de la composition).
  **Accès libre.**
- **Fichier :** `docs/Foods2017-soaking-roasting-soy-flour.pdf`
- **Pages :** numérotation de l'article, « 4 of 11 », « 5 of 11 ».
- **Ce qu'on en tire :** la composition en matière sèche du soja trempé 0, 24,
  48 et 72 h à 25 °C, puis dépelliculé, avec ou sans torréfaction à 110 °C
  pendant 10 min [tableau 1, p. 4] :
  - protéines 46,0 → 43,9 → 37,9 → 35,8 % : elles baissent **de plus en plus**
    avec la durée ;
  - cendres stables (3,5-3,6 %) : les minéraux partent au rythme des solides ;
  - la torréfaction légère ne change ni les glucides totaux, ni les protéines,
    ni les lipides, ni les cendres.
- **Réserves :** teneurs en % de matière sèche, sans perte de matière sèche
  mesurée ; trempage « traditionnel » camerounais à 25 ± 4 °C, avec
  fermentation naturelle ; écarts-types de 1 à 4 g/100 g, qui masquent de
  petites variations ; sucres non mesurés.

### [14] Wang, Swain, Hesseltine & Heath, 1979 — *Hydration of whole soybeans affects solids losses and cooking quality*

H. L. Wang, E. Swain, C. W. Hesseltine, H. D. Heath. « Hydration of whole
soybeans affects solids losses and cooking quality ». *Journal of Food Science*
44 (1979) 1510-1513. <https://doi.org/10.1111/j.1365-2621.1979.tb06474.x>

- **Statut :** résumé (via OpenAlex). Payant.
- **Ce qu'on en tire (tendances) :** les solides partent **à un rythme
  régulier** pendant tout le trempage, plus vite à chaud ; la température est
  le premier facteur ; la part de protéines dans ce qui part augmente avec la
  durée et la température ; une partie seulement des sucres solubles est
  retirée après une nuit à 25 °C.
- **À lire :** il mesure la perte de solides en fonction de la durée et de la
  température, ce qui permettrait de caler le trempage au-delà de 24 h et d'en
  faire dépendre la température.
