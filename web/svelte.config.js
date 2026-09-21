import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

// ⚠️ Sur GitHub Pages, le site vit sous `/<dépôt>/`, pas à la racine : sans ce
// préfixe, chaque ressource — y compris les modules de CORE — serait cherchée
// un cran trop haut et la page resterait vide. La CI le fournit ; en local il
// est absent, et le site se sert bien depuis `/`.
const base = process.env.BASE_PATH ?? '';

/** @type {import('@sveltejs/kit').Config} */
export default {
  preprocess: vitePreprocess(),
  kit: {
    // ⚠️ Page STATIQUE : ce qui sort de `build` s'ouvre sans rien lancer.
    // Aucun serveur, aucune base — cf. CLAUDE.md § CORE et WEB.
    adapter: adapter({ pages: 'build', assets: 'build', fallback: '404.html' }),
    paths: { base },
  },
};
