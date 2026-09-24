# Architecture — les trois briques du calcul

Le calcul d'une étiquette se ramène à trois concepts : une **fiche**, des
**transformations** que subit chaque ingrédient, et un **mélange** qui en fait
un produit. Ce document fixe leurs types et leurs signatures, et dit pourquoi.

> Ce document s'adresse à qui écrit du code. La justification réglementaire et
> nutritionnelle — d'où viennent les coefficients, ce qu'ils valent — reste dans
> [`refs/methode.md`](refs/methode.md), qui est le document qu'on présente à un contrôle.

```
  fiche brute ──► transformation ──► transformation ──► … ──► fiche préparée ─┐
  fiche brute ──► transformation ──► … ─────────────────────► fiche préparée ─┼─► mélange ──► fiche du produit
  fiche brute (vinaigre, aucune transformation) ────────────► fiche préparée ─┘
```

---

## 1. La fiche — `NutritionFacts`

```python
@dataclass(frozen=True, slots=True, kw_only=True)
class NutritionFacts:
    fat: float | None = None        # Matières grasses
    saturates: float | None = None  # dont acides gras saturés
    carbs: float | None = None      # Glucides (assimilables, fibres exclues)
    sugars: float | None = None     # dont sucres
    fibre: float | None = None      # Fibres alimentaires
    protein: float | None = None    # Protéines
    salt: float | None = None       # Sel
```

Module : `zyfenutri/nutrients.py`. Toutes les valeurs sont en **grammes pour 100 g**.

| Choix | Pourquoi |
|---|---|
| **`dataclass`**, pas un `dict` | les sept noms sont vérifiés à la construction : `NutritionFacts(proteines=…)` lève une erreur, là où une clé mal orthographiée dans un `dict` serait ignorée en silence |
| **`frozen=True`** | une fiche ne se modifie pas : une transformation en **rend une nouvelle**. On peut donc garder la fiche brute et la fiche préparée côte à côte sans qu'elles se contaminent |
| **`kw_only=True`** | sept `float` à la suite, c'est une inversion lipides / glucides qui passe inaperçue. On impose de nommer |
| **`float \| None`**, `None` par défaut | **une valeur absente n'est jamais un zéro**. `None` veut dire « on ne sait pas » et se propage dans tout le calcul ; `0.0` affirme qu'il n'y en a pas |
| **aucune validation à la construction** | une fiche incohérente doit pouvoir exister le temps qu'on la signale. `checks.check(fiche.as_dict())` dit si elle est physiquement possible |
| **mêmes noms que le contrat d'entrée** | `NutritionFacts.from_mapping(...)` lit un bloc `per_100g:` avec tous ses alias (`fat_g`, `proteines`…) |

Méthodes :

| Signature | Rend |
|---|---|
| `NutritionFacts.from_mapping(raw: Mapping \| None) -> NutritionFacts` | une fiche lue depuis un document, alias acceptés, clés inconnues ignorées |
| `fiche.as_dict() -> dict[str, float \| None]` | les sept valeurs, dans l'ordre de l'étiquette |
| `fiche.unknown -> tuple[str, ...]` | les noms des valeurs inconnues |

### L'énergie ne se stocke pas

```python
def energy_of(facts: NutritionFacts, unit: Literal["kJ", "kcal"] = "kJ") -> float | None
```

Module : `zyfenutri/label.py`.

**Oui, l'énergie se calcule toujours depuis la fiche.** L'annexe XIV la tire de
quatre des sept valeurs : matières grasses, glucides, protéines, fibres. La
stocker permettrait qu'elle diverge des macronutriments, et c'est la première
chose qu'un contrôleur recoupe.

- **Deux unités, deux jeux de coefficients.** Les kcal ne sont **pas** les
  kJ ÷ 4,184 : l'annexe XIV donne des coefficients propres à chaque unité.
- **`None` si l'un des quatre macronutriments est inconnu.** Une énergie à
  laquelle il manque un nutriment serait fausse, et elle aurait l'air juste.
- **Pas d'arrondi.** L'arrondi est une affaire d'étiquette (`declared`), pas de calcul.

⚠️ **La limite, pour être exact :** l'annexe XIV compte aussi les **acides
organiques**, les **polyols** et l'**alcool**, qui ne sont pas sur la fiche.
Pour un tempeh, c'est négligeable : 50 g de vinaigre dans 1,75 kg de produit
apportent environ 2 kJ pour 100 g. Pour un produit sucré aux polyols ou très
acide, les sept valeurs ne suffiraient plus.

---

## 2. La transformation — `Transform`

*Le nom.* « Étape de fabrication » devient **transformation**. C'est le mot
qu'emploient déjà `refs/methode.md` (T1 à T5) et la fiche de calcul
(`steps`) : le changer aurait fait deux vocabulaires pour une seule chose. En
code : `Transform`.

```python
class Transform(Protocol):
    @property
    def label(self) -> str: ...                                   # en français, pour la fiche de calcul
    def __call__(self, facts: NutritionFacts, /) -> NutritionFacts: ...
```

Module : `zyfenutri/transforms.py`. Une fiche entre, une fiche sort.

### ⚠️ La base ne change jamais : 100 g d'ingrédient **brut**

C'est **le** choix structurant de cette architecture.

Une fiche qui sort d'une transformation ne décrit **pas** « 100 g de soja
trempé ». Elle décrit **ce qui reste des nutriments contenus dans 100 g de
soja tel qu'il a été pesé au départ**. Le trempage fait perdre des glucides :
la valeur baisse. Le trempage fait gagner de l'eau : **rien ne bouge**, car
l'eau n'est pas un nutriment et la base reste 100 g de brut.

Conséquences :

- **Une transformation ne touche jamais à l'eau** et ne connaît pas la masse du
  produit. Elle ne fait que retirer — ou, exceptionnellement, ajouter — des
  grammes de nutriments.
- **La seule division par la masse de produit a lieu au mélange** (§ 3).
  Appliquer un facteur d'hydratation dans une transformation compterait l'eau
  **deux fois**. C'est l'erreur que ce découpage rend impossible par
  construction.
- C'est exactement le modèle « masses absolues » du moteur, ramené à 100 g de
  brut. Le test `test_the_building_blocks_agree_with_the_engine` le vérifie.

⚠️ **Le piège, du coup :** une fiche fournisseur de soja **déjà cuit** n'est pas
une fiche brute. La passer dans un trempage ferait subir les pertes deux fois.

### Les transformations à paramètre

La cuisson dépend de sa durée, la fermentation aussi. Le paramètre **ne
s'ajoute pas à l'appel** : une **fabrique** le reçoit et rend une transformation
toute prête.

```python
def cooking(minutes: float) -> Transform: ...   # la fabrique
def fermentation(hours: float) -> Transform: ...

pipeline: list[Transform] = [Dehulling(), Soaking(), cooking(minutes=30), fermentation(hours=36)]
prepared = process(raw, pipeline)
```

| Pourquoi une fabrique | |
|---|---|
| **une seule signature** à l'exécution | `(NutritionFacts) -> NutritionFacts`, quelle que soit la transformation. Une chaîne n'est qu'une liste, et `process` n'a pas à savoir quels réglages existent |
| **le réglage est lié une fois** | la durée est fixée à la construction, visible dans `label` (« Cuisson 30 min (égouttage compris) »), et la chaîne se relit telle qu'elle a été appliquée |
| **une transformation sans paramètre** | est une fabrique sans argument, ou une constante |

Les transformations réelles, et la manière dont leurs pertes dépendent de la
durée, sont **à décrire**. Elles viendront s'écrire comme des fabriques.

### `Retention` — le cas courant

La plupart des transformations multiplient chaque nutriment par son propre
facteur. `Retention` fait exactement ça :

```python
@dataclass(frozen=True, slots=True)
class Retention:
    label: str
    factors: Mapping[str, float]    # nutriment -> fraction CONSERVÉE (1.0 = rien ne part)
```

- **Un facteur est une fraction conservée**, pas un pourcentage de perte :
  `0.5` garde la moitié. On multiplie, on ne soustrait pas.
- **Un nutriment absent de `factors` ne bouge pas.**
- **Un « dont » non listé suit son total** : perdre 5 % des lipides fait perdre
  5 % des AGS. Sans cette règle, les AGS pourraient passer au-dessus des
  lipides. On peut toujours donner un facteur propre au « dont » (la
  torréfaction ne touche que les sucres).
- **Une valeur inconnue reste inconnue** : `None × 0,5` reste `None`.
- Un nom inconnu ou un facteur négatif lève `ValueError` **à la construction**,
  pas au milieu d'un calcul.

Une transformation qui n'est **pas** une simple multiplication implémente
directement le protocole. Le dépelliculage en est une : la pellicule emporte
surtout des fibres, ce qui est une soustraction, pas un facteur commun.

```python
def process(facts: NutritionFacts, transforms: Iterable[Transform]) -> NutritionFacts
```

`process` applique les transformations dans l'ordre. Une liste vide rend la fiche telle quelle.

---

## 3. Le mélange — `Portion` et `mix`

Module : `zyfenutri/mixing.py`.

```python
@dataclass(frozen=True, slots=True)
class Portion:
    facts: NutritionFacts       # fiche préparée, toujours pour 100 g de BRUT
    raw_mass: float             # masse brute engagée
    yield_factor: float = 1.0   # masse de produit / masse brute, sur toutes ses transformations

def mix(portions: Iterable[Portion], *, product_mass: float | None = None) -> NutritionFacts
```

Le calcul, pour chaque nutriment :

```
                      Σ  raw_mass × facts.nutriment / 100
valeur pour 100 g  =  ───────────────────────────────────  × 100
                      masse de produit

masse de produit   =  product_mass, si on l'a pesée
                   =  Σ  raw_mass × yield_factor, sinon
```

| Choix | Pourquoi |
|---|---|
| **le facteur de rendement est porté par la portion** | chaque ingrédient a le sien : un substrat trempé double de poids, un substrat dépelliculé en perd d'abord, un vinaigre n'en a pas (`1.0`) |
| **il absorbe tout ce qui change la masse** | pertes au dépelliculage, eau reprise au trempage et à la cuisson, eau perdue à l'incubation. C'est pourquoi aucune transformation n'a à s'en occuper (détail ci-dessous) |
| **`raw_mass` accepte une proportion** | des grammes, ou un ratio de recette (`100`, `5`…), du moment que toutes les portions ont la même unité |
| **`product_mass`, si on a pesé** | une pesée l'emporte sur une prédiction. Elle doit alors être dans la même unité que les masses brutes, donc en grammes |
| **un nutriment inconnu pour une portion est inconnu pour le mélange** | additionner les autres traiterait le manque comme un zéro |
| **`ValueError` si la masse de produit est nulle** | il n'y a rien à ramener à 100 g |

### Le facteur de rendement : un seul facteur pour tout

```
yield_factor  =  masse de l'ingrédient dans le produit fini
                 ────────────────────────────────────────────
                 masse brute pesée AVANT toute transformation
```

**Un seul facteur par ingrédient**, du grain sec au tempeh récolté. Il agrège
d'un coup tout ce qui fait varier la **masse** en cours de route :

| Effet | Sens | Quand |
|---|---|---|
| **Pertes de matière**, si l'ingrédient est dépelliculé : pellicule, germe, débris | ↓ | dépelliculage — **optionnel** : sans dépelliculage, pas de perte |
| **Hydratation** au trempage | ↑↑ | trempage |
| **Hydratation** à la cuisson | ↑ ou ≈ | cuisson |
| **Légère perte d'eau** pendant l'incubation | ↓ | fermentation |

Un exemple chiffré, pour 1 livre de soja entier [1, p. 80, citant Steinkraus et al. 1961] :

```
grain sec   trempé    dépelliculé   cuit     tempeh
  1,00   →   2,33   →    2,02    →  1,90  →   1,74      yield_factor = 1,74
          hydratation  pellicule   ─┬─     perte d'eau
                                    └── eau de cuisson égouttée
```

La baisse à l'incubation est faible : il faut environ 8,3 onces de graines
inoculées pour 8 onces de tempeh, « surtout par perte d'humidité » [1, p. 80].
En pratique, 1 livre de soja entier donne en moyenne 1,75 livre de tempeh
[1, p. 80].

⚠️ **Ce qu'on ne fait JAMAIS :**

- **découper le facteur par transformation** (« ×2,33 au trempage, ×0,87 au
  dépelliculage… ») et le faire porter aux transformations. Elles ne
  connaissent pas la masse (§ 2) ;
- **l'appliquer deux fois** : il n'entre qu'au mélange, dans la division. Le
  multiplier ailleurs compterait l'eau deux fois ;
- **le mesurer à partir d'un poids intermédiaire** : poids trempé, poids
  dépelliculé. La base, c'est le **poids brut avant toute transformation**,
  celui de `raw_mass`.

⚠️ **Masse et nutriments ne se confondent pas.** Le dépelliculage apparaît à deux
endroits, et ce n'est pas un double comptage :

| | porté par | exemple |
|---|---|---|
| la **masse** de pellicule perdue | le facteur de rendement | 9 g sur 100 g de graine |
| les **nutriments** partis avec elle | la transformation « dépelliculage » | surtout des fibres |

Le facteur de rendement dit **combien pèse** le produit ; les transformations
disent **ce qu'il contient**. On divise l'un par l'autre, une fois.

### Les trois cas cités

| Ingrédient | Transformations | `yield_factor` |
|---|---|---|
| **Vinaigre de cidre** | aucune : `process(fiche, [])` rend la fiche telle quelle | `1.0` |
| **Substrat non dépelliculé** | trempage et cuisson → fermentation | le sien, par exemple `1.75` |
| **Substrat dépelliculé** | dépelliculage → trempage et cuisson → fermentation | le sien, mesuré **depuis le poids brut avant dépelliculage** |

---

## 4. Les transformations et la recette

### Les cinq transformations

| Classe | Réglage | Connu aujourd'hui |
|---|---|---|
| `Dehulling()` | aucun : pellicule typique du soja, 9 % ; sa **masse** est dans le facteur de rendement | tout |
| `Soaking()` | aucun : toujours **une nuit, 10 à 15 h** | tout |
| `Cooking(minutes)` | durée en minutes | tout |
| `Fermentation(hours)` | durée en heures | tout jusqu'à 48 h ; protéines jusqu'à 72 h |
| `Roasting()` | aucun : torréfié ou non | tout — sucres −8 %, fibres −16 %, le reste inchangé |

Chacune est une `dataclass` gelée qui satisfait `Transform` : le réglage est
un champ, l'appel prend une fiche et en rend une.

⚠️ **Une lacune est `None`.** Chaque coefficient est une constante du module,
annotée de son origine : une source `[n, p. x]`, `HYPOTHESIS` ou `GAP`. Une
lacune vaut `None`, et le nutriment ressort **inconnu**. Tant que les lacunes
existent, un nutriment qui en traverse une ressort inconnu : c'est voulu.
Combler une lacune se fait en changeant une constante.

Le trempage est toujours **une nuit (10 à 15 h)** : ce n'est pas un réglage,
et ses coefficients sont des parts conservées après une nuit. Les pertes à la
cuisson ont la forme `conservé = 1 − perte_max × (1 − e^(−t/τ))` (`retained`).
Dans les deux cas, les glucides sont découpés en sucres et amidon
(`split_carbs`).

### La recette — `Ingredient` et `Recipe`

Module : `zyfenutri/recipe.py`.

```python
@dataclass(frozen=True, slots=True, kw_only=True)
class Ingredient:
    name: str
    facts: NutritionFacts                 # fiche brute, telle que pesée
    raw_mass: float
    transforms: tuple[Transform, ...] = ()
    yield_factor: float = 1.0

@dataclass(frozen=True, slots=True, kw_only=True)
class Recipe:
    name: str
    ingredients: tuple[Ingredient, ...]
    product_mass: float | None = None     # si le produit a été pesé

    def facts(self) -> NutritionFacts     # process() par ingrédient, puis mix()
    def steps(self) -> list[str]          # la chaîne, en français
```

La recette n'ajoute aucune règle : elle nomme les pièces et les enchaîne.

---

## 5. Ce qui reste à faire

- **Combler les lacunes** (`GAP`) des transformations, source par source
  (`refs/transformations.md`, `docs/A-LIRE.md`).
- **`compute()` repose sur `Recipe`.** Le document d'entrée
  se lit en `Ingredient` (rôle → transformations, réglages → paramètres), et
  un réglage absent devient une étape `Unknown`, qui rend tout inconnu.
