/**
 * Extrait la bibliographie de `refs/references.md` vers `static/`.
 *
 * ⚠️ `refs/references.md` EST la bibliographie — l'index numéroté, avec le
 * statut de chaque source et ce qu'on en tire. On ne la recopie pas à la main :
 * une seconde liste divergerait, et c'est exactement ce que la frontière
 * CORE / WEB interdit (CLAUDE.md § CORE et WEB). Ce script LIT, il n'écrit
 * jamais dans CORE.
 *
 * ⚠️ Il **échoue bruyamment** si le format change. Une bibliographie
 * silencieusement tronquée serait pire que pas de bibliographie du tout.
 */
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const ICI = dirname(fileURLToPath(import.meta.url));
const SOURCE = join(ICI, '..', '..', 'refs', 'references.md');
const CIBLE = join(ICI, '..', 'static', 'core');

const texte = readFileSync(SOURCE, 'utf8');

// `### [n] Auteurs, année — *Titre*`, puis le paragraphe de citation complète.
// ⚠️ Le titre n'est pas toujours SEUL après le tiret : [12] porte
// « *The Book of Tempeh*, Appendix E ». On prend donc tout ce qui suit, et on
// enlève les italiques — sinon la source disparaît de la biblio en silence.
const entetes = [...texte.matchAll(/^### \[(\d+)\] (.+?) — (.+?)\s*$/gm)];
if (entetes.length === 0) throw new Error(`aucune référence trouvée dans ${SOURCE}`);

const references = entetes.map((m, i) => {
  const numero = Number(m[1]);
  const suite = texte.slice(
    m.index + m[0].length,
    i + 1 < entetes.length ? entetes[i + 1].index : texte.length,
  );

  // La citation : le premier paragraphe non vide, avant la liste à puces.
  const citation = suite
    .split(/\n\s*\n/)
    .map((p) => p.trim())
    .find((p) => p && !p.startsWith('-'));
  if (!citation) throw new Error(`référence [${numero}] : citation introuvable`);

  const lien = citation.match(/<(https?:\/\/[^>]+)>/)?.[1] ?? null;
  // ⚠️ Le statut porte souvent un détail entre parenthèses (« lu, par passages
  // (voir ci-dessous) »). Ce qui compte pour une biblio, c'est la CATÉGORIE :
  // un chiffre ne se cite que d'une source LUE.
  const brut = suite.match(/^- \*\*Statut :\*\* *(.+)$/m)?.[1];
  if (!brut) throw new Error(`référence [${numero}] : statut introuvable`);
  const statut = ['non lu', 'retirée', 'résumé', 'lu'].find((c) => brut.startsWith(c));
  if (!statut) throw new Error(`référence [${numero}] : statut illisible — ${brut}`);

  return {
    numero,
    court: m[2].trim(),
    titre: m[3].replace(/\*/g, '').trim(),
    // Sans les liens ni les italiques : la citation telle qu'on la lit.
    // ⚠️ TOUTES les URL, pas seulement celle de fin : [11] porte le DOI de sa
    // réédition au milieu de la phrase, et il ressortait entre chevrons.
    citation: citation
      .replace(/\s*<https?:\/\/[^>]+>/g, '')
      // Retirer une URL au milieu d'une phrase laisse sa ponctuation orpheline
      // (« Réédition Springer : . Chapitre »). On recolle.
      .replace(/\s*:\s*\./g, '.')
      .replace(/\*/g, '')
      .replace(/\s+/g, ' ')
      .replace(/\s+([.,;])/g, '$1')
      .trim(),
    lien,
    statut,
  };
});

const attendus = references.map((r) => r.numero);
const manquants = Array.from({ length: Math.max(...attendus) }, (_, i) => i + 1)
  .filter((n) => !attendus.includes(n));
if (manquants.length) {
  // ⚠️ Un numéro ne se réattribue jamais : un trou est une source retirée, pas
  // une erreur de lecture. Mais il doit se voir.
  console.warn(`  ⚠️ numéros absents de l'index : ${manquants.join(', ')}`);
}

mkdirSync(CIBLE, { recursive: true });
writeFileSync(join(CIBLE, 'references.json'), JSON.stringify(references, null, 2) + '\n');
console.log(`refs → static : ${references.length} références`);
