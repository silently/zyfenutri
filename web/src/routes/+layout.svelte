<script lang="ts">
  import '../app.css';
  import logo from '../assets/zyfe.png';

  let { children } = $props();
</script>

<svelte:head>
  <link rel="icon" href={logo} />
</svelte:head>

{@render children()}
