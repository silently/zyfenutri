<script lang="ts">
  /**
   * La page : un document entre par des champs, un document sort — le même
   * contrat que `compute()` et que la ligne de commande.
   *
   * ⚠️ Le calcul est celui de CORE, exécuté par Pyodide. Rien n'est recalculé
   * ici, rien n'est réarrondi : la page affiche ce que le moteur rend.
   */
  import { onMount } from 'svelte';
  import {
    CircleAlert,
    CircleQuestionMark,
    Download,
    FileDown,
    Play,
    Plus,
    Printer,
    TriangleAlert,
  } from '@lucide/svelte';
  import logo from '../assets/zyfe.png';
  import Aide from '$lib/composants/Aide.svelte';
  import Etiquette from '$lib/composants/Etiquette.svelte';
  import IntrantChamps from '$lib/composants/Intrant.svelte';
  import {
    MODELE,
    calculVersYaml,
    depuisYaml,
    documentVide,
    intrantVide,
    nomFichier,
    versJson,
    versYaml,
  } from '$lib/document';
  import { calculer, preparer, versionMoteur, type Etat } from '$lib/moteur';
  import { lire } from '$lib/resultat';
  import type { Document, Intrant, Resultat } from '$lib/types';

  /**
   * ⚠️ Chaque ligne porte un `id` stable et son mode. Se repérer par l'INDEX
   * casserait à la première suppression : la carte suivante hériterait du mode
   * de celle qu'on vient de retirer.
   */
  type Ligne = { id: number; intrant: Intrant; edition: boolean };
  let compteur = 0;

  const vide = documentVide();
  let entete = $state({
    recipe: vide.recipe,
    fermentation_hours: vide.fermentation_hours,
  });
  let lignes = $state<Ligne[]>([]);

  const doc = $derived<Document>({ ...entete, ingredients: lignes.map((l) => l.intrant) });
  let etat = $state<Etat>({ phase: 'attente' });
  let resultat = $state<Resultat | null>(null);
  let erreur = $state<string | null>(null);
  let yamlColle = $state('');
  let detailOuvert = $state(false);
  let ignores = $state<string[]>([]);
  let aideOuverte = $state(false);

  const yaml = $derived(versYaml(doc));
  const pret = $derived(etat.phase === 'prêt');
  // ⚠️ `lire` met seulement les manques en français. Aucun jugement n'est
  // repris ici : `complete` vient du moteur — cf. `$lib/resultat`.
  const lecture = $derived(resultat ? lire(resultat) : null);

  onMount(async () => {
    try {
      await preparer((detail) => (etat = { phase: 'chargement', detail }));
      etat = { phase: 'prêt', version: versionMoteur() };
    } catch (e) {
      etat = { phase: 'échec', message: e instanceof Error ? e.message : String(e) };
    }
  });

  function lancer() {
    erreur = null;
    try {
      resultat = calculer(JSON.parse(JSON.stringify(doc)));
    } catch (e) {
      resultat = null;
      erreur = e instanceof Error ? e.message : String(e);
    }
  }

  function ajouter() {
    lignes = [...lignes, { id: ++compteur, intrant: intrantVide(), edition: true }];
  }

  function importer() {
    erreur = null;
    try {
      const relu = depuisYaml(yamlColle);
      entete = {
        recipe: relu.document.recipe,
        fermentation_hours: relu.document.fermentation_hours,
      };
      // Un ingrédient relu est déjà saisi : il s'ouvre en LECTURE, pas en
      // édition — on vient de le fournir, pas de le composer.
      lignes = relu.document.ingredients.map((intrant) => ({
        id: ++compteur,
        intrant,
        edition: false,
      }));
      ignores = relu.ignores;
      yamlColle = '';
      resultat = null;
    } catch (e) {
      erreur = `YAML illisible : ${e instanceof Error ? e.message : String(e)}`;
    }
  }

  function enregistrer(contenu: string, nom: string, type: string) {
    const blob = new Blob([contenu], { type: `${type};charset=utf-8` });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = nom;
    a.click();
    URL.revokeObjectURL(a.href);
  }

  // ⚠️ Le document part avec le MIME du format : un `.json` annoncé en YAML
  // s'ouvre dans le mauvais outil chez celui qui le reçoit.
  const telechargerDocument = (format: 'yml' | 'json') =>
    enregistrer(
      format === 'yml' ? yaml : versJson(doc),
      nomFichier(entete.recipe, `.${format}`),
      format === 'yml' ? 'text/yaml' : 'application/json',
    );

  /**
   * La fiche de calcul complète : valeurs, étiquette, chaîne suivie,
   * coefficients appliqués. C'est CE document qu'on archive et qu'on présente
   * si l'estimation est contestée — pas la page.
   */
  const telechargerCalcul = (format: 'yml' | 'json') =>
    enregistrer(
      format === 'yml' ? calculVersYaml(resultat) : JSON.stringify(resultat, null, 2) + '\n',
      nomFichier(entete.recipe, `-calcul.${format}`),
      format === 'yml' ? 'text/yaml' : 'application/json',
    );

  const telechargerModele = () => enregistrer(MODELE, 'modele-lot.yml', 'text/yaml');
</script>

<div class="min-h-screen bg-base-100">
  <header class="border-b border-base-300 bg-base-200 no-print">
    <!-- ⚠️ UNE seule rangée, jamais deux. Pas de `flex-wrap` : c'est lui qui
         faisait retomber le sous-titre à la ligne et épaississait l'en-tête.
         C'est le sous-titre qui absorbe le manque de place (`min-w-0` +
         `truncate`), parce que c'est le seul élément qu'on peut couper sans
         perdre une fonction. Les tailles sont dans `app.css`. -->
    <div class="max-w-6xl mx-auto px-4 py-1.5 flex items-center gap-3">
      <!-- « zyfe » est le logo, « nutri » s'écrit à la suite : un seul mot,
           deux matières, une seule ligne de base. -->
      <h1 class="flex items-end shrink-0">
        <img src={logo} alt="zyfe" />
        <span class="nutri">nutri</span>
      </h1>
      <p class="text-sm text-base-content/70 flex-1 min-w-0 truncate">
        Estimation de la déclaration nutritionnelle du tempeh
      </p>
      {#if etat.phase === 'prêt'}
        <span class="badge badge-sm badge-ghost shrink-0">moteur {etat.version}</span>
      {/if}
      <button class="btn btn-sm btn-ghost gap-1 shrink-0" onclick={() => (aideOuverte = true)}>
        <CircleQuestionMark size={16} /> Comment ça marche
      </button>
    </div>
  </header>

  <Aide bind:ouverte={aideOuverte} version={etat.phase === 'prêt' ? etat.version : '…'} />

  <main class="max-w-6xl mx-auto px-4 py-6 flex flex-col gap-6">
    {#if etat.phase === 'chargement' || etat.phase === 'attente'}
      <div class="alert no-print">
        <span class="loading loading-spinner loading-sm"></span>
        <span class="text-sm">
          {etat.phase === 'chargement' ? etat.detail : 'Démarrage…'}
        </span>
      </div>
    {:else if etat.phase === 'échec'}
      <div role="alert" class="alert alert-error no-print">
        <CircleAlert size={18} />
        <div class="text-sm">
          <p class="font-semibold">Le moteur n'a pas pu se charger.</p>
          <p>{etat.message}</p>
        </div>
      </div>
    {/if}

    <div class="grid gap-6 lg:grid-cols-[1fr_22rem] items-start">
      <!-- ═══ LE DOCUMENT ═══ -->
      <section class="flex flex-col gap-4 no-print">
        <div class="card bg-base-200 border border-base-300">
          <div class="card-body gap-3 p-4">
            <!-- Les trois réglages du lot tiennent sur une ligne : le nom prend
                 la place restante, les deux durées gardent la leur. -->
            <div class="flex flex-wrap items-end gap-3">
              <fieldset class="fieldset flex-1 min-w-48">
                <legend class="fieldset-legend">Identifiant recette</legend>
                <!-- ⚠️ C'est l'entrée de niveau 1 du document (`recipe:`), et le
                     nom des fichiers téléchargés. -->
                <input
                  class="input input-sm w-full"
                  bind:value={entete.recipe}
                  placeholder="ex : tempeh-soja-nature"
                />
              </fieldset>
              <!-- ⚠️ La fermentation SEULE est un fait du lot : tout le bloc
                   incube ensemble. La cuisson est sur chaque substrat — un soja
                   et une lentille ne cuisent ni le même temps ni dans la même
                   casserole. -->
              <fieldset class="fieldset shrink-0">
                <legend class="fieldset-legend">Fermentation</legend>
                <div class="join">
                  <input type="number" min="0" step="any" class="input input-sm join-item w-20" bind:value={entete.fermentation_hours} />
                  <span class="input input-sm join-item bg-base-200 w-auto px-3 text-base-content/60">h</span>
                </div>
              </fieldset>
            </div>
          </div>
        </div>

        {#each lignes as ligne, i (ligne.id)}
          <IntrantChamps
            bind:intrant={lignes[i].intrant}
            bind:edition={lignes[i].edition}
            supprimer={() => (lignes = lignes.filter((l) => l.id !== ligne.id))}
          />
        {/each}

        {#if lignes.length === 0}
          <p class="text-sm text-base-content/50 border border-dashed border-base-300 rounded-box p-6 text-center">
            Aucun ingrédient. Ajoutez-en un, ou partez du modèle (panneau « Le document »).
          </p>
        {/if}

        <button class="btn btn-sm btn-outline self-start gap-1" onclick={ajouter}>
          <Plus size={14} /> Ajouter un ingrédient
        </button>

        <button class="btn btn-primary gap-2" onclick={lancer} disabled={!pret}>
          <Play size={16} /> Calculer
        </button>

        {#if erreur}
          <div role="alert" class="alert alert-error">
            <CircleAlert size={18} />
            <span class="text-sm">{erreur}</span>
          </div>
        {/if}
      </section>

      <!-- ═══ CE QUI SORT ═══ -->
      <section class="flex flex-col gap-4">
                <div class="card bg-base-200 border border-base-300 no-print">
          <div class="card-body gap-2 p-4">
            <div class="flex items-center justify-between gap-2">
              <h2 class="font-medium text-sm">Données</h2>
              <div class="flex gap-1">
                <button class="btn btn-xs btn-ghost gap-1" onclick={telechargerModele}>
                  <FileDown size={14} /> modèle
                </button>
                <button class="btn btn-xs btn-ghost gap-1" onclick={() => telechargerDocument('yml')}>
                  <Download size={14} /> .yml
                </button>
                <button class="btn btn-xs btn-ghost gap-1" onclick={() => telechargerDocument('json')}>
                  <Download size={14} /> .json
                </button>
              </div>
            </div>
            <!-- ⚠️ Hauteur bornée : le document grandit avec la recette, et
                 « Données » étant au-dessus, un bloc libre repousserait
                 l'étiquette hors de l'écran — on calculerait sans rien voir. -->
            <pre class="bg-base-300 rounded p-2 text-xs overflow-auto max-h-72">{yaml}</pre>
            <p class="text-xs text-base-content/60">
              C'est exactement ce que reçoit <code>compute()</code>, et ce que lit
              <code>zyfenutri lot.yml</code>.
            </p>
            <details>
              <summary class="text-xs cursor-pointer">Repartir d'un document existant</summary>
              <textarea
                class="textarea textarea-sm w-full mt-2 font-mono text-xs"
                rows="5"
                bind:value={yamlColle}
                placeholder="Collez un document YAML…"
              ></textarea>
              <button class="btn btn-xs mt-1" onclick={importer} disabled={!yamlColle.trim()}>
                Charger dans les champs
              </button>
              {#if ignores.length}
                <!-- ⚠️ Ce qui a été laissé de côté se dit : le perdre en silence
                     donnerait un résultat différent sans rien pour l'expliquer. -->
                <div class="alert alert-info mt-2 text-xs">
                  <div>
                    <p class="font-semibold">Laissé de côté à la lecture</p>
                    <ul class="list-disc ml-4 mt-1">
                      {#each ignores as i (i)}<li>{i}</li>{/each}
                    </ul>
                  </div>
                </div>
              {/if}
            </details>
          </div>
        </div>

        {#if resultat && lecture}
          <Etiquette {resultat} complete={lecture.complete} />

          {#if lecture.poidsTempeh}
            <p class="text-xs text-base-content/60 no-print">
              Calculé pour <strong>{lecture.poidsTempeh} g</strong> de tempeh, donnés par les
              facteurs de rendement. Une étiquette porte une valeur moyenne, pas celle d'une
              fournée : c'est le facteur qui se règle, pas le calcul.
            </p>
          {/if}

          {#if lecture.manques.length}
            <div role="alert" class="alert alert-warning no-print">
              <TriangleAlert size={18} />
              <div class="text-sm">
                <p class="font-semibold">Ce qui manque</p>
                <ul class="list-disc ml-4 mt-1">
                  {#each lecture.manques as m (m)}<li>{m}</li>{/each}
                </ul>
              </div>
            </div>
          {/if}

          {#each resultat.warnings as w (w)}
            <div role="alert" class="alert no-print"><TriangleAlert size={18} /><span class="text-sm">{w}</span></div>
          {/each}

          <div class="flex flex-wrap items-center gap-2 no-print">
            <span class="text-xs text-base-content/60">Fiche de calcul complète :</span>
            <button class="btn btn-xs gap-1" onclick={() => telechargerCalcul('yml')}>
              <Download size={13} /> .yml
            </button>
            <button class="btn btn-xs gap-1" onclick={() => telechargerCalcul('json')}>
              <Download size={13} /> .json
            </button>
            <button class="btn btn-xs gap-1" onclick={() => window.print()}>
              <Printer size={13} /> imprimer l'étiquette
            </button>
          </div>

          <div class="collapse collapse-arrow bg-base-200 border border-base-300 no-print">
            <input type="checkbox" bind:checked={detailOuvert} />
            <div class="collapse-title text-sm font-medium">Voir le détail du calcul</div>
            <div class="collapse-content text-sm">
              <!-- ⚠️ La fiche de calcul : c'est elle qu'on présente si l'estimation
                   est contestée. Elle vient du moteur, en français, telle quelle. -->
              <ol class="list-decimal ml-4 flex flex-col gap-1">
                {#each resultat.steps as s (s)}<li>{s}</li>{/each}
              </ol>
            </div>
          </div>
        {:else}
          <div class="border border-dashed border-base-300 rounded-box p-6 text-center text-sm text-base-content/50 no-print">
            L'étiquette apparaîtra ici.
          </div>
        {/if}
      </section>
    </div>
  </main>
</div>
