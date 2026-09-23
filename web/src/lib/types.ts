/**
 * Les formes du contrat public de CORE — document d'entrée, document de sortie.
 *
 * ⚠️ Recopiées d'après `ARCHITECTURE.md` et les README. Elles DÉCRIVENT CORE,
 * elles ne le décident pas : si l'une diverge, c'est ici qu'on corrige.
 */

/** Les sept valeurs déclarées, dans l'ordre de l'étiquette. */
export const NUTRIMENTS = [
  'fat',
  'saturates',
  'carbs',
  'sugars',
  'fibre',
  'protein',
  'salt',
] as const;
export type Nutriment = (typeof NUTRIMENTS)[number];

/** Les libellés français, tels qu'ils s'écrivent sur une étiquette. */
export const LIBELLES: Record<Nutriment, string> = {
  fat: 'Matières grasses',
  saturates: 'dont acides gras saturés',
  carbs: 'Glucides',
  sugars: 'dont sucres',
  fibre: 'Fibres alimentaires',
  protein: 'Protéines',
  salt: 'Sel',
};

/**
 * Les rôles proposés à la saisie.
 *
 * ⚠️ CORE en connaît un de plus, `soaking_acid` : il part avec l'eau de
 * trempage, qui est jetée, donc il ne change jamais rien au résultat. On ne le
 * propose pas — un champ dont la valeur n'a aucun effet ne fait qu'encombrer.
 * CORE continue de l'accepter : un document qui en porte un reste valide.
 *
 * `compose: false` veut dire : **pas de fiche nutritionnelle**. Le starter ne
 * compte que par son poids et sa proportion dans la recette ; CORE l'exclut du
 * calcul (quelques grammes pour des kilos), donc lui demander une composition
 * serait demander une donnée qui ne sert à rien.
 */
export const ROLES = [
  { valeur: 'substrate', libelle: 'Substrat', aide: 'trempe, cuit, fermente — le seul à gonfler', compose: true },
  { valeur: 'support', libelle: "Support d'inoculation", aide: 'entre après égouttage, fermente', compose: true },
  { valeur: 'acid', libelle: 'Acidifiant pré-inoculation', aide: 'mélangé au substrat, compté', compose: true },
  { valeur: 'starter', libelle: 'Starter', aide: 'poids et proportion seulement — exclu du calcul', compose: false },
] as const;
export type Role = (typeof ROLES)[number]['valeur'];

export function porteUneFiche(role: Role | null | undefined): boolean {
  return ROLES.find((r) => r.valeur === role)?.compose ?? true;
}

/** Une composition pour 100 g. `null` = inconnu, jamais zéro. */
export type Composition = Partial<Record<Nutriment, number | null>>;

export type Intrant = {
  name?: string | null;
  role?: Role | null;
  weight_g?: number | null;
  /**
   * ⚠️ La cuisson appartient au SUBSTRAT : un soja et une lentille ne cuisent
   * ni le même temps ni dans la même casserole. La fermentation, elle, reste
   * un fait du lot — tout le bloc incube ensemble.
   */
  cooking_minutes?: number | null;
  dehulled?: boolean;
  roasted?: boolean;
  yield?: number | null;
  per_100g?: Composition | null;
};

/**
 * ⚠️ **Pas de `harvested_g`.** Le poids de tempeh est PRÉDIT par le facteur de
 * rendement du substrat. Peser une fournée ne dit rien de ce qu'on imprime :
 * ce poids porte sa propre incertitude, et une étiquette ne change pas d'une
 * fournée à l'autre. CORE accepte toujours la clé ; cette page ne l'envoie pas.
 */
export type Document = {
  recipe?: string | null;
  /** ⚠️ Collective : tout le bloc incube ensemble. La CUISSON, elle, est sur
   *  l'intrant — cf. `Intrant.cooking_minutes`. */
  fermentation_hours?: number | null;
  ingredients: Intrant[];
};

export type LigneIntrant = {
  name: string | null;
  role: string | null;
  counted: boolean;
  excluded_because?: string | null;
  transforms?: string[];
  contributes_g?: Record<string, number | null>;
};

export type Resultat = {
  recipe: string | null;
  harvested_g: number | null;
  harvest_estimated: boolean;
  complete: boolean;
  per_100g: Record<string, number | null>;
  /** Les mentions, telles qu'elles s'écrivent. ⚠️ Déjà arrondies par CORE : on
   *  les affiche, on ne les reformate JAMAIS — un second arrondi déplacerait
   *  le chiffre d'une unité. */
  label: Record<string, string | null>;
  dry_matter_g: number | null;
  ingredients: LigneIntrant[];
  missing: string[];
  warnings: string[];
  steps: string[];
  coefficients: Record<string, unknown>;
};
