<template>
  <div class="p-1">
    <p class="menu-label">File</p>
    <b-button
      class="button is-success"
      size="is-small"
      icon-right="save"
      @click="$emit('save')"
    >Save</b-button>
    <p class="menu-label">labels</p>
    <b-field>
      <b-input size="is-small" v-model="labelInput" placeholder="New label" type="search"></b-input>
      <p class="control">
        <b-button
          size="is-small"
          class="button is-primary"
          icon-right="plus"
          @click="addLabel(labelInput)"
        ></b-button>
      </p>
    </b-field>
    <b-field>
      <b-radio
        size="is-small"
        name="labelValue"
        v-model="internalLabelValue"
        :native-value="LabelType.POS"
      >Positive</b-radio>
      <b-radio
        size="is-small"
        name="labelValue"
        v-model="internalLabelValue"
        :native-value="LabelType.NEG"
      >Negative</b-radio>
    </b-field>
    <div class="field is-grouped is-grouped-multiline">
      <div class="control" v-for="label in labels" v-bind:key="label">
        <div class="tags has-addons">
          <a
            :class="label == selectedLabel ? 'tag is-primary' : 'tag'"
            @click="select(label)"
          >{{label}}</a>
          <a
            :class="label == selectedLabel ? 'tag is-delete is-primary' : 'tag is-delete'"
            @click="removeLabel(label)"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
import { LabelType } from "../models";

@Component
export default class Controls extends Vue {
  @Prop() private value!: LabelType;
  @Prop() private selectedLabel!: string;
  @Prop() private labels!: string[];
  private LabelType = LabelType;
  private labelInput = "";
  private internalLabelValue = this.value;

  addLabel(labelName: string) {
    if (labelName !== "") this.labels.push(labelName);
    this.labelInput = "";
  }

  select(labelName: string) {
    this.$emit("change-label", labelName);
  }

  @Watch("internalLabelValue")
  onLabelValueChange() {
    this.$emit("change-value", this.internalLabelValue);
  }

  removeLabel(labelName: string) {
    this.labels = this.labels.filter(item => item != labelName);
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
