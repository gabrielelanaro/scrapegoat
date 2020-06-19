<template>
  <article class="media">
    <div class="media-left">
      <div class="content is-small">
        <b-icon class="is-primary" icon="code-tags" size="is-small"></b-icon>
        <p class="has-text-centered has-text-weight-semibold">{{ candidate.tag.toLowerCase() }}</p>
      </div>
    </div>
    <div class="media-content">
      <div class="content is-small">{{ candidate.text }}</div>
    </div>
    <div class="media-right">
      <b-button
        v-if="deleteControl"
        icon-right="minus-circle-outline"
        expanded
        type="is-danger"
        size="is-small"
        outlined
        @click="$emit('delete', candidate)"
      ></b-button>
      <b-button
        v-if="selectControl"
        icon-right="plus"
        expanded
        outlined
        type="is-primary"
        size="is-small"
        @click="$emit('select', candidate)"
      ></b-button>
      <b-button
        v-if="gotoControl"
        icon-right="arrow-collapse-down"
        expanded
        outlined
        type="is-link"
        size="is-small"
        @click="$emit('goto', candidate)"
      ></b-button>
    </div>
  </article>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
import { CandidateInfo } from "../Store";

@Component
export default class Label extends Vue {
  @Prop() private candidate!: CandidateInfo;
  @Prop() private selectControl!: boolean;
  @Prop() private deleteControl!: boolean;
  @Prop() private gotoControl!: boolean;
}
</script>