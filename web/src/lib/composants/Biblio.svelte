<script lang="ts">
  /**
   * La bibliographie complète — titres, auteurs, statut de lecture.
   *
   * ⚠️ Les données viennent de `refs/references.md`, extraites à la
   * construction (`scripts/sync-refs.mjs`). On ne recopie RIEN ici : une
   * seconde liste divergerait de l'index, et c'est l'index qui fait foi.
   *
   * ⚠️ Le statut s'affiche, il ne se cache pas. « Un chiffre n'est cité que
   * d'une source LUE » : sans le statut, on ne peut pas savoir ce qui fonde
   * quoi.
   */
  import { onMount } from 'svelte';
  import { base } from '$app/paths';

  type Reference = {
    numero: number;
    court: string;
    titre: string;
    citation: string;
    lien: string | null;
    statut: string;
  };

  let references = $state<Reference[]>([]);
  let echec = $state(false);

  onMount(async () => {
    try {
      references = await (await fetch(`${base}/core/references.json`)).json();
    } catch {
      echec = true;
    }
  });

  const TEINTE: Record<string, string> = {
    lu: 'badge-success',
    résumé: 'badge-warning',
    'non lu': 'badge-ghost',
    retirée: 'badge-error',
  };
</script>

{#if echec}
  <p class="text-xs text-base-content/50">
    Bibliographie indisponible — elle est dans le dépôt, <code>refs/references.md</code>.
  </p>
{:else if references.length}
  <ol class="flex flex-col gap-2 text-xs">
    {#each references as r (r.numero)}
      <li class="flex gap-2">
        <span class="text-base-content/40 tabular-nums shrink-0">[{r.numero}]</span>
        <span>
          {#if r.lien}
            <a class="link" href={r.lien} target="_blank" rel="noopener noreferrer">{r.citation}</a>
          {:else}
            {r.citation}
          {/if}
          <span class="badge badge-xs {TEINTE[r.statut] ?? 'badge-ghost'} ml-1 align-middle">
            {r.statut}
          </span>
        </span>
      </li>
    {/each}
  </ol>
{/if}
