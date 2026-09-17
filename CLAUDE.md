# zyfenutri — CLAUDE.md

Le calcul qui transforme *ce qu'on a mis dans un lot de tempeh* en *ce qu'on a
le droit d'écrire sur l'étiquette*. Bibliothèque Python + script. Dépôt
**public**.

---

## 🗣️ Langue — RÈGLE STRICTE

| Quoi | Langue |
|---|---|
| Les `.md` (README, méthode, ce fichier), les messages de commit | **français** |
| Les commentaires et docstrings **dans le code** | **anglais** |
| Les messages rendus à l'utilisateur (`steps`, libellés d'étiquette) | **français** |

⚠️ Le dépôt est public et le code a vocation à être lu par des gens qui ne
parlent pas français. La **documentation**, elle, s'adresse d'abord à
l'exploitation qui s'en sert, et au contrôle sanitaire français.

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

⚠️ **Personne n'utilise encore ce contrat** : il peut évoluer librement. La
version suit le versionnage sémantique (correctif, ajout compatible, rupture),
dans `pyproject.toml` et `zyfenutri/__init__.py`. Dès qu'un consommateur existera, ajouter une clé de sortie
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

⚠️ **Les « dont » suivent leur total.** Les AGS n'ont pas de règle propre, les
sucres non plus au-delà de celle des glucides. Une valeur « dont » supérieure à
son total n'a aucun sens physique.

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
l'exiger, c'est qu'il appartient à l'appelant.

⚠️ **Pas de dépendance nouvelle sans très bonne raison.** Seule PyYAML est là,
et uniquement pour la ligne de commande — `compute()` n'importe que la stdlib.

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
