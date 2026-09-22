<script lang="ts">
  /**
   * L'aide : le principe, le calcul, le droit, les sources — en condensé.
   *
   * ⚠️ Tout ce qui est affirmé ici vient de `refs/methode.md` et
   * `refs/references.md` dans CORE. Rien n'y est inventé : si un chiffre
   * change là-bas, il est faux ici, et c'est ici qu'on le corrige.
   */
  import { X } from '@lucide/svelte';

  let { ouverte = $bindable(), version }: { ouverte: boolean; version: string } = $props();
</script>

<dialog class="modal" open={ouverte}>
  <div class="modal-box max-w-3xl">
    <div class="flex items-start justify-between gap-4 mb-3">
      <h2 class="text-lg font-bold">Comment Zyfe nutri fonctionne</h2>
      <button class="btn btn-sm btn-circle btn-ghost" onclick={() => (ouverte = false)} aria-label="Fermer">
        <X size={18} />
      </button>
    </div>

    <div class="flex flex-col gap-5 text-sm leading-relaxed">
      <section>
        <p>
          Concernant la déclaration nutritionnelle, le règlement <strong><a href="https://www.senat.fr/europe/textes_europeens/ue0120.pdf" target="_blank">(UE) 1169/2011</a></strong>, article 31 §4, met trois méthodes <em>à égalité</em> : l'analyse en laboratoire, le calcul à partir des ingrédients, et le calcul à partir de données établies. Un laboratoire n'est donc pas obligatoire — à condition que le calcul repose sur des données et connaissances fiables.
        </p>
        <p class="mt-1">
          Zyfe nutri propose un calcul de valeur nutritionnelle moyenne pour 100g de tempeh en prenant en compte les étapes de fabrication susceptibles d'en modifier la composition. Ce calcul repose sur des références scientifiques (TODO link) ainsi que des analyses officielles comparant déclaration nutritionnelle de la graine de soja et son tempeh (TODO link), mais les coefficients appliqués n'ont pas été testés en laboratoire et demeurent donc des hypothèses au mieux des connaissances disponibles au projet.
        </p>
      </section>

      <section class="mt-2">
        <h3 class="font-semibold mb-1">À vos risques et périls</h3>
        <p>
          Cet outil est fourni à titre indicatif, il reste améliorable (tout commentaire ou référence scientifique permettant de l'améliorer peut être proposé en <a href="https://github.com/silently/zyfenutri/issues" target="_blank">ouvrant un ticket</a>) et sans garantie. Il peut être intéressant de le confronter à des résultats en laboratoire.
        </p>
        <p>
          Si l'outil peut induire en erreur, ne pas oublier que les déclarations nutritionnelles des ingrédients peuvent elles aussi être erronées.
        </p>
      </section>

      <section class="mt-2">
        <h3 class="font-semibold mb-1">Les données nécessaires pour utiliser Zyfe nutri</h3>
        <p>
          Pour fonctionner, Zyfe nutri a besoin :
        </p>
        <ul class="list-disc ml-5">
          <li>des valeurs nutritionnelles (pour 100g) de chaque ingrédient (sauf le starter, négligé)</li>
          <li>du facteur de rendement (voir ci-après) des ingrédients de type substrat (légumineuse, céréale) dû notamment à l'hydratation des graines sèches</li>
          <li>de quelques infos sur votre process (dépelliculage ou non, durée de cuisson et de fermentation)</li>
        </ul>
        <p class="mt-1">
          Une valeur inconnue n'est pas une valeur nulle :
        </p>
        <ul class="list-disc ml-5">
          <li>0 signifie "absence de"</li>
          <li>un champ laissé vide signifie "valeur inconnue". Zyfe nutri ne pourra pas produire d'estimation sur cette dimension et indiquera un tiret en sortie</li>
        </ul>
      </section>

      <section class="mt-2">
        <h3 class="font-semibold mb-1">Le principe : des transformations...</h3>
        <p>
          On considère et on mesure l'effet des transformations suivantes selon le type d'ingrédient :
        </p>
        <ul class="list-disc ml-5">
          <li><strong>Substrat</strong> (légumineuse, céréale, oléagineux) : dépelliculage (optionnel) → trempage (dont rinçage) → cuisson (dont égouttage) → fermentation</li>
          <li><strong>Support d'inoculation</strong> (farine ou kinako): torréfaction (optionnelle) → fermentation</li>
          <li><strong>Acidifiant pré-inoculation</strong> : sans transformation</li>
          <li><strong>Starter</strong> : négligeable</li>
        </ul>
      </section>

      <section class="mt-2">
        <h3 class="font-semibold mb-1">...et une règle de trois</h3>
        <p>
          On génère la fiche nutritionnelle pour 100g de tempeh selon :
        </p>
        <ul class="list-disc ml-5">
          <li>la proportion de chaque ingrédient (en masse sèche pour les substrats)</li>
          <li>l'effet des transformations</li>
          <li>mais aussi le <strong>facteur de rendement</strong> des substrats</li>
        </ul>
      </section>
      <section class="mt-2">
        <h3 class="font-semibold mb-1">Le facteur de rendement</h3>
        <p>
          Ce facteur, obligatoire et à donner <strong>indépendamment pour chaque substrat</strong> (soja, lentille verte, pois chiche...), donne l'évolution de la masse de ce substrat sur l'ensemble de la fabrication. Il inclut : 
        </p>
        <ul class="list-disc ml-5">
          <li>les pertes : dépelliculage si effectué après réception, pertes de matière pendant les opérations, perte d'eau durant pendant la fermentation</li>
          <li>les gains, plus importants, dûs au gonflement lors du trempage et de la cuisson</li>
        </ul>
      </section>

      <section class="mt-2">
        <h3 class="font-semibold mb-1">L'énergie est calculée à la fin</h3>
        <p>
          L'énergie est calculée d'après les macronutriments estimés et grâce aux coefficients de l'<strong>annexe XIV</strong>. Les déclarations énergétiques des ingrédients ne sont donc pas utilisées.
        </p>
      </section>

      <section class="mt-2">
        <h3 class="font-semibold mb-1">Format de la déclaration nutritionnelle générée</h3>
        <p class="mb-1">Les valeurs sont arrondies en dernière étape (voir le tableau 4 du guide de décembre 2012) :</p>
        <table class="table table-xs">
          <tbody>
            <tr><td>Énergie</td><td>à l'unité de kJ / kcal</td></tr>
            <tr><td>Macronutriments ≥ 10 g</td><td>au gramme</td></tr>
            <tr><td>&lt; 10 g et &gt; 0,5 g</td><td>au décigramme</td></tr>
            <tr><td>≤ 0,5 g</td><td>« &lt; 0,5 g »</td></tr>
            <tr><td>AGS ≤ 0,1 g</td><td>« &lt; 0,1 g »</td></tr>
            <tr><td>Sel ≥ 1 g</td><td>au décigramme</td></tr>
            <tr><td>Sel &lt; 1 g et &gt; 0,0125 g</td><td>au centigramme</td></tr>
            <tr><td>Sel ≤ 0,0125 g</td><td>« &lt; 0,01 g »</td></tr>
          </tbody>
        </table>
        <p class="mt-2 mb-1">À noter les tolérances admises (incertitude de mesure comprise) :</p>
        <table class="table table-xs">
          <tbody>
            <tr><td>Glucides, sucres, protéines, fibres</td><td>&lt; 10 g : ± 2 g · 10–40 g : ± 20 % · &gt; 40 g : ± 8 g</td></tr>
            <tr><td>Matières grasses</td><td>&lt; 10 g : ± 1,5 g · 10–40 g : ± 20 % · &gt; 40 g : ± 8 g</td></tr>
            <tr><td>Acides gras saturés</td><td>&lt; 4 g : ± 0,8 g · ≥ 4 g : ± 20 %</td></tr>
            <tr><td>Sel</td><td>&lt; 1,25 g : ± 0,375 g · ≥ 1,25 g : ± 20 %</td></tr>
          </tbody>
        </table>
      </section>

      <section class="mt-2">
        <h3 class="font-semibold mb-1">Les sources</h3>
        <p class="mb-1">
          Dix-neuf références scientifiques, chacune avec son statut (lue, résumé, non lue) et ce
          qu'on en tire. Un chiffre n'est cité que d'une source <strong>lue</strong>. Les
          principales :
        </p>
        <ul class="list-disc ml-5 text-xs">
          <li>[1] Shurtleff &amp; Aoyagi, 1980 — <em>Tempeh Production</em> : rendements et pertes de solides par étape</li>
          <li>[2] de Reu et al., 1994 — <em>Changes in soya bean lipids during tempe fermentation</em></li>
          <li>[6] de Reu et al., 1995 — <em>Protein hydrolysis during soybean tempe fermentation</em></li>
          <li>[11] Liu, 1997 — <em>Soybeans: Chemistry, Technology, and Utilization</em></li>
          <li>[15] Ashenafi &amp; Busse, 1991 — <em>Production of tempeh from various indigenous Ethiopian beans</em></li>
        </ul>
        <p class="mt-2">
          Le détail — la méthode, chaque coefficient et sa source — est dans le dépôt :
          <code>refs/methode.md</code>, <code>refs/references.md</code> et
          <code>refs/transformations.md</code>.
        </p>
        <p class="mt-2">
          <a
            class="link"
            href="https://github.com/silently/zyfenutri"
            target="_blank"
            rel="noopener noreferrer">github.com/silently/zyfenutri</a
          >
          · moteur {version}
        </p>
      </section>
    </div>
  </div>
  <button class="modal-backdrop" onclick={() => (ouverte = false)} aria-label="Fermer">fermer</button>
</dialog>
