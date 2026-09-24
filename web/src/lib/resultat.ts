/**
 * Lire le résultat de CORE pour cette page.
 *
 * ⚠️ **Les manques se disent en français.** CORE les écrit en anglais — c'est
 * sa règle, son `missing` s'adresse à un appelant, pas à un lecteur. Ici c'est
 * une personne qui lit. Ce qu'on ne sait pas traduire est rendu tel quel :
 * mieux vaut de l'anglais qu'un silence.
 *
 * ⚠️ On ne juge RIEN ici. `complete` vient du moteur tel quel. Cette couche a
 * porté, jusqu'à zyfenutri 1.13, la levée d'une réserve sur le poids de
 * récolte ; le moteur ne l'émet plus depuis qu'il n'accepte plus de poids pesé.
 */
import type { Resultat } from './types';

const LIBELLES: [RegExp, (m: RegExpMatchArray) => string][] = [
  [/^no cooking time for (.+) \(/, (m) => `${m[1]} — durée de cuisson non renseignée`],
  [/^no cooking time/, () => 'Durée de cuisson non renseignée'],
  [/^no fermentation time/, () => 'Durée de fermentation non renseignée'],
  [/^invalid cooking time for (.+) \(cooking_minutes\): (.+)$/,
    (m) => `${m[1]} — durée de cuisson illisible : ${m[2]}`],
  [/^invalid fermentation time: (.+)$/, (m) => `Durée de fermentation illisible : ${m[1]}`],
  [
    /^no yield factor on a substrate/,
    () => 'Aucun facteur de rendement sur un substrat : le poids de tempeh ne peut pas être établi',
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
  complete: boolean;
  manques: string[];
  /** Le poids de tempeh, donné par les facteurs de rendement, en grammes. */
  poidsTempeh: number | null;
};

export function lire(resultat: Resultat): Lecture {
  return {
    complete: resultat.complete,
    manques: resultat.missing.map(enFrancais),
    poidsTempeh: resultat.tempeh_g,
  };
}
