<template>
  <article class="media">
    <div class="media-content">
      <div>
        <span class="tag is-success">S</span>
        {{ source.text }}
      </div>
      <div>
        <span class="tag is-danger">T</span>
        {{ target.text }}
      </div>
    </div>
    <div class="media-right">
      <b-button
        v-if="deleteControl"
        expanded
        icon-right="minus-circle-outline"
        type="is-danger"
        size="is-small"
        outlined
        @click="$emit('delete', {source, target})"
      ></b-button>
      <b-button
        v-if="selectControl"
        expanded
        icon-right="plus"
        outlined
        type="is-primary"
        size="is-small"
        @click="$emit('select', {source, target})"
      ></b-button>
      <b-button
        v-if="gotoControl"
        expanded
        icon-right="arrow-collapse-down"
        outlined
        type="is-link"
        size="is-small"
        @click="$emit('goto', {source, target})"
      ></b-button>
    </div>
  </article>
</template>

<script lang="ts">
// Representation of a vue
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
import { CandidateInfo } from "../models";

@Component
export default class CandidateLink extends Vue {
  @Prop() private source!: CandidateInfo;
  @Prop() private target!: CandidateInfo;
  @Prop() private selectControl!: boolean;
  @Prop() private deleteControl!: boolean;
  @Prop() private gotoControl!: boolean;
}
</script>

<style>
</style>