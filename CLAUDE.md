# zyfenutri — CLAUDE.md

Le calcul qui transforme *ce qu'on a mis dans un lot de tempeh* en *ce qu'on a
le droit d'écrire sur l'étiquette*. Bibliothèque Python + script. Dépôt
**public**.

---

## 🗣️ Langue — RÈGLE STRICTE

| Quoi | Langue |
|---|---|
| `README.md` | **anglais** |
| `README.fr.md`, les autres `.md` (méthode, ce fichier…), les messages de commit | **français** |
| Les commentaires et docstrings **dans le code** | **anglais** |
| Les messages rendus à l'utilisateur (`steps`, libellés d'étiquette) | **français** |

⚠️ Le dépôt est public et le code a vocation à être lu par des gens qui ne
parlent pas français. La **documentation**, elle, s'adresse d'abord à
l'exploitation qui s'en sert, et au contrôle sanitaire français.

⚠️ **Les deux README se maintiennent ensemble.** `README.md` (anglais) et
`README.fr.md` (français) disent la même chose : toute modification de l'un se
reporte dans l'autre, dans le même commit.

⚠️ `steps` est rendu en français **à dessein** : c'est la fiche de calcul qu'on
présente à la DDPP. Ce n'est pas une inconséquence avec la règle ci-dessus.

---

## Le contrat public — ce qui ne doit pas bouger à la légère

**Un document entre, un document sort.** Le même, qu'il vienne d'un fichier,
d'un tube ou d'un appel Python :

```python
compute({"harvested_g": 1750, "fermentation_hours": 36, "ingredients": [...]}) -> dict
```
```bash
zyfenutri lot.yml
```

⚠️ **Personne n'utilise encore ce contrat** : il peut évoluer librement, et on
reste en **1.x** tant que c'est le cas — une rupture fait monter la version
mineure, pas la majeure. Version dans `pyproject.toml` et `zyfenutri/__init__.py`. Dès qu'un consommateur existera, ajouter une clé de sortie
restera sans risque ; en renommer une, en supprimer une, ou changer le sens
d'un rôle cassera des consommateurs qu'on ne voit pas d'ici, et demandera une
version majeure.

⚠️ **Les noms longs restent acceptés en entrée** (`fat_g` → `fat`, cf.
`nutrients.ALIASES`). C'est ce qui évite à un appelant d'écrire une couche de
traduction. Ne pas les retirer.

⚠️ **Une valeur inconnue se propage.** Un ingrédient sans composition ou sans
poids, un réglage absent (`cooking_minutes`…), une lacune d'une transformation :
la valeur du produit est `None`, jamais une somme partielle.

⚠️ **`compute()` ne lève jamais sur une donnée manquante.** Il le dit dans
`missing`, et `complete` répond à la seule question qui compte : est-ce que ça
peut aller sur un emballage ? Une exception ferait perdre le calcul partiel,
qui est utile.

---

## CORE et WEB — deux chantiers, une frontière

Ce dépôt porte **deux choses**, et la frontière entre elles est une règle, pas
une habitude.

| | Quoi | Où |
|---|---|---|
| **CORE** | le calcul et son contrat : `compute()`, la ligne de commande, les transformations, les données de `refs/` | `zyfenutri/`, `tests/`, `refs/`, les `README`, `ARCHITECTURE.md` |
| **WEB** | le portage en application **full front**, sans back end : saisie du document dans des champs HTML, calcul dans le navigateur, rendu de l'étiquette | `web/` |

⚠️ **CORE porte le contrat public.** Tout ce qui s'y touche se répercute sur
des consommateurs qu'on ne voit pas d'ici, et qui l'épinglent par un SHA. C'est
ce qui lui vaut ses invariants, ses tests et ses versions. *(Le dépôt est
public : il décrit ce qu'il fait, jamais qui l'utilise.)*

🛑 **WEB NE TOUCHE PAS À CORE.** Aucune tâche WEB ne modifie un fichier de
CORE — ni une signature, ni un coefficient, ni un test, ni un README. Si un
travail WEB semble l'exiger, **on en parle d'abord** : c'est le signe soit
qu'une règle est mal placée, soit qu'il faut vraiment changer le contrat, et
les deux se décident, jamais en passant.

⚠️ **WEB lit CORE, il ne le duplique pas.** Le calcul du navigateur est le
**même code Python**, exécuté par Pyodide — pas une réécriture en JavaScript.
Une seule implémentation des règles, donc aucune divergence possible entre ce
que dit la ligne de commande et ce que montre la page. Si un jour la lenteur de
Pyodide l'imposait, ce serait une décision à prendre, pas un glissement.

⚠️ **Les dépendances de WEB restent dans WEB.** `web/package.json` lui
appartient ; `compute()` continue de n'importer que la bibliothèque standard, et
`pyproject.toml` ne gagne rien. Le « pas de dépendance nouvelle » ci-dessous
vaut pour CORE.

⚠️ **Pas de serveur pour autant.** WEB est une page **statique** : le serveur de
développement est un outil de construction, pas une pièce du produit. Ce qui
est livré est un dossier de fichiers, ouvrable sans rien lancer.

```bash
cd web && npm install
npm run dev      # sync-core, puis le serveur de développement
npm run build    # sync-core, puis `web/build/` — le site statique
npm run check    # svelte-check
```

`scripts/sync-core.mjs` recopie `zyfenutri/*.py` dans `web/static/core/` avant
chaque `dev` et chaque `build`. **Cette copie n'est pas versionnée** : la
versionner ferait une seconde source des règles, qui divergerait.

⚠️ **Pyodide 314.x embarque CPython 3.14**, la version que CORE exige. C'est ce
qui permet d'exécuter les modules **tels quels**, sans portage ni adaptation.
Vérifié : sur le même document, la page et `zyfenutri lot.yml` rendent la même
étiquette, mention par mention.

⚠️ **Déploiement : GitHub Pages**, par `.github/workflows/pages.yml`, à chaque
poussée sur `main` qui touche `web/` **ou `zyfenutri/`** — une correction dans
CORE change ce que la page calcule, elle doit donc redéployer aussi.

⚠️ **Le site vit sous `/<dépôt>/`, pas à la racine.** La CI passe `BASE_PATH`,
que `svelte.config.js` lit. Sans lui, la page se charge mais ne trouve aucun
module de CORE et reste muette. `static/.nojekyll` est là pour la même raison :
sans lui, Jekyll ignore les dossiers commençant par `_`, dont `_app`.

⚠️ **WEB pose une question que CORE laisse ouverte : le poids de tempeh.**
Cette page n'a **pas** de champ « poids récolté » : le poids est toujours
**prédit** par le facteur de rendement, qui devient donc obligatoire. Une
étiquette ne change pas d'une fournée à l'autre — le facteur est une consigne
d'atelier, et les tolérances du tableau 1 absorbent l'écart. `src/lib/resultat.ts`
lève **cette réserve de CORE, et elle seule** ; une composition manquante ou une
durée absente rendent toujours la fiche incomplète. C'est le même partage que
pour une fiche de formulation côté consommateur.

⚠️ **`web/src/lib/composants/Aide.svelte` est la SOURCE DE VÉRITÉ de WEB.**
C'est la doc utilisateur de la version web : ce qu'elle affirme fait foi. Si le
code s'en écarte, c'est le **code** qu'on corrige, pas la doc — et si c'est la
doc qui a tort, on la change d'abord, explicitement. Elle ne se contredit pas
non plus avec `refs/methode.md`, qui reste la référence de CORE et du droit.

⚠️ **Les messages de `missing` se traduisent dans WEB.** CORE les écrit en
anglais — ils s'adressent à un appelant. La page s'adresse à une personne. Ce
qui n'est pas reconnu passe **tel quel** : mieux vaut de l'anglais qu'un silence.

---

## Les invariants du calcul

⚠️ **Masses absolues du début à la fin.** On ne raisonne jamais en pourcentages
intermédiaires. Chaque transformation prend des grammes et rend des grammes.

⚠️ **On ne divise qu'UNE FOIS**, par le poids de tempeh, tout à la fin. C'est
cette division, et elle seule, qui porte l'eau reprise au trempage. Ajouter un
« facteur d'hydratation » quelque part compterait l'eau **deux fois** — c'est
l'erreur que ce modèle est conçu pour rendre impossible. Deux tests la gardent.

⚠️ **Aucune transformation ne touche à l'eau.** Une torréfaction chasse de
l'eau : ça ne change donc *rien* aux masses de nutriments, seulement les
sucres via Maillard.

⚠️ **Une valeur absente n'est jamais un zéro.** « On ne sait pas » et « il n'y
en a pas » sont deux affirmations différentes, et la seconde engage.

⚠️ **L'énergie se calcule, toujours** — depuis les macros, coefficients de
l'annexe XIV. Elle ne se recopie jamais d'une table. Et les **kcal ne sont pas
les kJ ÷ 4,184** : l'annexe donne deux jeux de coefficients indépendants, et
convertir ferait diverger les deux chiffres de l'étiquette.

⚠️ **On n'arrondit qu'UNE FOIS, à l'impression.** Aucune transformation,
aucun mélange, aucune étape du moteur n'arrondit : la valeur reste exacte
jusqu'à `declared`, qui applique le tableau 4. Arrondir en chemin déplace le
chiffre imprimé d'une unité — 2,449 g passe par 2,45 et s'écrit « 2,5 g » — et
peut transformer une valeur au-dessus du seuil en un « < 0,5 g », qui n'est
plus un arrondi mais une affirmation. C'est la même erreur que la double
division, et quatre tests la gardent. Le `per_100g` du document est arrondi
pour la lecture : cet arrondi-là est terminal, rien ne le relit.

⚠️ **La masse et la composition se pèsent sur la MÊME base.** Un substrat entre
avec le poids de la graine **telle qu'achetée**, sèche, avant toute
transformation, pellicule comprise si on la retire soi-même ; tout le reste
entre **tel quel**, eau comprise. ⚠️ « Sèche » n'est pas « matière sèche » : une
légumineuse sèche porte encore ~10 % d'eau, et c'est ce poids-là qu'on saisit.
Détail : `refs/methode.md` § 3.1.

⚠️ **`dehulled` et `roasted` disent QUI le fait, pas dans quel état est
l'ingrédient.** Une graine achetée déjà décortiquée est `dehulled: false` : sa
fiche et son poids en tiennent déjà compte, et la déclarer dépelliculée
retirerait une pellicule une seconde fois. Idem pour une farine achetée
torréfiée.

⚠️ **Une valeur « dont » ne dépasse jamais son total.** Par défaut, les AGS
suivent les lipides ; seule exception, la fermentation, où leur part augmente
(calée sur `refs/official/`). Les sucres ont leur propre règle, découpée de
l'amidon. Une valeur « dont » supérieure à son total n'a aucun sens physique.

---

## Architecture — huit modules courts

Les types et les signatures sont documentés dans **`ARCHITECTURE.md`**.

| Module | Ce qu'il porte | Ce qu'il ne doit PAS porter |
|---|---|---|
| `nutrients.py` | les 7 noms, les libellés, les alias d'entrée, la fiche `NutritionFacts` | aucune règle de calcul |
| `label.py` | annexe XIV (`energy_of`), arrondis (tableau 4), tolérances (tableau 1) | rien de spécifique au tempeh |
| `checks.py` | bornes physiques, bouclage de masse | rien de réglementaire |
| `transforms.py` | les coefficients, les transformations, le protocole `Transform` et `Retention` | aucune I/O, aucun état, **aucune masse de produit** |
| `mixing.py` | le mélange `mix` : **la seule division** par la masse de produit | aucune transformation |
| `recipe.py` | `Ingredient` et `Recipe` : nomme les pièces, enchaîne `process` puis `mix` | aucune règle de calcul |
| `engine.py` | l'enchaînement : document → document | aucune règle nutriment par nutriment |
| `__main__.py` | la ligne de commande | aucun calcul |

⚠️ **Chaque transformation est une fonction pure** : une fiche en entrée, une
fiche en sortie, **toujours pour 100 g d'ingrédient brut**. Le facteur de
rendement n'entre qu'au mélange.

⚠️ **Une lacune est `None`, jamais une valeur inventée.** Chaque coefficient
d'une transformation porte son origine en commentaire : une source `[n, p. x]`,
`HYPOTHESIS`, ou `GAP` (valeur `None`). Combler une lacune, c'est changer une
donnée, pas le code.

⚠️ **Un réglage (durée…) se lie par une fabrique** qui rend une `Transform` :
toutes les transformations gardent la même signature d'appel.

⚠️ **Un réglage se lit au bon NIVEAU.** La **cuisson** appartient à l'intrant
(un soja et une lentille ne cuisent ni le même temps ni dans la même
casserole), avec la valeur du document en repli. La **fermentation** appartient
au lot : tout le bloc incube ensemble. Avant d'ajouter un réglage, se demander
lequel des deux il est — se tromper produit un calcul faux qui ne se voit pas.

⚠️ Si une transformation a besoin de savoir *quel* ingrédient elle traite, c'est
que la règle est mal placée.

---

## Style de code — le plus simple et le plus moderne possible

⚠️ **Dernière version stable de Python, et elle seule.** Aujourd'hui **3.14**
(`requires-python = ">=3.14"`). Quand une nouvelle version sort (3.15 en octobre
2026), on monte, et on retire ce qu'elle rend inutile. Aucune rétrocompatibilité
avec une version antérieure : pas de `from __future__`, pas de `typing.Optional`,
`Union`, `List`, `Dict`, pas de repli pour un vieil interpréteur.

⚠️ **Le plus simple d'abord.** Une fonction plutôt qu'une classe, une
`dataclass` plutôt qu'une hiérarchie, un module court plutôt qu'un paquet. Pas
d'abstraction tant qu'il n'y a pas deux usages réels. Si un lecteur doit
remonter trois fichiers pour comprendre une ligne, c'est trop.

Concrètement :

| Préférer | Plutôt que |
|---|---|
| `X \| None`, `list[str]`, `dict[str, float]` | `Optional[X]`, `List[str]`, `Dict[str, float]` |
| `type Unit = Literal["kJ", "kcal"]` (PEP 695) | `Unit: TypeAlias = …` |
| `@dataclass(frozen=True, slots=True, kw_only=True)` | une classe écrite à la main, un `dict` à clés libres, un `NamedTuple` |
| `Protocol` pour un contrat de forme | une classe de base abstraite |
| `collections.abc` (`Iterable`, `Mapping`) | leurs équivalents de `typing` |
| `match` quand il clarifie un aiguillage | une cascade de `if` / `elif` sur la même valeur |
| la bibliothèque standard | une dépendance |

---

⚠️ **La justification ne va pas dans le code.** D'où viennent les coefficients,
ce qui les fonde, les réserves assumées : tout ça est dans `refs/methode.md`,
en français. Le code dit *ce qu'il fait*, la doc dit *pourquoi*. Le code a déjà
porté des pages d'essai en français — c'est ce qu'on a corrigé, ne pas y
revenir.

---

## `refs/` — les données, et leur honnêteté

| | |
|---|---|
| `methode.md` | la méthode et le droit. **C'est ce document qu'on présente à un contrôle** |
| `official/` | des compositions **publiées** par des tables nationales, recopiées telles quelles |
| `analyses/` | des analyses de laboratoire, s'il en arrive |
| `references.md` | **l'index numéroté des sources scientifiques** — `[1]`, `[2]`… |
| `transformations.md` | le document de travail : ce qu'on sait de chaque transformation, source par source |

⚠️ **Chaque fiche déclare sa `convention_glucides`.** « Glucides » ne veut pas
dire la même chose partout : l'USDA publie *by difference*, fibres comprises ;
l'INCO les exclut. Comparer sans lire cette ligne, c'est comparer deux méthodes
et non deux produits.

⚠️ **Chaque fiche porte ses défauts dans ses `notes`.** Une donnée de référence
dont on tait les faiblesses n'en est pas une. Exemples en place : les AGS
incohérents du tempeh USDA, l'eau à 20 g de la graine norvégienne.

⚠️ **Un couple graine → tempeh doit venir d'une SEULE table.** Sinon on mesure
un écart de convention, pas une transformation.

⚠️ **Ne jamais caler un coefficient sur une composition de tempeh seule** : sans
savoir de quoi elle vient, elle ne prouve rien. Une tentative de ce genre a
produit des coefficients absurdes et a dû être annulée.

---

## Sources scientifiques — citer, toujours

⚠️ **Tout coefficient ou toute règle tirée d'une lecture cite sa source** par son
numéro dans `refs/references.md`, avec la page imprimée si possible :
`# [1, p. 80]: 12.2% of solids lost to soaking and cooking` dans le code,
« 12,2 % [1, p. 80] » dans la doc. Un chiffre sans source est une hypothèse,
et doit le dire.

⚠️ **Les titres des sources restent dans leur langue d'origine**, jamais
traduits — même dans une doc en français.

⚠️ **Un numéro ne se réattribue jamais.** Une source abandonnée reste dans
l'index, marquée *retirée*.

⚠️ **Ne citer un chiffre que d'une source LUE.** Si on n'a que le résumé,
on cite une tendance, pas un chiffre. Une étude citée par une autre se cite
comme telle : « Steinkraus 1964, cité dans [1, p. 80] ».

⚠️ **Les PDF vont dans `docs/`**, qui est ignoré par git : on ne les
redistribue pas.

⚠️ **L'ordre des sources pour un coefficient** (détail : `refs/methode.md`, § 3.2) :
1. **la littérature lue**, citée `[n, p. x]` ;
2. à défaut, **un calage sur les couples de `refs/official/`**, marqué comme tel,
   pour ce que la littérature laisse ouvert. Un couple ne cale **qu'une
   inconnue par nutriment**, et une perte absolue dépend du rendement supposé
   (1,75 [1, p. 80]) ;
3. à défaut, **une hypothèse**, écrite comme telle dans le code
   (`# HYPOTHESIS: …`).

Les analyses de laboratoire jugent le résultat ; elles ne comblent pas un trou.
Un coefficient calé sur `refs/official/` ne se « vérifie » pas contre ces
mêmes couples.

**L'objectif du projet :** des transformations valables pour **tous les
substrats** (légumineuses, céréales, oléagineux). Une règle doit donc porter
sur des fractions physiques (soluble ou non, amidon ou sucre), jamais sur
l'espèce : c'est la fiche de l'ingrédient qui porte la différence entre un soja
et une lentille (`refs/transformations.md`, § 2).

---

## Ce qui n'entre pas dans ce dépôt

⚠️ **Pas de serveur, pas de base de données, pas de port.** Si un besoin semble
l'exiger, c'est qu'il appartient à l'appelant. *(`web/` ne fait pas exception :
c'est une page statique, son serveur de développement est un outil de
construction — cf. § CORE et WEB.)*

⚠️ **Pas de dépendance nouvelle sans très bonne raison.** Seule PyYAML est là,
et uniquement pour la ligne de commande — `compute()` n'importe que la stdlib.
*(Vaut pour CORE. `web/` a les siennes, dans son `package.json`.)*

⚠️ **Aucune référence à l'infrastructure d'un consommateur** : pas de chemin de
déploiement, pas de nom de conteneur, pas de dépôt privé cité. Le dépôt est
public ; il décrit ce qu'il fait, pas qui l'utilise.

⚠️ **`docs/` est ignoré par git** : il contient des PDF de référence qu'on n'a
pas le droit de redistribuer.

---

## Tests

```bash
pip install -e ".[dev]" && pytest
```

Ils se lisent comme des affirmations sur le domaine, pas comme des
vérifications de code. Les valeurs épinglées viennent de sources nommées et
datées (`test_label.py` cite les tableaux de la Commission, `test_refs.py` les
couples publiés).

⚠️ `test_refs.py` se **skippe** si `refs/analyses/` ne contient rien de réel.
Il s'active de lui-même au premier fichier rempli — c'est voulu.
