# zyfenutri

*Version française : [README.fr.md](README.fr.md)*

The calculation that turns *what went into a batch of tempeh* into *what may be
written on the label*.

A Python library and a script. No server, no database, no port to open.

## Why this repository exists

European Regulation 1169/2011, in its **Article 31(4)**, puts **calculation** on
an equal footing with laboratory analysis for establishing a nutrition
declaration. The calculation still has to be *documented and reproducible*.

Hence this repository: written rules, the public data behind them, and an
engine that returns **the full chain** of what it did — so that it can be
checked, and argued with.

## One document in, one document out

That is the whole protocol. The same document, whether you go through a file,
a pipe, or a Python call.

```bash
zyfenutri batch.yml                 # the result as YAML, on standard output
zyfenutri batch.yml -o sheet.yml    # or in a file
cat batch.yml | zyfenutri           # or through a pipe
zyfenutri batch.yml --json          # or as JSON, if that is handier
```

```python
from zyfenutri import compute
result = compute({"harvested_g": 1750, "fermentation_hours": 36, "ingredients": [...]})
```

### What goes in

```yaml
recipe: Plain soy tempeh
harvested_g: 1750          # what was WEIGHED at harvest
cooking_minutes: 30        # cooking time of the substrates
fermentation_hours: 36     # incubation time

ingredients:
  - name: Soybeans
    role: substrate        # substrate · support · acid · soaking_acid · starter
    weight_g: 1000         # weight BEFORE any transform, hulls included
    dehulled: true         # dehulled: its loss of mass is in the yield
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
    roasted: true          # roasted in-house: sheet and weight of the RAW flour
    per_100g: {fat: 20, saturates: 2.9, carbs: 15, sugars: 5.7, fibre: 15, protein: 40, salt: 0.01}

  - name: Cider vinegar
    role: acid
    weight_g: 50
    per_100g: {fat: 0, saturates: 0, carbs: 0.93, sugars: 0.4, fibre: 0, protein: 0, salt: 0.013}

  - name: Starter
    role: starter          # left out: a few grams for several kilos
```

Compositions are **per 100 g**, in the unit of the table you take them from.

⚠️ **What is missing does not stop the calculation, but makes unknown whatever
depends on it.** An ingredient without a composition or a weight, a missing
duration, a transform that cannot yet handle a nutrient: the product's value
comes out `null`, and `missing` says why. **Never a zero, never a partial
sum.**

> **Not weighed?** Leave out `harvested_g` and give the substrate a
> `yield: 1.75`: the tempeh weight will be **predicted**. That is what lets a
> recipe be costed before it has been made. ⚠️ The result is then marked
> `complete: false` — a product is not labelled with a denominator that is
> itself an estimate.

### What comes out

```yaml
recipe: Plain soy tempeh
harvested_g: 1750
complete: true             # every value is known (see the current state below)

per_100g:                  # the computed values; null = unknown
  fat: 9.99
  saturates: 2.24
  carbs: 5.19
  sugars: 1.4
  fibre: 4.36
  protein: 20.28
  salt: 0.01
  energy_kj: 837.6
  energy_kcal: 200.5

label:                     # the same, as they are written
  energy: 838 kJ / 201 kcal
  energy_kj: 838 kJ        # apart too, for a caller holding two fields
  energy_kcal: 201 kcal
  fat: 10,0 g
  saturates: 2,2 g
  carbs: 5,2 g
  sugars: 1,4 g
  fibre: 4,4 g
  protein: 20 g
  salt: < 0,01 g

steps:                     # the calculation sheet, in French, to show when challenged
  - "Apport de chaque intrant : masse pesée × composition pour 100 g (3 intrants)"
  - "Soybeans : Dépelliculage → Trempage (une nuit) → Cuisson 30 min → Fermentation 36 h"
  - "Kinako : Torréfaction → Fermentation 36 h"
  - "Cider vinegar : tel quel"
  - "Ramené à 100 g de produit fini : ÷ 1750 g récoltés. C'est cette division qui porte l'eau reprise"
  - "Énergie calculée depuis les macros (annexe XIV), jamais recopiée"

missing: []                # what stands in the way of a label, in plain words — here, nothing
warnings: []               # what does not stand in the way, but deserves a look
coefficients: {...}        # every coefficient of the transforms; null = gap
```

## What the engine does

It applies to each ingredient the transforms it actually goes through, staying
expressed per **100 g of raw ingredient**, then divides **once** by the weight
of tempeh.

> ⚠️ That final division, and it alone, carries the water taken up while
> soaking. A batch that doubles in weight by taking up water sees all its values
> halved, without any coefficient having to say so. Adding a "hydration factor"
> on top would count water twice.

| `role` | Transforms |
|---|---|
| `substrate` | dehulling *(if `dehulled`)* → soaking *(always one night, 10 to 15 h)* → cooking → fermentation |
| `support` | roasting *(if `roasted`)* → fermentation |
| `acid` | none — added after cooking, counted pro rata of its mass |
| `soaking_acid` | **left out** — it leaves with the soaking water, which is thrown away |
| `starter` | **left out** — a few grams for several kilos |

Both exclusions slightly **under-declare** the product: the safe direction, the
one that does not expose you.

⚠️ **`roasted: true` means you roast it.** Give the sheet and weight of the
**raw** product: roasting takes 8 % of the sugars and 16 % of the fibre
(`refs/methode.md`, T3). **Bought** kinako is already roasted, and its sheet
says so: enter it with `roasted: false`, or roasting counts twice. The water
it loses changes nothing in the calculation: the final weighing carries it.

Coefficients are no longer passed in the document: each one lives in
`zyfenutri/transforms.py`, with its source or the mention of a gap. What is
known about each transform, and what is missing, is in
**[`refs/transformations.md`](refs/transformations.md)**. The method and the law
are in **[`refs/methode.md`](refs/methode.md)**, the document shown at an
inspection. Both are in French.

> ⚠️ **Current state.** A soy tempeh described in full (durations, weights,
> sheets) comes out complete, as in the example above. Several coefficients
> are still hypotheses, and none has yet been validated by a laboratory analysis
> (`refs/transformations.md`, § 0). What needs refining, what is missing, and
> the three publications to obtain first: `refs/transformations.md`, § 0 bis.

## For those who write code

The calculation rests on three building blocks — the **sheet**
(`NutritionFacts`), the **transform** (`Transform`) and the **mix** (`mix`).
Their types, their signatures and what justifies them are in
**[`ARCHITECTURE.md`](ARCHITECTURE.md)** (in French).

## Reference data

`refs/official/` holds compositions **published by national food composition
tables**, copied as they are: three seed → tempeh pairs (USDA, New Zealand,
Norway) used to calibrate the coefficients.

> ⚠️ Each sheet states its **carbohydrate convention** and carries its flaws in
> its `notes`. Reference data whose weaknesses are kept quiet is not reference
> data.

`refs/analyses/` is for laboratory analyses, should any arrive.

```bash
python check.py      # holds the analyses up against the calculation — changes nothing
```

## What this repository does not do

It **does not decide**: it applies rules to data it is given.

It **knows no product**: no recipe, no supplier, no batch. It is given masses
and compositions, and returns values per 100 g.

It **never raises an exception on missing data**: it says so in `missing`, and
`complete` answers the only question that matters — can this go on a package?

## Installation and tests

```bash
pip install -e ".[dev]" && pytest
```

Single dependency: **PyYAML**, and only to read and write YAML on the command
line. `compute()` imports nothing but the standard library.

## Licence

MIT.
