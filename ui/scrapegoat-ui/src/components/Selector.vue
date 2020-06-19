<template>
  <div class="p-1">
    <p class="menu-label">search</p>
    <b-input size="is-small" v-model="query" placeholder="Search by text" type="search"></b-input>
    <div v-for="match in matches" v-bind:key="match.path">
      <Label :candidate="match" :select-control="true" @select="$emit('selected', match)" />
      <!-- 
      <input
        type="checkbox"
        id="match"
        name="scales"
        v-on:change="$emit('selected', match)"
        :checked="selected[match.path]"
      />
      <label for="match">{{ match.text.slice(0, 500) }}</label>-->
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
import { CandidateInfo } from "../Store";
import Label from "./Label.vue";

@Component({ components: { Label } })
export default class Selector extends Vue {
  @Prop() private candidates!: CandidateInfo[];
  @Prop() private selected!: { [key: string]: boolean };
  private query = "";

  get matches() {
    let cand = this.candidates
      .map(item => {
        let intersection;
        if (item.text.toLowerCase().includes(this.query.toLowerCase()))
          intersection = this.query.length;
        else intersection = 0;
        const union = item.text.length;

        return { score: intersection / union, item };
      })
      .filter(item => item.score > 0.0)
      .sort((a, b) => b.score - a.score)
      .map(item => item.item);

    if (cand.length > 0) {
      cand = cand.slice(0, 1);
    }
    return cand;
  }

  truncate(str: string, n: number) {
    return str.length > n ? str.substr(0, n - 1) + "&hellip;" : str;
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
