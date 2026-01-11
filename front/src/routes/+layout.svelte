<script>
  import "../app.css";
  import TopNav from "$lib/components/TopNav.svelte";
  import SiteFooter from "$lib/components/SiteFooter.svelte";
</script>

<main>
  <TopNav />
  <div class="page">
    <slot />
  </div>
  <SiteFooter />
</main>