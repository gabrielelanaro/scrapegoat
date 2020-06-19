<template>
  <section class="section">
    <!-- <img alt="Vue logo" src="./assets/logo.png" /> -->
    <DrawingArea
      v-if="store"
      :candidates="store.candidates"
      :img="store.image"
      :selected="store.selected"
      :onselect="onselect"
    />
    <div id="sidebar-page">
      <section class="sidebar-layout">
        <b-sidebar position="fixed" open right fullheight>
          <Controls
            v-if="store"
            :selectedLabel="store.labelName"
            :value="store.labelValue"
            :labels="store.availableLabels"
            v-on:save="store.save().then()"
            v-on:change-label="store.switchLabelName($event)"
            v-on:change-value="store.switchLabelValue($event)"
          />
          <Selector
            v-if="store"
            :candidates="store.candidates"
            :selected="store.selected"
            @selected="onselect"
          />
          <LabelViewer
            v-if="store"
            :candidates="store.candidates"
            :selected="store.selected"
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
import { Store, CandidateInfo, LabelType } from "./Store";
import Buefy from "buefy";
import "buefy/dist/buefy.css";

Vue.use(Buefy);

@Component({
  components: {
    Controls,
    DrawingArea,
    LabelViewer,
    Selector
  }
})
export default class App extends Vue {
  store: null | Store = null;
  created() {
    Store.load().then(store => (this.store = store));
  }

  onselect(arg: CandidateInfo) {
    if (this.store) {
      /* eslint-disable */

      const lbl = {
        ref: arg.url + arg.path,
        label_name: this.store.labelName,
        value: this.store.labelValue,
        remarks: ["manual"]
      };
      this.store.toggleLabel(lbl);
      this.store.recalculateSelected();
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
