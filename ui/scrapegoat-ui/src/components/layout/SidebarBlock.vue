<template>
  <div class="block py-1">
    <p class="menu-label">{{ title }}</p>
    <slot />
  </div>
</template>

<script lang="ts">
import Vue from "vue";
export default Vue.extend({
  props: ["title"]
});
</script>

<style>
</style>