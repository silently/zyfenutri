# Données attestées de composition

Des compositions **publiées par des tables nationales**, recopiées telles
quelles. Rien n'est calculé ici, rien n'est converti : c'est le matériau brut
auquel on se réfère quand une question se pose sur la « tempehisation ».

## Les couples soja → tempeh

C'est ce qui donne leur valeur à ces fiches : une composition de tempeh seule ne
dit rien, faute de savoir de quoi elle vient. Un **couple issu de la même
table** partage ses conventions d'analyse — sans quoi on compare deux méthodes
plutôt que deux produits.

| Source | Graine | Tempeh | Couple |
|---|---|---|---|
| **USDA** (États-Unis) | `usda-soja-174270` | `usda-tempeh-174272` | ✅ |
| **Nouvelle-Zélande** | `nz-soja-X230` | `nz-tempeh-X10030` | ✅ |
| **Norvège** | `norvege-soja` | `norvege-tempeh` | ✅ |
| **Suède** | — | `suede-tempeh-7027` | ❌ tempeh seul |

> ⚠️ **Finlande (Fineli) manquant.** `fineli.fi/fineli/en/elintarvikkeet/31249`
> est protégé par Cloudflare : 403 sur la page comme sur son API, depuis le
> navigateur serveur comme en ligne de commande. À récupérer à la main depuis un
> navigateur, ou à laisser de côté.

## Les couples soja → kinako

La même logique pour la **torréfaction** : une graine et sa farine torréfiée,
dans la même table.

| Source | Graine | Kinako | Couple |
|---|---|---|---|
| **Japon** (MEXT 2020), soja jaune | `mext-soja-04023` | `mext-kinako-04029` | ✅ sucres ; fibres par Prosky seulement |
| **Japon** (MEXT 2020), soja vert | `mext-soja-vert-04104` | `mext-kinako-vert-04082` | ✅ sucres ; ❌ fibres (deux méthodes) |

⚠️ La torréfaction chasse de l'eau : ces couples se lisent **en matière
sèche**, sans quoi tout semble augmenter. Et ce sont deux lots, pas un lot
torréfié : les lipides y montent de 10 à 19 %, ce qu'une torréfaction ne peut
pas faire. Seul ce qui bouge nettement et dans le même sens sur les deux
couples sert de calage (`refs/methode.md`, T3).

## Ce qu'il faut lire avant de comparer deux fiches

⚠️ **« Glucides » ne veut pas dire la même chose partout.**

| Convention | Ce que le nombre contient | Qui l'emploie |
|---|---|---|
| `by_difference` | 100 − eau − protéines − lipides − cendres − fibres : **les fibres en sont déduites, mais tout le reste y est** | USDA |
| `assimilables` | amidon + sucres **pesés** ; conforme au règlement INCO | Norvège, Suède |
| `les_deux` | les deux nombres sont publiés | Nouvelle-Zélande, Japon |

Chaque fiche porte sa convention en tête, sous `convention_glucides`.

**La Nouvelle-Zélande est la source la plus instructive** parce qu'elle publie
les deux : sur sa graine, 22,0 g par différence contre 9,59 g pesés. Les
**12,4 g d'écart** ne sont ni amidon, ni sucre, ni fibre — ce sont les
oligosaccharides du soja (raffinose, stachyose). Dans son tempeh, ce même écart
tombe à 3,15 g : ils ont presque tous disparu au trempage et à la fermentation.

⚠️ La frontière **fibres / glucides** bouge d'une table à l'autre sans que le
produit change. Sur le tempeh : 1,3 g de fibres en Suède, 4,0 en Norvège, 7,7 en
Nouvelle-Zélande — mais `glucides + fibres` vaut 9,5 g des deux côtés pour la
Suède et la Norvège. Comparer les fibres de deux tables différentes n'a
pratiquement aucun sens ; comparer leur somme en a un.

## Format

Une fiche = un aliment, une table. Les valeurs sont **pour 100 g, telles que
publiées** — aucun arrondi, aucune conversion. Une valeur que la table ne publie
pas reste **vide** : ce n'est pas un zéro.

Le bloc `notes` de chaque fichier porte ce qu'on a remarqué en la lisant, y
compris quand c'est gênant — l'anomalie des AGS du tempeh USDA, l'eau à 20 g de
la graine norvégienne, les fibres à 1,3 g du tempeh suédois. Une donnée de
référence dont on tait les défauts n'est pas une référence.
