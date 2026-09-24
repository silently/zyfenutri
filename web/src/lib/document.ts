/**
 * Le document : le construire depuis les champs, l'écrire en YAML, le relire.
 *
 * ⚠️ **Un champ vide est une valeur ABSENTE, jamais un zéro.** C'est la règle
 * la plus facile à trahir depuis un formulaire : un `<input type="number">`
 * vide rend `''`, et `Number('') === 0`. Envoyer ce zéro à CORE lui ferait
 * affirmer « il n'y en a pas » là où on voulait dire « on ne sait pas ».
 */
import { parse, stringify } from 'yaml';
import { NUTRIMENTS, porteUneFiche, type Composition, type Document, type Intrant } from './types';

/** `null` si le champ est vide ou illisible — jamais `0`. */
export function nombre(v: unknown): number | null {
  if (v === null || v === undefined || v === '') return null;
  const n = typeof v === 'number' ? v : Number(String(v).replace(',', '.'));
  return Number.isFinite(n) ? n : null;
}

export function intrantVide(): Intrant {
  return {
    name: '',
    role: 'substrate',
    weight_g: null,
    cooking_minutes: null,
    dehulled: false,
    roasted: false,
    yield: null,
    per_100g: Object.fromEntries(NUTRIMENTS.map((n) => [n, null])) as Composition,
  };
}

export function documentVide(): Document {
  return {
    recipe: '',
    fermentation_hours: null,
    ingredients: [intrantVide()],
  };
}

/**
 * Le document tel que CORE le reçoit : on retire ce qui est vide plutôt que de
 * l'envoyer à zéro ou à chaîne vide. Ce qui manque, `missing` le dira.
 */
export function pourLeMoteur(doc: Document): Document {
  // ⚠️ L'ordre des clés est celui de la LECTURE, pas celui du code : un
  // document s'ouvre sur son identifiant, puis son procédé, puis ses
  // ingrédients. En JavaScript, l'ordre d'insertion est l'ordre de sortie.
  const entete: Document = { ingredients: [] };
  if (doc.recipe?.trim()) entete.recipe = doc.recipe.trim();
  for (const cle of ['fermentation_hours'] as const) {
    const v = nombre(doc[cle]);
    if (v !== null) entete[cle] = v;
  }

  const ingredients = doc.ingredients.map((i) => {
    const sortie: Intrant = {};
    if (i.name?.trim()) sortie.name = i.name.trim();
    if (i.role) sortie.role = i.role;
    const poids = nombre(i.weight_g);
    if (poids !== null) sortie.weight_g = poids;
    const rendement = nombre(i.yield);
    if (rendement !== null) sortie.yield = rendement;
    const cuisson = nombre(i.cooking_minutes);
    if (cuisson !== null) sortie.cooking_minutes = cuisson;
    // Des booléens : `false` veut bien dire « non », pas « on ne sait pas ».
    if (i.dehulled) sortie.dehulled = true;
    if (i.roasted) sortie.roasted = true;

    // ⚠️ Un rôle exclu du calcul n'a pas de fiche : le starter compte par son
    // poids et sa proportion, rien d'autre. Lui en envoyer une serait envoyer
    // une donnée que CORE ignore, et laisser croire qu'elle sert.
    if (porteUneFiche(i.role)) {
      const compo: Composition = {};
      for (const n of NUTRIMENTS) {
        const v = nombre(i.per_100g?.[n]);
        if (v !== null) compo[n] = v;
      }
      if (Object.keys(compo).length > 0) sortie.per_100g = compo;
    }
    return sortie;
  });

  // `ingredients` est posé en DERNIER, pour qu'il se lise en dernier.
  const { ingredients: _vide, ...tete } = entete;
  return { ...tete, ingredients };
}

export function versYaml(doc: Document): string {
  return stringify(pourLeMoteur(doc), { lineWidth: 0 });
}

export function versJson(doc: Document): string {
  return JSON.stringify(pourLeMoteur(doc), null, 2) + '\n';
}

/** Le résultat du moteur, tel quel — la fiche de calcul à archiver. */
export function calculVersYaml(resultat: unknown): string {
  return stringify(resultat, { lineWidth: 0 });
}

/**
 * Un nom de fichier tiré de l'identifiant de recette.
 *
 * ⚠️ L'identifiant est saisi librement : il peut porter des espaces, des
 * accents, une barre oblique. Un nom de fichier, non — et une barre oblique
 * ferait silencieusement échouer le téléchargement sur certains navigateurs.
 */
export function nomFichier(identifiant: string | null | undefined, suffixe: string): string {
  const base = (identifiant ?? '')
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-zA-Z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .toLowerCase()
    .slice(0, 60);
  return `${base || 'lot'}${suffixe}`;
}

export type Relecture = { document: Document; ignores: string[] };

/**
 * Relit un document YAML dans les champs. Tolérant sur ce qui manque : un
 * document partiel se saisit aussi bien qu'un complet.
 *
 * ⚠️ Rend aussi ce qu'il a **laissé de côté**. Un document écrit pour une
 * version antérieure du moteur peut porter un `harvested_g` (retiré en 2.0) ou
 * un acidifiant de trempage : les perdre en silence ferait un résultat
 * différent sans que rien ne l'explique.
 */
export function depuisYaml(texte: string): Relecture {
  const lu = parse(texte) as (Partial<Document> & { harvested_g?: unknown }) | null;
  if (!lu || typeof lu !== 'object') throw new Error('Document vide ou illisible');

  const cuissonDuLot = nombre((lu as { cooking_minutes?: unknown }).cooking_minutes);
  const ignores: string[] = [];
  if (lu.harvested_g != null) {
    ignores.push(
      `poids récolté (${lu.harvested_g} g) — le moteur ne l'accepte plus : ` +
        'le poids de tempeh vient des facteurs de rendement',
    );
  }
  const trempage = (Array.isArray(lu.ingredients) ? lu.ingredients : []).filter(
    (i) => (i as { role?: string })?.role === 'soaking_acid',
  );
  for (const i of trempage) {
    ignores.push(
      `${(i as { name?: string }).name ?? 'acidifiant de trempage'} — part avec l'eau de ` +
        'trempage, qui est jetée : il ne change rien au résultat',
    );
  }

  const intrants = (Array.isArray(lu.ingredients) ? lu.ingredients : []).filter(
    (i) => (i as { role?: string })?.role !== 'soaking_acid',
  );
  const document: Document = {
    recipe: lu.recipe ?? '',
    fermentation_hours: nombre(lu.fermentation_hours),
    ingredients: (intrants.length ? intrants : [intrantVide()]).map((i) => {
      const base = intrantVide();
      const compo = { ...base.per_100g } as Composition;
      // ⚠️ CORE accepte les noms longs en entrée (`fat_g` → `fat`) : on en fait
      // autant, sinon un document qui passe en ligne de commande serait refusé ici.
      for (const [cle, valeur] of Object.entries(i?.per_100g ?? {})) {
        const court = ALIAS[cle] ?? cle;
        if ((NUTRIMENTS as readonly string[]).includes(court)) {
          compo[court as (typeof NUTRIMENTS)[number]] = nombre(valeur);
        }
      }
      return {
        ...base,
        name: i?.name ?? '',
        role: i?.role ?? 'substrate',
        weight_g: nombre(i?.weight_g),
        yield: nombre(i?.yield),
        // ⚠️ Un document venu de la ligne de commande peut porter la cuisson au
        // niveau du lot. On la REDESCEND sur les substrats qui n'en ont pas :
        // le calcul est identique, et la valeur devient visible et modifiable
        // au lieu de rester un réglage caché.
        cooking_minutes: nombre(i?.cooking_minutes) ?? cuissonDuLot,
        dehulled: Boolean(i?.dehulled),
        roasted: Boolean(i?.roasted),
        per_100g: compo,
      };
    }),
  };
  return { document, ignores };
}

/** Les mêmes alias que `nutrients.ALIASES` dans CORE, pour l'entrée. */
const ALIAS: Record<string, string> = {
  fat_g: 'fat',
  lipides: 'fat',
  matieres_grasses: 'fat',
  saturates_g: 'saturates',
  saturated: 'saturates',
  ags: 'saturates',
  carbohydrates: 'carbs',
  carbohydrates_g: 'carbs',
  carbs_g: 'carbs',
  glucides: 'carbs',
  sugars_g: 'sugars',
  sucres: 'sugars',
  fibre_g: 'fibre',
  fiber: 'fibre',
  fibres: 'fibre',
  protein_g: 'protein',
  proteins: 'protein',
  proteines: 'protein',
  salt_g: 'salt',
  sel: 'salt',
};


/**
 * Un modèle à télécharger, pour ne pas partir d'une page blanche.
 *
 * ⚠️ Les compositions sont des EXEMPLES d'ordre de grandeur, pas des données
 * de référence : elles se remplacent par la fiche du fournisseur ou une table
 * publiée (Ciqual, USDA). Un chiffre qu'on n'a pas se laisse VIDE — CORE dira
 * que la valeur est inconnue, ce qui est vrai, au lieu d'un zéro qui ment.
 */
export const MODELE = `# Modèle de lot pour zyfenutri — remplacez les valeurs par les vôtres.
#
# ⚠️ Les compositions ci-dessous sont des EXEMPLES, pas des données de
# référence. Prenez celles de la fiche de votre fournisseur, ou d'une table
# publiée (Ciqual, USDA). Une valeur qu'on n'a pas se laisse VIDE, jamais à 0 :
# « on ne sait pas » et « il n'y en a pas » sont deux affirmations différentes.

recipe: tempeh-soja-nature   # identifiant : c'est lui qui nomme les fichiers
fermentation_hours: 36       # collective : tout le bloc incube ensemble

ingredients:
  # Le substrat : le seul à tremper, cuire et gonfler. Son facteur de rendement
  # est ce qui prédit le poids de tempeh, et donc la division finale.
  - name: Soja
    role: substrate
    weight_g: 1000        # poids BRUT, pellicule comprise
    dehulled: true
    yield: 1.75
    cooking_minutes: 30   # LA SIENNE : chaque substrat cuit son propre temps
    per_100g: {fat: 20, saturates: 2.9, carbs: 15, sugars: 5.7, fibre: 15, protein: 40, salt: 0.01}

  # L'acidifiant pré-inoculation : mélangé au substrat, il compte entièrement.
  - name: Vinaigre de cidre
    role: acid
    weight_g: 50
    per_100g: {fat: 0, saturates: 0, carbs: 0.93, sugars: 0.4, fibre: 0, protein: 0, salt: 0.013}

  # Le starter : poids et proportion seulement. Quelques grammes pour des
  # kilos de produit — il est exclu du calcul, et n'a donc pas de fiche.
  - name: Starter
    role: starter
    weight_g: 4
`;
