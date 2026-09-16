# zyfenutri

Le calcul qui transforme *ce qu'on a mis dans un lot de tempeh* en *ce qu'on a
le droit d'écrire sur l'étiquette*.

Une bibliothèque Python et un script. Pas de serveur, pas de base de données,
pas de port à ouvrir.

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
resultat = compute({"harvested_g": 1750, "ingredients": [...]})
```

### Ce qu'on lui donne

```yaml
recipe: Tempeh de soja nature
harvested_g: 1750          # ce qu'on a PESÉ à la récolte

ingredients:
  - name: Soja
    role: substrate        # substrate · support · acid · soaking_acid · starter
    weight_g: 1000         # poids net, celui qui part au trempage
    raw_weight_g: 1100     # facultatif — l'écart avec le net est la pellicule
    dehulled: true
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
    roasted: true
    per_100g: {fat: 25, saturates: 3.6, carbs: 14, sugars: 10, fibre: 18, protein: 37, salt: 0.01}

  - name: Vinaigre de cidre
    role: acid
    weight_g: 50
    per_100g: {fat: 0, saturates: 0, carbs: 0.93, sugars: 0.4, fibre: 0, protein: 0, salt: 0.013}

  - name: Starter
    role: starter          # exclu du calcul : quelques grammes pour des kilos
```

Tout est facultatif sauf `role`, `weight_g` et `per_100g`. Les compositions sont
**pour 100 g**, dans l'unité de la table dont vous les tirez.

> **Sans pesée ?** Omettez `harvested_g` et donnez un `yield: 1.75` au substrat :
> le poids de tempeh sera **prédit**. C'est ce qui permet de chiffrer une recette
> avant de l'avoir faite. ⚠️ Le résultat est alors marqué `complete: false` — on
> n'étiquette pas un produit avec un dénominateur lui-même estimé.

### Ce qu'il rend

```yaml
recipe: Tempeh de soja nature
harvested_g: 1750
complete: true

per_100g:                  # les valeurs calculées
  energy_kj: 886.2
  protein: 22.35
  ...

label:                     # les mêmes, telles qu'elles s'écrivent
  energy: 886 kJ / 213 kcal
  protein: 22 g
  salt: < 0,01 g
  ...

steps:                     # la fiche de calcul, à montrer si on la conteste
  - "Apport de chaque intrant : masse pesée × composition pour 100 g (3 intrants)"
  - "T2a · Trempage et cuisson (substrats) : −50 % de glucides, …"
  - "T5 · Ramené à 100 g : ÷ 1750 g récoltés. C'est cette division qui porte l'eau"

missing: []                # ce qui empêche d'étiqueter, en clair
warnings: []               # ce qui n'empêche pas, mais mérite un œil
```

## Ce que le moteur fait

Il ne manipule que des **masses absolues de nutriments**, du début à la fin. Il
applique à chaque ingrédient les transformations qu'il subit réellement, puis
divise **une seule fois** par le poids de tempeh.

> ⚠️ C'est cette division finale, et elle seule, qui porte l'eau reprise au
> trempage. Un lot qui double de poids en s'hydratant voit toutes ses valeurs
> divisées par deux, sans qu'aucun coefficient n'ait à le dire. Ajouter un
> « facteur d'hydratation » par-dessus compterait l'eau deux fois.

| `role` | Transformations |
|---|---|
| `substrate` | dépelliculage *(si les deux poids sont donnés)* → trempage et cuisson → fermentation |
| `support` | torréfaction *(si `roasted`)* → fermentation |
| `acid` | aucune — ajouté après cuisson, compté au prorata de sa masse |
| `soaking_acid` | **exclu** — il part avec l'eau de trempage, qui est jetée |
| `starter` | **exclu** — quelques grammes pour plusieurs kilos |

Les deux exclusions **sous-déclarent** légèrement le produit : c'est le sens
prudent, celui qui n'expose pas.

Les sept coefficients de perte ont des valeurs par défaut, et s'écrasent :

```yaml
coefficients:
  leaching_carbs: 45       # au lieu de 50
```

Le détail — règles nutriment par nutriment, ce qui fonde chaque coefficient, et
les réserves assumées — est dans **[`refs/methode.md`](refs/methode.md)**. C'est
ce document-là qu'on présente à un contrôle, pas ce README.

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

## Installation et tests

```bash
pip install -e ".[dev]" && pytest
```

Seule dépendance : **PyYAML**, et uniquement pour lire et écrire du YAML en
ligne de commande. `compute()` n'importe que la bibliothèque standard.

## Licence

MIT.
