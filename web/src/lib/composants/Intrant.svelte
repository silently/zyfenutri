<script lang="ts">
  /**
   * Un intrant du lot : ce qu'il est, ce qu'il pèse, ce qu'il contient.
   *
   * ⚠️ Les champs numériques sont vides par défaut et le restent : un champ
   * vide vaut « on ne sait pas ». Rien n'est pré-rempli à zéro.
   */
  import { Trash2 } from '@lucide/svelte';
  import { LIBELLES, NUTRIMENTS, ROLES, porteUneFiche, type Intrant } from '$lib/types';

  let {
    intrant = $bindable(),
    index,
    supprimable,
    supprimer,
  }: {
    intrant: Intrant;
    index: number;
    supprimable: boolean;
    supprimer: () => void;
  } = $props();

  const role = $derived(ROLES.find((r) => r.valeur === intrant.role));
  const estSubstrat = $derived(intrant.role === 'substrate');
  const estSupport = $derived(intrant.role === 'support');
  const aUneFiche = $derived(porteUneFiche(intrant.role));
</script>

<div class="card bg-base-200 border border-base-300">
  <div class="card-body gap-3 p-4">
    <div class="flex items-end gap-2">
      <fieldset class="fieldset flex-1">
        <legend class="fieldset-legend">Nom</legend>
        <input
          class="input input-sm w-full"
          bind:value={intrant.name}
          placeholder="ex : Soja, Vinaigre de cidre"
        />
      </fieldset>
      {#if supprimable}
        <button
          class="btn btn-sm btn-ghost text-error"
          onclick={supprimer}
          aria-label="Retirer l'intrant {index + 1}"
        >
          <Trash2 size={16} />
        </button>
      {/if}
    </div>

    <div class="grid gap-3 sm:grid-cols-2">
      <fieldset class="fieldset">
        <legend class="fieldset-legend">Rôle</legend>
        <select class="select select-sm w-full" bind:value={intrant.role}>
          {#each ROLES as r (r.valeur)}
            <option value={r.valeur}>{r.libelle}</option>
          {/each}
        </select>
        {#if role}
          <p class="label text-xs">{role.aide}</p>
        {/if}
      </fieldset>

      <fieldset class="fieldset">
        <legend class="fieldset-legend">
          Poids {estSubstrat ? 'brut, pellicule comprise' : ''}
        </legend>
        <div class="join">
          <input
            type="number"
            min="0"
            step="any"
            class="input input-sm join-item w-28"
            bind:value={intrant.weight_g}
          />
          <span class="input input-sm join-item bg-base-200 w-auto px-3 text-base-content/60">g</span>
        </div>
      </fieldset>
    </div>

    {#if estSubstrat || estSupport}
      <div class="flex flex-wrap gap-4">
        {#if estSubstrat}
          <label class="label cursor-pointer gap-2">
            <input type="checkbox" class="checkbox checkbox-sm" bind:checked={intrant.dehulled} />
            <span class="label-text">Dépelliculé</span>
          </label>
          <fieldset class="fieldset">
            <legend class="fieldset-legend">
              Facteur de rendement <span class="text-error">*</span>
            </legend>
            <input
              type="number"
              min="0"
              step="any"
              class="input input-sm w-24 {intrant.yield == null ? 'input-error' : ''}"
              bind:value={intrant.yield}
              placeholder="1.75"
              required
            />
            <!-- ⚠️ OBLIGATOIRE, et c'est le seul dénominateur : la fiche ne
                 dépend d'aucun poids de récolte. Un lot qui pèse autrement ne
                 change pas ce qu'on imprime — c'est ce facteur qu'on règle. -->
            <p class="label text-xs whitespace-normal">
              kg de tempeh pour 1 kg de graines brutes. Un seul nombre, qui contient
              <strong>tout</strong> : le dépelliculage et les pertes, le gonflement au
              trempage et à la cuisson, la déshydratation pendant la fermentation.
            </p>
          </fieldset>
        {/if}
        {#if estSupport}
          <label class="label cursor-pointer gap-2">
            <input type="checkbox" class="checkbox checkbox-sm" bind:checked={intrant.roasted} />
            <span class="label-text">Torréfié par nous</span>
          </label>
        {/if}
      </div>
    {/if}

    {#if aUneFiche}
      <div>
        <p class="fieldset-legend mb-1">Composition pour 100 g de produit brut</p>
        <div class="grid gap-2 sm:grid-cols-2 lg:grid-cols-3">
          {#each NUTRIMENTS as n (n)}
            <label class="flex items-center gap-2 text-sm">
              <span class="flex-1 text-base-content/70">{LIBELLES[n]}</span>
              <input
                type="number"
                min="0"
                step="any"
                class="input input-xs w-20 tabular-nums"
                bind:value={intrant.per_100g![n]}
              />
              <span class="text-xs text-base-content/50 w-3">g</span>
            </label>
          {/each}
        </div>
        <p class="label text-xs mt-1">Laissé vide = inconnu. La valeur du produit le sera aussi.</p>
      </div>
    {:else}
      <!-- ⚠️ Pas de champs de composition : le starter ne pèse que quelques
           grammes pour des kilos de produit, le moteur l'exclut du calcul.
           Lui demander une fiche serait demander une donnée qui ne sert pas. -->
      <p class="text-xs text-base-content/60 bg-base-300 rounded px-2 py-1">
        Pas de fiche nutritionnelle : le starter ne compte que par son poids et sa
        proportion dans la recette. Le moteur l'exclut du calcul — quelques grammes
        pour des kilos de produit.
      </p>
    {/if}
  </div>
</div>
