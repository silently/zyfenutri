# zyfenutri

**zyfenutri** — le calcul qui transforme *ce qu'on a mis dans un
lot de tempeh* en *ce qu'on a le droit d'écrire sur l'étiquette*.

Une bibliothèque Python **sans aucune dépendance**, et un script. Pas de
serveur, pas de base de données, pas de port à ouvrir.

## Pourquoi ce dépôt existe

Le règlement européen 1169/2011, en son **article 31 § 4**, met le **calcul** à
égalité avec l'analyse de laboratoire pour établir une déclaration
nutritionnelle. Encore faut-il que ce calcul soit *documenté et reproductible*.

C'est exactement ce que ce dépôt fournit : des règles écrites, les données
publiques qui les fondent, et un moteur qui rend **la chaîne déroulée** de ce
qu'il a fait — pour qu'elle soit vérifiable, et contestable.

## En bibliothèque

```python
from zyfenutri import estimate, declared_values

resultat = estimate(
    harvest_weight_g=1750,
    ingredients=[{
        "input_type_name": "Soja",
        "category": "substrate",
        "net_weight_g": 1000,
        "gross_weight_g": 1100,     # dépelliculé : l'écart donne la pellicule
        "dehulled": True,
        "composition": {            # pour 100 g, tels que la fiche les donne
            "fat_g": 20.0, "saturates_g": 2.9, "carbohydrates_g": 15.0,
            "sugars_g": 5.7, "fibre_g": 15.0, "protein_g": 40.0, "salt_g": 0.01,
        },
    }],
)
print(resultat.per_100g, resultat.energy_kj)
print("\n".join(resultat.steps))      # la fiche de calcul
```

## En script

```bash
echo '{"harvest_weight_g": 1750, "ingredients": [...]}' | python -m zyfenutri
```

Du JSON entre sur l'entrée standard, du JSON sort sur la sortie standard. C'est
tout le protocole : **aucun HTTP**, aucun état, aucun démon. Le découplage est
celui du système d'exploitation.

Codes de sortie : `0` calcul abouti, `2` entrée invalide.

## Ce que le moteur fait

Il ne manipule que des **masses absolues de nutriments**, du début à la fin. Il
applique à chaque ingrédient les transformations qu'il subit réellement, puis
divise **une seule fois** par le poids de tempeh obtenu.

> ⚠️ Ce dernier point est la clé : c'est cette division finale, et elle seule,
> qui porte l'eau reprise au trempage. Un lot qui double de poids en
> s'hydratant voit toutes ses valeurs divisées par deux, sans qu'aucun
> coefficient n'ait à le dire. Ajouter un « facteur d'hydratation » par-dessus
> compterait l'eau deux fois.

| Ingrédient | Transformations |
|---|---|
| **Substrat** | dépelliculage *(si pesé)* → trempage et cuisson → fermentation |
| **Support d'inoculation** | torréfaction *(si pratiquée)* → fermentation |
| **Acidifiant pré-inoculation** | aucune — compté au prorata |
| **Acidifiant de trempage**, **starter** | exclus |

Chaque transformation est une **fonction pure** avec une règle par nutriment.
Le détail, ce qui le fonde et les réserves assumées sont dans
[`refs/methode.md`](refs/methode.md).

## Les données de référence

`refs/official/` contient des compositions **publiées par des tables
nationales**, recopiées telles quelles — trois couples graine → tempeh (USDA,
Nouvelle-Zélande, Norvège) qui servent à caler les coefficients.

> ⚠️ Chaque fiche déclare sa **convention de glucides** et porte ses défauts
> dans ses `notes`. Une donnée de référence dont on tait les faiblesses n'en
> est pas une.

`refs/analyses/` accueille des analyses de laboratoire, s'il en arrive.

```bash
python check.py      # confronte les analyses au calcul, ne modifie rien
```

## Ce que ce dépôt ne fait pas

Il **ne décide pas**. Il applique des règles à des données qu'on lui donne. Les
coefficients ont des valeurs par défaut documentées, et l'appelant peut les
remplacer (`coefficients=`) — c'est à lui de savoir pourquoi.

Il **ne connaît aucun produit** : ni recette, ni fournisseur, ni lot. On lui
passe des masses et des compositions, il rend des valeurs pour 100 g.

## Tests

```bash
pip install -e ".[dev]" && pytest
```

## Licence

MIT.
