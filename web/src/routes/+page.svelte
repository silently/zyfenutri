<script lang="ts">
  /**
   * La page : un document entre par des champs, un document sort — le même
   * contrat que `compute()` et que la ligne de commande.
   *
   * ⚠️ Le calcul est celui de CORE, exécuté par Pyodide. Rien n'est recalculé
   * ici, rien n'est réarrondi : la page affiche ce que le moteur rend.
   */
  import { onMount } from 'svelte';
  import { CircleAlert, CircleQuestionMark, Download, FileDown, Play, Plus, TriangleAlert } from '@lucide/svelte';
  import Aide from '$lib/composants/Aide.svelte';
  import Etiquette from '$lib/composants/Etiquette.svelte';
  import IntrantChamps from '$lib/composants/Intrant.svelte';
  import { MODELE, depuisYaml, documentVide, intrantVide, versYaml } from '$lib/document';
  import { calculer, preparer, versionMoteur, type Etat } from '$lib/moteur';
  import { lire } from '$lib/resultat';
  import type { Resultat } from '$lib/types';

  let doc = $state(documentVide());
  let etat = $state<Etat>({ phase: 'attente' });
  let resultat = $state<Resultat | null>(null);
  let erreur = $state<string | null>(null);
  let yamlColle = $state('');
  let detailOuvert = $state(false);
  let ignores = $state<string[]>([]);
  let aideOuverte = $state(false);

  const yaml = $derived(versYaml(doc));
  const pret = $derived(etat.phase === 'prêt');
  // ⚠️ `lire` lève la réserve sur le poids de récolte et met les manques en
  // français. Ce que CORE rend n'est pas touché — cf. `$lib/resultat`.
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

  function importer() {
    erreur = null;
    try {
      const relu = depuisYaml(yamlColle);
      doc = relu.document;
      ignores = relu.ignores;
      yamlColle = '';
      resultat = null;
    } catch (e) {
      erreur = `YAML illisible : ${e instanceof Error ? e.message : String(e)}`;
    }
  }

  function enregistrer(contenu: string, nom: string) {
    const blob = new Blob([contenu], { type: 'text/yaml;charset=utf-8' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = nom;
    a.click();
    URL.revokeObjectURL(a.href);
  }

  const telecharger = () => enregistrer(yaml, `${doc.recipe?.trim() || 'lot'}.yml`);
  const telechargerModele = () => enregistrer(MODELE, 'modele-lot.yml');
</script>

<div class="min-h-screen bg-base-100">
  <header class="border-b border-base-300 bg-base-200 no-print">
    <div class="max-w-6xl mx-auto px-4 py-4 flex items-baseline gap-3 flex-wrap">
      <h1 class="text-xl font-bold">zyfenutri</h1>
      <p class="text-sm text-base-content/70 flex-1">
        Ce qu'on a mis dans un lot de tempeh → ce qu'on a le droit d'écrire sur l'étiquette
      </p>
      {#if etat.phase === 'prêt'}
        <span class="badge badge-sm badge-ghost">moteur {etat.version}</span>
      {/if}
      <button class="btn btn-sm btn-ghost gap-1" onclick={() => (aideOuverte = true)}>
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
            <fieldset class="fieldset">
              <legend class="fieldset-legend">Recette</legend>
              <input class="input input-sm w-full" bind:value={doc.recipe} placeholder="ex : Tempeh de soja nature" />
            </fieldset>
            <div class="grid gap-3 sm:grid-cols-2">
              <fieldset class="fieldset">
                <legend class="fieldset-legend">Cuisson</legend>
                <div class="join">
                  <input type="number" min="0" step="any" class="input input-sm join-item w-20" bind:value={doc.cooking_minutes} />
                  <span class="input input-sm join-item bg-base-200 w-auto px-3 text-base-content/60">min</span>
                </div>
              </fieldset>
              <fieldset class="fieldset">
                <legend class="fieldset-legend">Fermentation</legend>
                <div class="join">
                  <input type="number" min="0" step="any" class="input input-sm join-item w-20" bind:value={doc.fermentation_hours} />
                  <span class="input input-sm join-item bg-base-200 w-auto px-3 text-base-content/60">h</span>
                </div>
              </fieldset>
            </div>
          </div>
        </div>

        {#each doc.ingredients as _, i (i)}
          <IntrantChamps
            bind:intrant={doc.ingredients[i]}
            index={i}
            supprimable={doc.ingredients.length > 1}
            supprimer={() => (doc.ingredients = doc.ingredients.filter((_, j) => j !== i))}
          />
        {/each}

        <button
          class="btn btn-sm btn-outline self-start gap-1"
          onclick={() => (doc.ingredients = [...doc.ingredients, intrantVide()])}
        >
          <Plus size={14} /> Ajouter un intrant
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
        {#if resultat && lecture}
          <Etiquette {resultat} complete={lecture.complete} />

          {#if lecture.poidsPredit}
            <p class="text-xs text-base-content/60 no-print">
              Calculé pour <strong>{lecture.poidsPredit} g</strong> de tempeh, prédits par les
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

        <div class="card bg-base-200 border border-base-300 no-print">
          <div class="card-body gap-2 p-4">
            <div class="flex items-center justify-between gap-2">
              <h2 class="font-medium text-sm">Le document</h2>
              <div class="flex gap-1">
                <button class="btn btn-xs btn-ghost gap-1" onclick={telechargerModele}>
                  <FileDown size={14} /> modèle
                </button>
                <button class="btn btn-xs btn-ghost gap-1" onclick={telecharger}>
                  <Download size={14} /> .yml
                </button>
              </div>
            </div>
            <pre class="bg-base-300 rounded p-2 text-xs overflow-x-auto">{yaml}</pre>
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
      </section>
    </div>
  </main>
</div>
