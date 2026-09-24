<script lang="ts">
  /**
   * Un ingrédient du lot, dans une carte à deux états : on le saisit, on le
   * valide, on le relit. Modifier ou supprimer se fait depuis la lecture.
   *
   * ⚠️ Valider ne BLOQUE jamais. Une lacune se dit — elle est signalée dans la
   * vue de lecture, et `missing` la reprendra au calcul. Refuser la saisie
   * ferait perdre le reste de ce qui est déjà juste.
   *
   * ⚠️ Les champs numériques sont vides par défaut et le restent : un champ
   * vide vaut « on ne sait pas ». Rien n'est pré-rempli à zéro.
   */
  import { Check, Pencil, Trash2, TriangleAlert } from '@lucide/svelte';
  import { LIBELLES, NUTRIMENTS, ROLES, porteUneFiche, type Intrant } from '$lib/types';

  let {
    intrant = $bindable(),
    edition = $bindable(),
    supprimer,
  }: {
    intrant: Intrant;
    edition: boolean;
    supprimer: () => void;
  } = $props();

  const role = $derived(ROLES.find((r) => r.valeur === intrant.role));
  const estSubstrat = $derived(intrant.role === 'substrate');
  const estSupport = $derived(intrant.role === 'support');
  const aUneFiche = $derived(porteUneFiche(intrant.role));

  /** Les lignes « dont » : elles se renfoncent, comme sur une étiquette. */
  const SOUS_TOTAL = new Set(['saturates', 'sugars']);

  /**
   * Ce qui empêchera un calcul complet. Dit, jamais bloquant.
   *
   * ⚠️ Un rôle exclu du calcul ne réclame RIEN. Le moteur écarte le starter
   * avant toute vérification : ni son poids ni sa fiche n'entrent nulle part,
   * et aucun `missing` ne le cite. Signaler un manque chez lui ferait croire
   * à un défaut qui ne peut pas exister.
   */
  const lacunes = $derived.by(() => {
    if (!aUneFiche) return [];
    const out: string[] = [];
    if (!intrant.name?.trim()) out.push('pas de nom');
    if (intrant.weight_g == null) out.push('pas de poids');
    if (estSubstrat && intrant.yield == null) out.push('pas de facteur de rendement');
    if (estSubstrat && intrant.cooking_minutes == null) out.push('pas de durée de cuisson');
    if (aUneFiche) {
      const absents = NUTRIMENTS.filter((n) => intrant.per_100g?.[n] == null);
      if (absents.length === NUTRIMENTS.length) out.push('pas de composition');
      else if (absents.length) out.push(`${absents.length} valeur${absents.length > 1 ? 's' : ''} de composition manquante${absents.length > 1 ? 's' : ''}`);
    }
    return out;
  });
</script>

<div class="card bg-base-200 border border-base-300">
  <div class="card-body gap-3 p-4">
    {#if edition}
      <!-- ═══ SAISIE ═══ -->
      <fieldset class="fieldset">
        <legend class="fieldset-legend">Nom</legend>
        <input
          class="input input-sm w-full"
          bind:value={intrant.name}
          placeholder="ex : Soja, Vinaigre de cidre"
        />
      </fieldset>

      <div class="grid gap-3 sm:grid-cols-2">
        <fieldset class="fieldset">
          <legend class="fieldset-legend">Rôle</legend>
          <select class="select select-sm w-full" bind:value={intrant.role}>
            {#each ROLES as r (r.valeur)}
              <option value={r.valeur}>{r.libelle}</option>
            {/each}
          </select>
          {#if role}
            <p class="text-xs text-base-content/60 mt-1">{role.aide}</p>
          {/if}
        </fieldset>

        <fieldset class="fieldset">
          <legend class="fieldset-legend">Poids</legend>
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
          {#if estSubstrat}
            <p class="text-xs text-base-content/60 mt-1">
              Le poids <strong>avant</strong> toute transformation — pellicule comprise si
              vous la retirez vous-même.
            </p>
          {/if}
        </fieldset>
      </div>

      {#if estSubstrat}
        <div class="grid gap-3 sm:grid-cols-2">
          <fieldset class="fieldset">
            <legend class="fieldset-legend">
              Cuisson <span class="text-error">*</span>
            </legend>
            <div class="join">
              <input
                type="number"
                min="0"
                step="any"
                class="input input-sm join-item w-20 {intrant.cooking_minutes == null
                  ? 'input-error'
                  : ''}"
                bind:value={intrant.cooking_minutes}
                required
              />
              <span class="input input-sm join-item bg-base-200 w-auto px-3 text-base-content/60">min</span>
            </div>
            <!-- ⚠️ Par SUBSTRAT, pas par lot : un soja et une lentille ne cuisent
                 ni le même temps ni dans la même casserole, et tous les
                 coefficients de cuisson sont fonction du temps. -->
            <p class="text-xs text-base-content/60 mt-1">
              Le temps de cuisson <strong>de cet ingrédient</strong>. Chacun cuit le sien.
            </p>
          </fieldset>

          <fieldset class="fieldset">
            <legend class="fieldset-legend">Dépelliculage</legend>
            <label class="label cursor-pointer justify-start gap-2">
              <input
                type="checkbox"
                class="checkbox checkbox-sm checkbox-primary"
                bind:checked={intrant.dehulled}
              />
              <span class="label-text">Nous le dépelliculons ici</span>
            </label>
            <!-- ⚠️ La question est bien « QUI le fait ». Une graine achetée déjà
                 décortiquée porte le résultat dans sa composition et dans son
                 poids : la cocher retirerait une pellicule une seconde fois. -->
            <p class="text-xs text-base-content/60 mt-1">
              À cocher seulement si <strong>vous</strong> retirez la pellicule. Une graine
              achetée déjà décortiquée : laissez décoché, sa fiche en tient déjà compte.
            </p>
          </fieldset>

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
            <p class="text-xs text-base-content/60 mt-1">
              kg de tempeh pour 1 kg de graines brutes. Un seul nombre, qui contient
              <strong>tout</strong> : le dépelliculage et les pertes, le gonflement au
              trempage et à la cuisson, la déshydratation pendant la fermentation.
            </p>
          </fieldset>
        </div>
      {/if}

      {#if estSupport}
        <fieldset class="fieldset">
          <legend class="fieldset-legend">Torréfaction</legend>
          <label class="label cursor-pointer justify-start gap-2">
            <input
              type="checkbox"
              class="checkbox checkbox-sm checkbox-primary"
              bind:checked={intrant.roasted}
            />
            <span class="label-text">Nous le torréfions ici</span>
          </label>
          <p class="text-xs text-base-content/60 mt-1">
            À cocher seulement si <strong>vous</strong> torréfiez. Une farine achetée déjà
            torréfiée porte le résultat dans sa composition.
          </p>
        </fieldset>
      {/if}

      {#if aUneFiche}
        <div>
          <p class="fieldset-legend mb-1">Composition pour 100 g de produit brut</p>
          <!-- ⚠️ UN nutriment par ligne. Recopier une fiche produit, c'est lire
               une colonne : sur plusieurs colonnes, l'œil saute une ligne sans
               s'en apercevoir, et une valeur se retrouve en face du mauvais
               libellé. Les « dont » se renfoncent, comme sur une étiquette. -->
          <div class="flex flex-col">
            {#each NUTRIMENTS as n (n)}
              <label
                class="flex items-center gap-2 text-sm border-b border-base-300/60 py-1
                  {SOUS_TOTAL.has(n) ? 'pl-4' : ''}"
              >
                <span class="flex-1 text-base-content/70">{LIBELLES[n]}</span>
                <input
                  type="number"
                  min="0"
                  step="any"
                  class="input input-xs w-24 tabular-nums"
                  bind:value={intrant.per_100g![n]}
                />
                <span class="text-xs text-base-content/50 w-3">g</span>
              </label>
            {/each}
          </div>
          <p class="text-xs text-base-content/60 mt-1">
            Laissé vide = inconnu. La valeur du produit le sera aussi.
          </p>
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

      <div class="flex gap-2">
        <button class="btn btn-sm btn-primary gap-1" onclick={() => (edition = false)}>
          <Check size={14} /> Valider
        </button>
        <button class="btn btn-sm btn-ghost text-error gap-1" onclick={supprimer}>
          <Trash2 size={14} /> Supprimer
        </button>
      </div>
    {:else}
      <!-- ═══ LECTURE ═══ -->
      <div class="flex items-start justify-between gap-2">
        <div class="flex items-baseline gap-2 flex-wrap">
          <span class="font-semibold">{intrant.name?.trim() || 'Sans nom'}</span>
          <span class="badge badge-sm badge-soft badge-secondary">{role?.libelle ?? intrant.role}</span>
          {#if intrant.weight_g != null}
            <span class="text-sm text-base-content/70 tabular-nums">{intrant.weight_g} g</span>
          {/if}
        </div>
        <div class="flex gap-1 shrink-0">
          <button class="btn btn-xs btn-ghost gap-1" onclick={() => (edition = true)}>
            <Pencil size={13} /> Modifier
          </button>
          <button class="btn btn-xs btn-ghost text-error" onclick={supprimer} aria-label="Supprimer">
            <Trash2 size={13} />
          </button>
        </div>
      </div>

      <div class="flex flex-wrap gap-x-4 gap-y-1 text-xs text-base-content/70">
        {#if estSubstrat}
          <span>Dépelliculage : <strong>{intrant.dehulled ? 'par nous' : 'non'}</strong></span>
          <span>
            Rendement :
            <strong class={intrant.yield == null ? 'text-error' : ''}>
              {intrant.yield ?? 'manquant'}
            </strong>
          </span>
          <span>
            Cuisson :
            <strong class={intrant.cooking_minutes == null ? 'text-error' : ''}>
              {intrant.cooking_minutes != null ? `${intrant.cooking_minutes} min` : 'manquante'}
            </strong>
          </span>
        {/if}
        {#if estSupport}
          <span>Torréfaction : <strong>{intrant.roasted ? 'par nous' : 'non'}</strong></span>
        {/if}
      </div>

      {#if aUneFiche}
        <p class="text-xs text-base-content/50">Composition, en g pour 100 g de produit brut</p>
        <div class="flex flex-col text-xs">
          {#each NUTRIMENTS as n (n)}
            <div
              class="flex justify-between gap-2 border-b border-base-300/60 py-0.5
                {SOUS_TOTAL.has(n) ? 'pl-4' : ''}"
            >
              <span class="text-base-content/60">{LIBELLES[n]}</span>
              <!-- ⚠️ Un tiret, jamais « 0 » : « on ne sait pas » et « il n'y en a
                   pas » sont deux affirmations différentes. -->
              <span class="tabular-nums">{intrant.per_100g?.[n] ?? '—'}</span>
            </div>
          {/each}
        </div>
      {/if}

      {#if lacunes.length}
        <p class="text-xs text-warning-content bg-warning rounded px-2 py-1 flex items-center gap-1">
          <TriangleAlert size={13} />
          {lacunes.join(' · ')}
        </p>
      {/if}
    {/if}
  </div>
</div>
