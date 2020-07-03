<template>
  <section class="section">
    <DrawingBoard v-if="$store.state.image" :shapes="shapes" :image="$store.state.image" />
    <Sidebar>
      <SidebarBlock title="Edit">
        <b-button type="is-success" @click="save">Save</b-button>
      </SidebarBlock>
      <SidebarBlock title="Select">
        <b-radio v-model="linkComponent" size="is-small" name="name" native-value="source">Source</b-radio>
        <b-radio v-model="linkComponent" size="is-small" name="name" native-value="target">Target</b-radio>
        <br />
        <b-radio v-model="labelType" size="is-small" name="name2" :native-value="LabelType.POS">Pos</b-radio>
        <b-radio v-model="labelType" size="is-small" name="name2" :native-value="LabelType.NEG">Neg</b-radio>
      </SidebarBlock>

      <Selector
        title="search"
        :candidates="$store.state.tagger.candidates"
        @selected="setLinkComponent($event)"
      />

      <div class="p-1">
        <p class="menu-label">create link</p>
        <p class="tag is-info">source</p>
        <Label
          v-if="$store.state.linker.selectedSource"
          :candidate="$store.state.linker.selectedSource"
        />
        <p class="tag is-info">target</p>
        <Label
          v-if="$store.state.linker.selectedTarget"
          :candidate="$store.state.linker.selectedTarget"
        />
        <b-button size="is-small is-uppercase" type="is-primary" @click="addLink">create</b-button>
      </div>
      <div class="p-1">
        <p class="menu-label">Links</p>
        <CandidateLink
          :source="link.source"
          :target="link.target"
          v-for="(link, index) in links"
          delete-control="true"
          @delete="$store.commit('linker/removeLink', link.orig)"
          :key="index"
        />
      </div>
    </Sidebar>
  </section>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import Selector from "../components/Selector.vue";
import DrawingBoard from "../components/DrawingBoard.vue";
import CandidateLink from "../components/CandidateLink.vue";
import Label from "../components/Label.vue";
import Sidebar from "../components/layout/Sidebar.vue";
import SidebarBlock from "../components/layout/SidebarBlock.vue";
import { extractBoxSize } from "../common";

import {
  CandidateInfo,
  LabelType,
  Drawable,
  Rect,
  Arrow,
  LinkLabelInfo
} from "../models";

import Buefy from "buefy";
import "buefy/dist/buefy.css";
import { RootState } from "../store/types";

@Component({
  components: {
    Selector,
    DrawingBoard,
    Label,
    CandidateLink,
    Sidebar,
    SidebarBlock
  }
})
export default class LinkingTool extends Vue {
  linkComponent: "source" | "target" = "source";

  // To access enum through template
  LabelType = LabelType;

  get links() {
    const links = this.$store.state.linker.links;

    return links
      .filter((item: LinkLabelInfo) => item.value == this.labelType)
      .map((item: LinkLabelInfo) => ({
        source: this.candidatesById[item.source],
        target: this.candidatesById[item.target],
        orig: item
      }));
  }

  get candidatesById() {
    const candidatesById: { [key: string]: CandidateInfo } = {};

    this.$store.state.tagger.candidates.forEach((item: CandidateInfo) => {
      candidatesById[item.path] = item;
    });
    return candidatesById;
  }

  get shapes() {
    const shapes: Drawable[] = [];
    const selectedSource = this.$store.state.linker.selectedSource;
    const selectedTarget = this.$store.state.linker.selectedTarget;

    const candidates = this.$store.state.tagger.candidates;
    const candidatesDrawn = new Set();
    // We draw all candidates first;
    this.links.forEach(link => {
      candidatesDrawn.add(link.source.path);
      candidatesDrawn.add(link.target.path);

      shapes.push(
        new Rect({
          ...extractBoxSize(link.source),
          fill: "",
          lineWidth: 4,
          stroke: "#00FF00"
        })
      );

      shapes.push(
        new Rect({
          ...extractBoxSize(link.target),
          fill: "",
          lineWidth: 4,
          stroke: "#FF0000"
        })
      );
    });

    if (selectedSource) {
      const cand = selectedSource as CandidateInfo;
      candidatesDrawn.add(cand.path);
      shapes.push(
        new Rect({
          ...extractBoxSize(cand),
          fill: "#00FF0080"
        })
      );
    }

    if (selectedTarget) {
      const cand = selectedTarget as CandidateInfo;
      candidatesDrawn.add(cand.path);
      shapes.push(
        new Rect({
          ...extractBoxSize(selectedTarget),
          fill: "#FF000080"
        })
      );
    }

    if (selectedTarget && selectedSource) {
      const candFrom = selectedSource as CandidateInfo;
      const candTo = selectedTarget as CandidateInfo;

      shapes.push(
        new Arrow({
          from: { x: candFrom.rect.left, y: candFrom.rect.top },
          to: { x: candTo.rect.left, y: candTo.rect.top },
          color: "#0000FF",
          lineWidth: 3,
          r: 3
        })
      );
    }

    // Draw the rest of the candidates

    candidates.forEach(cand => {
      if (!candidatesDrawn.has(cand.path)) {
        shapes.push(new Rect({ ...extractBoxSize(cand), stroke: "#000000" }));
      }
    });

    return shapes;
  }

  get labelType() {
    return this.$store.state.linker.labelType;
  }

  set labelType(arg: LabelType) {
    this.$store.commit("linker/setLabelType", arg);
  }

  setLinkComponent(arg: CandidateInfo) {
    if (this.linkComponent == "source") {
      this.$store.commit("linker/setSource", arg);
    } else {
      this.$store.commit("linker/setTarget", arg);
    }
  }

  addLink() {
    this.$store.dispatch("linker/createLink");
  }

  save() {
    this.$store.dispatch("linker/save");
  }
}
</script>
