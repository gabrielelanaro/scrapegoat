<template>
  <div class="pl-1">
    <p class="menu-label">Labels</p>
    <Label
      v-for="candidate in selectedCandidates"
      :key="candidate.path"
      :candidate="candidate"
      delete-control="true"
      goto-control="true"
      @select="$emit('select', candidate)"
    />
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";
import { CandidateInfo } from "../models";
import Label from "./Label.vue";

@Component({ components: { Label } })
export default class LabelViewer extends Vue {
  @Prop() private candidates!: CandidateInfo[];
  @Prop() private selected!: { [key: string]: boolean };

  get selectedCandidates() {
    return this.candidates.filter(item => this.selected[item.path]);
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#labelbox {
  max-height: 300px;
  overflow-y: auto;
}
</style>
