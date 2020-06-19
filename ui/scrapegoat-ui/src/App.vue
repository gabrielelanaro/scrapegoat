<template>
  <section class="section">
    <!-- <img alt="Vue logo" src="./assets/logo.png" /> -->
    <DrawingArea
      v-if="$store.state.image"
      :candidates="$store.state.tagger.candidates"
      :img="$store.state.image"
      :selected="$store.state.tagger.selected"
      :onselect="onselect"
    />
    <div id="sidebar-page">
      <section class="sidebar-layout">
        <b-sidebar position="fixed" open right fullheight>
          <Controls
            v-if="$store.state.tagger.candidates"
            :selectedLabel="$store.state.tagger.labelName"
            :value="$store.state.tagger.labelValue"
            :labels="$store.state.tagger.availableLabels"
            v-on:save="$store.dispatch('tagger/save')"
            v-on:change-label="$store.commit('tagger/switchLabelName', $event)"
            v-on:change-value="$store.commit('tagger/switchLabelValue', $event)"
          />
          <Selector
            v-if="$store.state.tagger.labels"
            :candidates="$store.state.tagger.candidates"
            :selected="$store.state.tagger.selected"
            @selected="onselect"
          />
          <LabelViewer
            v-if="$store.state.tagger.labels"
            :candidates="$store.state.tagger.candidates"
            :selected="$store.state.tagger.selected"
            @select="onselect"
          />
        </b-sidebar>
      </section>
    </div>
  </section>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import DrawingArea from "./components/DrawingArea.vue";
import Controls from "./components/Controls.vue";
import LabelViewer from "./components/LabelViewer.vue";
import Selector from "./components/Selector.vue";
// import { Store, CandidateInfo, LabelType } from "./Store";
import { CandidateInfo, LabelType } from "./models";
import store from "./store/Main";

import Buefy from "buefy";
import "buefy/dist/buefy.css";

Vue.use(Buefy);

@Component({
  components: {
    Controls,
    DrawingArea,
    LabelViewer,
    Selector
  },
  store
})
export default class App extends Vue {
  created() {
    this.$store.dispatch("loadApp");
  }

  onselect(arg: CandidateInfo) {
    if (this.$store.state.tagger.labels) {
      /* eslint-disable */

      const lbl = {
        ref: arg.url + arg.path,
        label_name: this.$store.state.tagger.labelName,
        value: this.$store.state.tagger.labelValue,
        remarks: ["manual"]
      };
      this.$store.commit("tagger/toggleLabel", lbl);
    }
  }
}
</script>

<style lang="scss">
@import "~bulma/sass/utilities/_all";

// $box-padding: 0.5;

// #app {
//   font-family: Avenir, Helvetica, Arial, sans-serif;
//   -webkit-font-smoothing: antialiased;
//   -moz-osx-font-smoothing: grayscale;
//   display: flex;
//   color: #2c3e50;
//   margin-top: 60px;
//   margin-left: 0px;
// }

@import "~bulma";
@import "~buefy/src/scss/buefy";
</style>
