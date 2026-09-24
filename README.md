# zyfenutri

*Version française : [README.fr.md](README.fr.md)*

Zyfe nutri is a tool that estimates the nutrition declaration of tempeh from
those of its ingredients and from variables of the making (cooking time of the
substrates, fermentation time).

A Python library, a script, and a **web page** that runs the same calculation
in the browser: <https://silently.github.io/zyfenutri/>. No server, no
database, no port to open.

## At your own risk

This tool is provided **for guidance only**. It can be improved (any comment or
scientific reference that would help is welcome — please
[open an issue](https://github.com/silently/zyfenutri/issues)) and it comes with
no warranty. It may be worth checking it against laboratory results.

If the tool can mislead, do not forget that the nutrition declarations of the
ingredients can be wrong too.

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
result = compute({"fermentation_hours": 36, "ingredients": [...]})
```

### What goes in

```yaml
recipe: Plain soy tempeh
cooking_minutes: 30        # default cooking time; an ingredient may carry its own
fermentation_hours: 36     # incubation time

ingredients:
  - name: Soybeans
    role: substrate        # substrate · support · acid · soaking_acid · starter
    weight_g: 1000         # weight BEFORE any transform, hulls included
    dehulled: true         # dehulled BY US, after delivery
    yield: 1.75            # yield factor — required, see below
    cooking_minutes: 30    # ITS OWN — a soybean and a lentil do not cook for the
                           #  same time, nor in the same pot. Falls back to the document's.
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

### `yield` — the yield factor

**One number per substrate, required**: kg of tempeh per 1 kg of raw grain.

⚠️ It carries **every gain and every loss of that substrate, from the raw grain
through to harvest** — a single number for the whole making. It alone gives the
weight of tempeh the final division uses.

It is **set**, not measured once: a workshop instruction, read back against
one's own batches and adjusted. Two different substrates have two different
factors, and a blend set on an average would skew each one's share.

⚠️ The engine then attaches a reservation to the sheet, in `missing`: it cannot
know whether its caller is designing a recipe or describing a batch. Lifting
that reservation is the caller's call, and the caller's to justify —
`refs/methode.md` § 3.3 says when *(in French)*.

### What comes out

```yaml
recipe: Plain soy tempeh

per_100g:                  # the computed values; null = unknown
  fat: 9.66
  saturates: 2.16
  carbs: 5.02
  sugars: 1.36
  fibre: 4.21
  protein: 19.61
  salt: 0.01
  energy_kj: 809.8
  energy_kcal: 193.9

label:                     # the same, as they are written
  energy: 810 kJ / 194 kcal
  energy_kj: 810 kJ        # apart too, for a caller holding two fields
  energy_kcal: 194 kcal
  fat: 9,7 g
  saturates: 2,2 g
  carbs: 5,0 g
  sugars: 1,4 g
  fibre: 4,2 g
  protein: 20 g
  salt: < 0,01 g

steps:                     # the calculation sheet, in French, to show when challenged
  - "Apport de chaque intrant : masse pesée × composition pour 100 g (3 intrants)"
  - "Soybeans : Dépelliculage → Trempage et rinçage (une nuit) → Cuisson 30 min (égouttage compris) → Fermentation 36 h"
  - "Kinako : Torréfaction → Fermentation 36 h"
  - "Cider vinegar : tel quel"
  - "Ramené à 100 g de produit fini : ÷ 1810 g de tempeh prédits par le facteur de rendement"
  - "Énergie calculée depuis les macros (annexe XIV), jamais recopiée"

missing:                   # what stands in the way of a label, in plain words
  - "harvest weight predicted, not weighed — fine to design a recipe, not to label a product"
warnings: []               # what does not stand in the way, but deserves a look
coefficients: {...}        # every coefficient of the transforms; null = gap
```

## What the engine does

It applies to each ingredient the transforms it actually goes through, staying
expressed per **100 g of raw ingredient**, then divides **once** by the weight
of tempeh.

> ⚠️ That final division is the **only** one. The yield factor already carries
> everything that changes a substrate's mass, from the raw grain through to
> harvest: adding a second factor on top would count the same change twice.

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

## An example: what ten hours of fermentation change

The same batch — 1 kg of dehulled soybeans, `yield: 1.75`, cooked 30 min —
fermented 30 h, then 40 h:

| per 100 g | 30 h | 40 h | gap | tolerance allowed |
|---|---|---|---|---|
| Fat | 9,9 g | 9,9 g | **none** | ± 1.5 g |
| of which saturates | 2,2 g | 2,2 g | **none** | ± 0.8 g |
| Carbohydrate | 5,4 g | 4,9 g | **− 0.49 g** | ± 2 g |
| of which sugars | 1,4 g | 1,3 g | − 0.06 g | ± 2 g |
| Fibre | 4,3 g | 4,3 g | **none** | ± 2 g |
| Protein | 20 g | 20 g | − 0.12 g | ± 4 g |
| Energy | 834 kJ | 824 kJ | − 10 kJ | — |

On the label, **only two lines move**: carbohydrate and sugars. The largest gap
is **a quarter of its tolerance** — ten hours of fermentation therefore do not
put a declaration at risk.

Fat does not move at all: the model holds it on a plateau between 26 and 60 h,
the loss being complete before 30 h.

⚠️ **The break is at 48 h, not between 30 and 40.** Past that, the loss of
sugars is no longer covered by the literature that has been read: the engine
returns `null` rather than extrapolate, and energy becomes unknown with them,
since it is computed from the macronutrients.

```
48 h : carbs 4.54   sugars 1.30   energy_kj 815.8
50 h : carbs null   sugars null   energy_kj null
```

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

## The web version

<https://silently.github.io/zyfenutri/> — a static page, no back end. The
document is typed into fields, the page renders the label, and both the
document and the calculation sheet download as `.yml` or `.json`.

⚠️ **It is the same Python code**, run by [Pyodide](https://pyodide.org) in the
browser — not a JavaScript rewrite. One implementation of the rules, so the
page cannot say anything the command line would not.

It answers a question the library leaves open: **the weight of tempeh**. The
page has no "harvested weight" field — it always **predicts** that weight from
the yield factor, which is therefore required there. A label carries an average
value, not one batch's. That choice, and what follows from it, is in
[`refs/methode.md`](refs/methode.md) § 3.3 *(in French)*.

Its in-page help is the **user documentation** for that page;
`refs/methode.md` remains the reference for the method and the law.

The code lives in [`web/`](web/) and never reaches into the engine's own.

## Installation and tests

```bash
pip install -e ".[dev]" && pytest
```

Single dependency: **PyYAML**, and only to read and write YAML on the command
line. `compute()` imports nothing but the standard library.

## Licence

MIT.
