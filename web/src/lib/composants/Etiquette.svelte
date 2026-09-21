<script lang="ts">
  /**
   * La déclaration nutritionnelle, telle qu'elle s'écrit sur un emballage.
   *
   * ⚠️ Les mentions viennent de `label` et s'affichent **telles quelles**.
   * On ne les reformate jamais : CORE les a arrondies une fois, selon le
   * tableau 4, et un second arrondi déplacerait le chiffre d'une unité.
   *
   * ⚠️ Une valeur inconnue est un tiret, jamais « 0 g » : « il n'y en a pas »
   * est une affirmation, et elle engage.
   */
  import { LIBELLES, NUTRIMENTS, type Resultat } from '$lib/types';

  // ⚠️ `complete` vient de la LECTURE, pas de `resultat.complete` : sans poids
  // récolté, CORE réserve à raison son jugement, et c'est cette page qui lève
  // cette réserve-là — et elle seule (cf. `$lib/resultat`).
  let { resultat, complete }: { resultat: Resultat; complete: boolean } = $props();

  // Les lignes « dont » se renfoncent, comme sur une étiquette.
  const RENFONCE = new Set(['saturates', 'sugars']);
</script>

<div class="border border-base-content/30 bg-base-100 p-4 max-w-sm">
  <h3 class="font-bold text-lg border-b-4 border-base-content pb-1">
    Déclaration nutritionnelle
  </h3>
  <p class="text-xs text-base-content/60 mt-1">pour 100 g de produit fini</p>

  <table class="w-full text-sm mt-2">
    <tbody>
      <tr class="border-b border-base-content/20">
        <th class="text-left font-semibold py-1">Énergie</th>
        <td class="text-right py-1 tabular-nums">{resultat.label.energy ?? '—'}</td>
      </tr>
      {#each NUTRIMENTS as n (n)}
        <tr class="border-b border-base-content/20">
          <th
            class="text-left py-1 {RENFONCE.has(n) ? 'pl-4 font-normal' : 'font-semibold'}"
          >
            {LIBELLES[n]}
          </th>
          <td class="text-right py-1 tabular-nums">{resultat.label[n] ?? '—'}</td>
        </tr>
      {/each}
    </tbody>
  </table>

  {#if !complete}
    <p class="text-xs mt-3 font-semibold text-warning-content bg-warning px-2 py-1">
      Estimation incomplète — ne pas étiqueter avec ces valeurs.
    </p>
  {/if}
</div>
