<template>
  <section class="section">
    <router-link to="/tool/linking">Linking</router-link>
    <router-link to="/tool/tagging">Tagging</router-link>
    <router-link to="/tool/suggestLink">Suggest Link></router-link>
    <router-view></router-view>
  </section>
</template>

<script lang="ts">
import TaggingTool from "./tools/TaggingTool.vue";
import LinkingTool from "./tools/LinkingTool.vue";
import SuggestLinkTool from "./tools/SuggestLinkTool.vue";
import store from "./store/Main";
import { Vue, Component } from "vue-property-decorator";
import VueRouter from "vue-router";
import registerFilters from "./filters";

import Buefy from "buefy";
import "buefy/dist/buefy.css";

Vue.use(Buefy);
Vue.use(VueRouter);
registerFilters(Vue);

const routes = [
  { path: "*", redirect: "/tool/linking" },
  { path: "/tool/linking", component: LinkingTool },
  { path: "/tool/tagging", component: TaggingTool },
  { path: "/tool/suggestLink", component: SuggestLinkTool }
];

const router = new VueRouter({
  routes // short for `routes: routes`
});

@Component({
  components: {
    TaggingTool,
    LinkingTool
  },
  router,
  store
})
export default class App extends Vue {
  created() {
    this.$store.dispatch("loadApp");
  }
}
</script>

<style lang="scss">
@import "~bulma/sass/utilities/_all";

@import "~bulma";
@import "~buefy/src/scss/buefy";
</style>
