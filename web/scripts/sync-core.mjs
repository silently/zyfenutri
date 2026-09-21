/**
 * Recopie les modules de CORE dans `static/`, pour que le navigateur les
 * charge tels quels.
 *
 * ⚠️ Ce script LIT `../zyfenutri/` et n'y écrit JAMAIS. C'est le seul point de
 * contact entre WEB et CORE, et il va dans un seul sens (CLAUDE.md § CORE et
 * WEB). Le calcul de la page est donc le MÊME code Python que la ligne de
 * commande — pas une réécriture, donc aucune divergence possible.
 *
 * Relancé avant chaque `dev` et chaque `build` : une copie périmée donnerait
 * une page qui calcule autrement que le dépôt, sans que rien ne le signale.
 */
import { copyFileSync, mkdirSync, readFileSync, readdirSync, rmSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const ICI = dirname(fileURLToPath(import.meta.url));
const CORE = join(ICI, '..', '..', 'zyfenutri');
const CIBLE = join(ICI, '..', 'static', 'core', 'zyfenutri');

const modules = readdirSync(CORE).filter((f) => f.endsWith('.py')).sort();
if (!modules.includes('__init__.py')) {
  throw new Error(`CORE introuvable ou incomplet dans ${CORE}`);
}

rmSync(CIBLE, { recursive: true, force: true });
mkdirSync(CIBLE, { recursive: true });
for (const f of modules) copyFileSync(join(CORE, f), join(CIBLE, f));

// La version, lue à la source : elle s'affiche sur la page, parce qu'un
// résultat qu'on ne peut pas rattacher à une version du moteur ne se discute pas.
const init = readFileSync(join(CORE, '__init__.py'), 'utf8');
const version = init.match(/^__version__ = "([^"]+)"/m)?.[1];
if (!version) throw new Error('version introuvable dans zyfenutri/__init__.py');

writeFileSync(
  join(CIBLE, 'manifest.json'),
  JSON.stringify({ version, modules }, null, 2) + '\n',
);
console.log(`core → static : zyfenutri ${version}, ${modules.length} modules`);
