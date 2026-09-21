/**
 * Le moteur, dans le navigateur.
 *
 * ⚠️ C'est **le code Python de CORE**, exécuté par Pyodide — pas une
 * réécriture. Une seule implémentation des règles, donc la page ne peut pas
 * dire autre chose que la ligne de commande (CLAUDE.md § CORE et WEB).
 *
 * Pyodide se charge depuis le CDN : environ 10 Mo la première fois, puis le
 * cache du navigateur. C'est le prix d'un calcul sans back end, et il se paie
 * une fois par visite, pas à chaque calcul.
 */
import { base } from '$app/paths';
import type { Document, Resultat } from './types';

/** ⚠️ Pyodide 314.x embarque CPython 3.14, que CORE exige (`requires-python`). */
const PYODIDE = '314.0.7';

export type Etat =
  | { phase: 'attente' }
  | { phase: 'chargement'; detail: string }
  | { phase: 'prêt'; version: string }
  | { phase: 'échec'; message: string };

type Pyodide = {
  FS: { mkdirTree(p: string): void; writeFile(p: string, c: string): void };
  runPython(code: string): unknown;
};

let pyodide: Pyodide | null = null;
let version = '';
let enCours: Promise<void> | null = null;

async function amorcer(dire: (detail: string) => void): Promise<void> {
  dire('Téléchargement de Python (~10 Mo, la première fois seulement)…');
  const url = `https://cdn.jsdelivr.net/pyodide/v${PYODIDE}/full/pyodide.mjs`;
  const { loadPyodide } = (await import(/* @vite-ignore */ url)) as {
    loadPyodide(o?: { indexURL?: string }): Promise<Pyodide>;
  };
  const py = await loadPyodide({ indexURL: `https://cdn.jsdelivr.net/pyodide/v${PYODIDE}/full/` });

  dire('Chargement du moteur zyfenutri…');
  const racine = `${base}/core/zyfenutri`;
  const manifest = (await (await fetch(`${racine}/manifest.json`)).json()) as {
    version: string;
    modules: string[];
  };
  py.FS.mkdirTree('/core/zyfenutri');
  await Promise.all(
    manifest.modules.map(async (nom) => {
      const source = await (await fetch(`${racine}/${nom}`)).text();
      py.FS.writeFile(`/core/zyfenutri/${nom}`, source);
    }),
  );

  py.runPython(`
import sys, json
sys.path.insert(0, "/core")
from zyfenutri import compute
`);
  pyodide = py;
  version = manifest.version;
}

/** Charge le moteur une seule fois, même si plusieurs appels se croisent. */
export function preparer(dire: (detail: string) => void): Promise<void> {
  enCours ??= amorcer(dire);
  return enCours;
}

export function versionMoteur(): string {
  return version;
}

/**
 * Le calcul : un document entre, un document sort — le même contrat que
 * `compute()` en Python et que la ligne de commande.
 *
 * ⚠️ Le passage se fait en JSON des deux côtés : les conversions automatiques
 * de Pyodide transformeraient les `None` en `undefined` et les dictionnaires en
 * `Map`, là où tout le contrat repose sur « une valeur inconnue est `null` ».
 */
export function calculer(document: Document): Resultat {
  if (!pyodide) throw new Error("le moteur n'est pas encore chargé");
  const entree = JSON.stringify(document);
  const sortie = pyodide.runPython(
    `json.dumps(compute(json.loads(${JSON.stringify(entree)})))`,
  );
  return JSON.parse(sortie as string) as Resultat;
}
