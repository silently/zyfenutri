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
      <h2 class="text-lg font-bold">Comment ce calcul fonctionne</h2>
      <button class="btn btn-sm btn-circle btn-ghost" onclick={() => (ouverte = false)} aria-label="Fermer">
        <X size={18} />
      </button>
    </div>

    <div class="flex flex-col gap-5 text-sm leading-relaxed">
      <section>
        <h3 class="font-semibold mb-1">Calculer est une méthode légale</h3>
        <p>
          Le règlement <strong>(UE) 1169/2011</strong>, article 31 §4, met trois méthodes
          <em>à égalité</em> : l'analyse en laboratoire, le calcul à partir des ingrédients, et le
          calcul à partir de données établies. Le « ou » n'introduit aucune hiérarchie. Un
          laboratoire n'est donc pas obligatoire — à condition que le calcul repose sur des données
          fiables et qu'il soit <strong>documenté</strong>.
        </p>
        <p class="mt-1">
          Les valeurs déclarées sont des <strong>valeurs moyennes</strong>, pas des maxima ni des
          garanties.
        </p>
      </section>

      <section>
        <h3 class="font-semibold mb-1">Le principe : on ne divise qu'une fois</h3>
        <p>
          Le calcul ne manipule que des <strong>masses absolues</strong> de nutriments, du début à
          la fin. On part de ce qui entre dans le lot, on applique à chaque intrant les
          transformations qu'il subit, on additionne, et on divise <strong>une seule fois</strong>
          par le poids de tempeh obtenu.
        </p>
        <p class="mt-1">
          C'est la clé : cette division finale, et elle seule, porte l'eau reprise au trempage. Un
          lot qui double de poids en s'hydratant voit toutes ses valeurs divisées par deux, sans
          qu'aucun coefficient n'ait à le dire. Ajouter un « facteur d'hydratation » ailleurs
          compterait l'eau <strong>deux fois</strong>.
        </p>
      </section>

      <section>
        <h3 class="font-semibold mb-1">Le facteur de rendement</h3>
        <p>
          C'est le dénominateur, et il est <strong>obligatoire</strong> : kg de tempeh pour 1 kg de
          graines brutes. Un seul nombre, qui contient tout — le dépelliculage et les pertes, le
          gonflement au trempage et à la cuisson, la déshydratation pendant la fermentation.
        </p>
        <p class="mt-1">
          ⚠️ <strong>La fiche ne dépend d'aucun poids de récolte.</strong> Une fournée qui pèse
          autrement ne change pas ce qu'on imprime : le facteur est une consigne d'atelier qu'on
          règle soi-même, et les tolérances d'étiquetage absorbent l'écart d'un lot à l'autre.
        </p>
      </section>

      <section>
        <h3 class="font-semibold mb-1">Cinq transformations, et rien d'autre</h3>
        <p class="mb-1">Chacune raisonne pour 100 g d'intrant tel qu'il a été pesé, avant toute transformation.</p>
        <ul class="list-disc ml-5">
          <li><strong>Substrat</strong> : dépelliculage → trempage → cuisson → fermentation</li>
          <li><strong>Support d'inoculation</strong> : torréfaction (si on la fait soi-même) → fermentation</li>
          <li><strong>Acidifiant pré-inoculation</strong> : rien — ajouté après cuisson, compté au prorata</li>
          <li><strong>Starter</strong> : exclu — quelques grammes pour des kilos de produit</li>
        </ul>
        <p class="mt-1">
          Aucune transformation ne touche à l'eau : une torréfaction chasse de l'eau, ça ne change
          donc <em>rien</em> aux masses de nutriments.
        </p>
      </section>

      <section>
        <h3 class="font-semibold mb-1">L'énergie se calcule, toujours</h3>
        <p>
          Depuis les macronutriments, avec les coefficients de l'<strong>annexe XIV</strong>. Elle
          ne se recopie jamais d'une table. Et les <strong>kcal ne sont pas les kJ ÷ 4,184</strong> :
          l'annexe donne deux jeux de coefficients indépendants, et convertir ferait diverger les
          deux chiffres de l'étiquette.
        </p>
      </section>

      <section>
        <h3 class="font-semibold mb-1">Une valeur absente n'est jamais un zéro</h3>
        <p>
          « On ne sait pas » et « il n'y en a pas » sont deux affirmations différentes, et la
          seconde engage. Un intrant sans composition, un réglage absent : la valeur du produit est
          <strong>inconnue</strong> (un tiret), jamais une somme partielle. C'est ce que dit
          « ce qui manque ».
        </p>
      </section>

      <section>
        <h3 class="font-semibold mb-1">Arrondis — tableau 4 du guide de décembre 2012</h3>
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
        <p class="mt-1">
          ⚠️ L'arrondi n'a lieu qu'<strong>une fois</strong>, à l'impression. Arrondir en chemin
          déplacerait le chiffre d'une unité.
        </p>
      </section>

      <section>
        <h3 class="font-semibold mb-1">Tolérances — non, ce n'est pas « ±20 % » partout</h3>
        <table class="table table-xs">
          <tbody>
            <tr><td>Glucides, sucres, protéines, fibres</td><td>&lt; 10 g : ± 2 g · 10–40 g : ± 20 % · &gt; 40 g : ± 8 g</td></tr>
            <tr><td>Matières grasses</td><td>&lt; 10 g : ± 1,5 g · 10–40 g : ± 20 % · &gt; 40 g : ± 8 g</td></tr>
            <tr><td>Acides gras saturés</td><td>&lt; 4 g : ± 0,8 g · ≥ 4 g : ± 20 %</td></tr>
            <tr><td>Sel</td><td>&lt; 1,25 g : ± 0,375 g · ≥ 1,25 g : ± 20 %</td></tr>
          </tbody>
        </table>
        <p class="mt-1">Incertitude de mesure comprise. Sous les seuils, la marge est ABSOLUE, et souvent bien plus large que 20 %.</p>
      </section>

      <section>
        <h3 class="font-semibold mb-1">Ce que ce calcul ne sait pas faire</h3>
        <p>
          ⚠️ <strong>Aucun coefficient n'est validé par une analyse de laboratoire.</strong>
          Plusieurs restent des hypothèses, marquées comme telles dans le code. Les coefficients
          sont calés sur la littérature quand elle existe, sur des couples graine → tempeh publiés
          sinon, et à défaut sur une hypothèse assumée.
        </p>
        <p class="mt-1">
          La <strong>vitamine B12</strong> n'est pas déclarée : aucun calcul ne peut l'établir.
        </p>
      </section>

      <section>
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
          Le détail — la méthode, le droit, chaque coefficient et sa source — est dans le dépôt :
          <code>refs/methode.md</code>, <code>refs/references.md</code> et
          <code>refs/transformations.md</code>. <strong>C'est ce document-là qu'on présente à un
          contrôle</strong>, pas cette page.
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
