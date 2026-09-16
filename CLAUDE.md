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
compute({"harvested_g": 1750, "ingredients": [...]}) -> dict
```
```bash
zyfenutri lot.yml
```

⚠️ **Des dépôts privés dépendent de ce contrat.** Ajouter une clé de sortie est
sans risque ; en renommer une, en supprimer une, ou changer le sens d'un rôle
casse des consommateurs qu'on ne voit pas d'ici. Si c'est nécessaire, c'est une
version majeure.

⚠️ **Les noms longs restent acceptés en entrée** (`fat_g` → `fat`, cf.
`nutrients.ALIASES`). C'est ce qui évite à un appelant d'écrire une couche de
traduction. Ne pas les retirer.

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

## Architecture — six modules courts

| Module | Ce qu'il porte | Ce qu'il ne doit PAS porter |
|---|---|---|
| `nutrients.py` | les 7 noms, les libellés, les alias d'entrée | aucune règle de calcul |
| `label.py` | annexe XIV, arrondis (tableau 4), tolérances (tableau 1) | rien de spécifique au tempeh |
| `checks.py` | bornes physiques, bouclage de masse | rien de réglementaire |
| `transforms.py` | les coefficients et les 5 transformations, en **fonctions pures** | aucune I/O, aucun état |
| `engine.py` | l'enchaînement : document → document | aucune règle nutriment par nutriment |
| `__main__.py` | la ligne de commande | aucun calcul |

⚠️ **Chaque transformation est une fonction pure** : masses en entrée, masses en
sortie. Si une transformation a besoin de savoir *quel* ingrédient elle traite,
c'est que la règle est mal placée.

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
