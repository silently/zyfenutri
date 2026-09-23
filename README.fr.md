# zyfenutri

*English: [README.md](README.md)*

Le calcul qui transforme *ce qu'on a mis dans un lot de tempeh* en *ce qu'on a
le droit d'écrire sur l'étiquette*.

Une bibliothèque Python, un script, et une **page web** qui fait le même calcul
dans le navigateur : <https://silently.github.io/zyfenutri/>. Pas de serveur,
pas de base de données, pas de port à ouvrir.

## Pourquoi ce dépôt existe

Le règlement européen 1169/2011, en son **article 31 § 4**, met le **calcul** à
égalité avec l'analyse de laboratoire pour établir une déclaration
nutritionnelle. Encore faut-il que ce calcul soit *documenté et reproductible*.

D'où ce dépôt : des règles écrites, les données publiques qui les fondent, et un
moteur qui rend **la chaîne déroulée** de ce qu'il a fait — pour qu'elle soit
vérifiable, et contestable.

## Un document entre, un document sort

C'est tout le protocole. Le même document, que vous passiez par un fichier, par
un tube, ou par un appel Python.

```bash
zyfenutri lot.yml                 # le résultat en YAML, sur la sortie standard
zyfenutri lot.yml -o fiche.yml    # ou dans un fichier
cat lot.yml | zyfenutri           # ou par un tube
zyfenutri lot.yml --json          # ou en JSON, si c'est plus commode
```

```python
from zyfenutri import compute
resultat = compute({"harvested_g": 1750, "fermentation_hours": 36, "ingredients": [...]})
```

### Ce qu'on lui donne

```yaml
recipe: Tempeh de soja nature
harvested_g: 1750          # ce qu'on a PESÉ à la récolte
cooking_minutes: 30        # cuisson par défaut ; un intrant peut avoir la sienne
fermentation_hours: 36     # durée d'incubation

ingredients:
  - name: Soja
    role: substrate        # substrate · support · acid · soaking_acid · starter
    weight_g: 1000         # poids AVANT toute transformation, pellicule comprise
    dehulled: true         # dépelliculé : sa perte de masse est dans le rendement
    cooking_minutes: 45    # LA SIENNE — un soja et une lentille ne cuisent pas pareil,
                           #  et pas dans la même casserole. À défaut, celle du document.
    per_100g:
      fat: 20
      saturates: 2.9
      carbs: 15
      sugars: 5.7
      fibre: 15
      protein: 40
      salt: 0.01

  - name: Kinako
    role: support
    weight_g: 10
    roasted: true          # torréfié à l'atelier : fiche et poids de la farine CRUE
    per_100g: {fat: 20, saturates: 2.9, carbs: 15, sugars: 5.7, fibre: 15, protein: 40, salt: 0.01}

  - name: Vinaigre de cidre
    role: acid
    weight_g: 50
    per_100g: {fat: 0, saturates: 0, carbs: 0.93, sugars: 0.4, fibre: 0, protein: 0, salt: 0.013}

  - name: Starter
    role: starter          # exclu du calcul : quelques grammes pour des kilos
```

Les compositions sont **pour 100 g**, dans l'unité de la table dont vous les
tirez.

⚠️ **Ce qui manque ne bloque pas le calcul, mais rend inconnu ce qui en dépend.**
Un ingrédient sans composition ou sans poids, une durée absente, une
transformation qui ne sait pas encore traiter un nutriment : la valeur du
produit ressort `null`, et `missing` dit pourquoi. **Jamais de zéro, jamais de
somme partielle.**

> **Sans pesée ?** Omettez `harvested_g` et donnez un `yield: 1.75` au substrat :
> le poids de tempeh sera **prédit**. C'est ce qui permet de chiffrer une recette
> avant de l'avoir faite. ⚠️ Le résultat est alors marqué `complete: false` — on
> n'étiquette pas un produit avec un dénominateur lui-même estimé.

### Ce qu'il rend

```yaml
recipe: Tempeh de soja nature
harvested_g: 1750
complete: true             # toutes les valeurs sont connues (voir l'état actuel plus bas)

per_100g:                  # les valeurs calculées ; null = inconnu
  fat: 9.99
  saturates: 2.24
  carbs: 5.19
  sugars: 1.4
  fibre: 4.36
  protein: 20.28
  salt: 0.01
  energy_kj: 837.6
  energy_kcal: 200.5

label:                     # les mêmes, telles qu'elles s'écrivent
  energy: 838 kJ / 201 kcal
  energy_kj: 838 kJ        # aussi séparées, pour qui les stocke en deux champs
  energy_kcal: 201 kcal
  fat: 10,0 g
  saturates: 2,2 g
  carbs: 5,2 g
  sugars: 1,4 g
  fibre: 4,4 g
  protein: 20 g
  salt: < 0,01 g

steps:                     # la fiche de calcul, à montrer si on la conteste
  - "Apport de chaque intrant : masse pesée × composition pour 100 g (3 intrants)"
  - "Soja : Dépelliculage → Trempage (une nuit) → Cuisson 30 min → Fermentation 36 h"
  - "Kinako : Torréfaction → Fermentation 36 h"
  - "Vinaigre de cidre : tel quel"
  - "Ramené à 100 g de produit fini : ÷ 1750 g récoltés. C'est cette division qui porte l'eau reprise"
  - "Énergie calculée depuis les macros (annexe XIV), jamais recopiée"

missing: []                # ce qui empêche d'étiqueter, en clair — ici, rien
warnings: []               # ce qui n'empêche pas, mais mérite un œil
coefficients: {...}        # chaque coefficient des transformations ; null = lacune
```

## Ce que le moteur fait

Il applique à chaque ingrédient les transformations qu'il subit réellement,
en restant rapporté à **100 g d'ingrédient brut**, puis divise **une seule
fois** par le poids de tempeh.

> ⚠️ C'est cette division finale, et elle seule, qui porte l'eau reprise au
> trempage. Un lot qui double de poids en s'hydratant voit toutes ses valeurs
> divisées par deux, sans qu'aucun coefficient n'ait à le dire. Ajouter un
> « facteur d'hydratation » par-dessus compterait l'eau deux fois.

| `role` | Transformations |
|---|---|
| `substrate` | dépelliculage *(si `dehulled`)* → trempage *(toujours une nuit, 10 à 15 h)* → cuisson → fermentation |
| `support` | torréfaction *(si `roasted`)* → fermentation |
| `acid` | aucune — ajouté après cuisson, compté au prorata de sa masse |
| `soaking_acid` | **exclu** — il part avec l'eau de trempage, qui est jetée |
| `starter` | **exclu** — quelques grammes pour plusieurs kilos |

Les deux exclusions **sous-déclarent** légèrement le produit : c'est le sens
prudent, celui qui n'expose pas.

⚠️ **`roasted: true`, c'est vous qui torréfiez.** On donne alors la fiche et le
poids du produit **cru** : la torréfaction retire 8 % des sucres et 16 % des
fibres (`refs/methode.md`, T3). Un kinako **acheté** est déjà torréfié, et sa
fiche le dit : il s'entre avec `roasted: false`, sinon la torréfaction compte
deux fois. La perte d'eau, elle, ne change rien au calcul : elle est dans la
pesée finale.

Les coefficients ne se passent plus dans le document : chacun vit dans
`zyfenutri/transforms.py`, avec sa source ou la mention d'une lacune. Ce qu'on
sait de chaque transformation, et ce qui manque, est dans
**[`refs/transformations.md`](refs/transformations.md)**. La méthode et le droit
sont dans **[`refs/methode.md`](refs/methode.md)**, le document qu'on présente à
un contrôle.

> ⚠️ **État actuel.** Un tempeh de soja décrit en entier (durées, poids,
> fiches) sort complet, comme l'exemple ci-dessus. Plusieurs coefficients
> restent des hypothèses, et
> aucun n'est encore validé par une analyse de laboratoire
> (`refs/transformations.md`, § 0). Ce qui est à affiner, ce qui manque,
> et les trois publications à obtenir en priorité :
> `refs/transformations.md`, § 0 bis.

## Pour qui écrit du code

Le calcul repose sur trois briques — la **fiche** (`NutritionFacts`), la
**transformation** (`Transform`) et le **mélange** (`mix`). Leurs types, leurs
signatures et ce qui les justifie sont dans
**[`ARCHITECTURE.md`](ARCHITECTURE.md)**.

## Les données de référence

`refs/official/` contient des compositions **publiées par des tables
nationales**, recopiées telles quelles : trois couples graine → tempeh (USDA,
Nouvelle-Zélande, Norvège) qui servent à caler les coefficients.

> ⚠️ Chaque fiche déclare sa **convention de glucides** et porte ses défauts dans
> ses `notes`. Une donnée de référence dont on tait les faiblesses n'en est pas
> une.

`refs/analyses/` accueille des analyses de laboratoire, s'il en arrive.

```bash
python check.py      # confronte les analyses au calcul — ne modifie rien
```

## Ce que ce dépôt ne fait pas

Il **ne décide pas** : il applique des règles à des données qu'on lui donne.

Il **ne connaît aucun produit** : ni recette, ni fournisseur, ni lot. On lui
passe des masses et des compositions, il rend des valeurs pour 100 g.

Il **ne lève jamais d'exception sur une donnée manquante** : il le dit dans
`missing`, et `complete` répond à la seule question qui compte — est-ce que ça
peut aller sur un emballage ?

## La version web

<https://silently.github.io/zyfenutri/> — une page statique, sans back end. On
y saisit le document dans des champs, elle rend l'étiquette, et le document
comme la fiche de calcul se téléchargent en `.yml` ou en `.json`.

⚠️ **C'est le même code Python**, exécuté par [Pyodide](https://pyodide.org)
dans le navigateur — pas une réécriture en JavaScript. Une seule implémentation
des règles, donc la page ne peut pas dire autre chose que la ligne de commande.

Elle pose une question que la bibliothèque laisse ouverte : **le poids de
tempeh**. La page n'a pas de champ « poids récolté » — elle le **prédit**
toujours par le facteur de rendement, qui y est donc obligatoire. Une étiquette
porte une valeur moyenne, pas celle d'une fournée. Le détail de ce choix, et ce
qu'il implique, est dans [`refs/methode.md`](refs/methode.md) § 3.3.

Son aide en ligne (« Comment ça marche ») est la **documentation utilisateur**
de cette page ; `refs/methode.md` reste la référence de la méthode et du droit.

Le code est dans [`web/`](web/) et n'entre jamais dans celui du moteur.

## Installation et tests

```bash
pip install -e ".[dev]" && pytest
```

Seule dépendance : **PyYAML**, et uniquement pour lire et écrire du YAML en
ligne de commande. `compute()` n'importe que la bibliothèque standard.

## Licence

MIT.
