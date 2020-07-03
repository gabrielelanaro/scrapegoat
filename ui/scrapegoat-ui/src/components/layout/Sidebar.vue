<template>
  <div id="sidebar-page">
    <section class="sidebar-layout">
      <b-sidebar position="fixed" open :can-cancel="false" right fullheight>
        <slot />
      </b-sidebar>
    </section>
  </div>
</template>

<script lang="ts">
export default {};
</script>

<style>
</style>