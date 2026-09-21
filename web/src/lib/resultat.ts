/**
 * Lire le résultat de CORE pour cette page.
 *
 * Deux choses s'y jouent, toutes deux **côté WEB** — aucune ne touche CORE.
 *
 * 1. **La réserve sur le poids de récolte se lève ici.** Sans `harvested_g`,
 *    CORE prédit le poids par le facteur de rendement et dit, à raison, que
 *    ça vaut pour concevoir une recette et non pour étiqueter un produit.
 *    Cette page CONÇOIT des recettes : le facteur de rendement est une
 *    consigne d'atelier qu'on règle soi-même, et les tolérances d'étiquetage
 *    (règlement INCO, tableau 1) absorbent l'écart d'une fournée à l'autre.
 *    ⚠️ On ne lève QUE cette réserve : une composition manquante ou une durée
 *    absente rendent toujours la fiche incomplète.
 *
 * 2. **Les manques se disent en français.** CORE les écrit en anglais — c'est
 *    sa règle, son `missing` s'adresse à un appelant, pas à un lecteur. Ici
 *    c'est une personne qui lit. Ce qu'on ne sait pas traduire est rendu tel
 *    quel : mieux vaut de l'anglais qu'un silence.
 */
import type { Resultat } from './types';

/** La seule réserve qu'on lève. ⚠️ Le texte vient de `engine.py` — s'il change
 *  là-bas, la réserve réapparaît ici au lieu de disparaître en silence. */
const RESERVE_RECOLTE = 'harvest weight predicted, not weighed';

const LIBELLES: [RegExp, (m: RegExpMatchArray) => string][] = [
  [/^no cooking time/, () => 'Durée de cuisson non renseignée'],
  [/^no fermentation time/, () => 'Durée de fermentation non renseignée'],
  [/^invalid cooking time: (.+)$/, (m) => `Durée de cuisson illisible : ${m[1]}`],
  [/^invalid fermentation time: (.+)$/, (m) => `Durée de fermentation illisible : ${m[1]}`],
  [
    /^no harvest weight, and no yield factor/,
    () => 'Aucun facteur de rendement sur le substrat : le poids de tempeh ne peut pas être prédit',
  ],
  [/^(.+) — no composition given$/, (m) => `${m[1]} — pas de composition saisie`],
  [/^(.+) — no weight given$/, (m) => `${m[1]} — pas de poids saisi`],
  [/^(.+) — sheet has no (.+)$/, (m) => `${m[1]} — sa fiche ne donne pas : ${NUTRIMENT[m[2]] ?? m[2]}`],
  [
    /^(.+) unknown in the product: an ingredient or a transform/,
    (m) => `${NUTRIMENT[m[1]] ?? m[1]} — inconnu dans le produit : un intrant ou une transformation ne sait pas encore le calculer`,
  ],
];

const NUTRIMENT: Record<string, string> = {
  fat: 'matières grasses',
  saturates: 'acides gras saturés',
  carbs: 'glucides',
  sugars: 'sucres',
  fibre: 'fibres alimentaires',
  protein: 'protéines',
  salt: 'sel',
};

function enFrancais(message: string): string {
  for (const [motif, rendre] of LIBELLES) {
    const m = message.match(motif);
    if (m) return rendre(m);
  }
  return message;
}

export type Lecture = {
  /** ⚠️ Recalculé : CORE compte la réserve sur la récolte, pas nous. */
  complete: boolean;
  manques: string[];
  /** Le poids de tempeh prédit par les facteurs de rendement, en grammes. */
  poidsPredit: number | null;
};

export function lire(resultat: Resultat): Lecture {
  const manques = resultat.missing.filter((m) => !m.startsWith(RESERVE_RECOLTE));
  return {
    complete: manques.length === 0 && resultat.per_100g.energy_kj != null,
    manques: manques.map(enFrancais),
    poidsPredit: resultat.harvested_g,
  };
}
