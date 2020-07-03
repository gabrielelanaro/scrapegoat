<template>
  <section class="section">
    <DrawingBoard v-if="$store.state.image" :shapes="shapes" :image="$store.state.image" />
    <Sidebar>
      <SidebarBlock title="Tools">
        <b-button @click="suggest">Suggest</b-button>
      </SidebarBlock>
      <SidebarBlock title="Links">
        <CandidateLink
          :source="link.source"
          :target="link.target"
          v-for="(link, index) in links"
          :key="index"
          select-control="true"
          delete-control="true"
          goto-control="true"
          @select="addLink($event)"
          @delete="deleteLink($event)"
          @goto="selectLink($event)"
        />
      </SidebarBlock>
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
export default class SuggestLinkTool extends Vue {
  linkComponent: "source" | "target" = "source";

  get links() {
    const links = this.$store.state.suggestLink.predictedLinks;
    // TODO: extract positive links
    return links.map((item: LinkLabelInfo) => ({
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

  suggest() {
    console.log(this.$store.state.linker.links);
    console.log(this.$store.state.tagger.candidates);
    this.$store.dispatch("suggestLink/predictLinks", {
      candidates: this.$store.state.tagger.candidates,
      links: this.$store.state.linker.links
    });
  }

  setLinkComponent(arg: CandidateInfo) {
    if (this.linkComponent == "source") {
      this.$store.commit("linker/setSource", arg);
    } else {
      this.$store.commit("linker/setTarget", arg);
    }
  }

  selectLink(link: { source: CandidateInfo; target: CandidateInfo }) {
    this.$store.commit("linker/setSource", link.source);
    this.$store.commit("linker/setTarget", link.target);
  }

  deleteLink(link: { source: CandidateInfo; target: CandidateInfo }) {
    this.$store.commit("linker/setLabelType", LabelType.NEG);
    this.$store.dispatch("linker/createLink");
  }

  addLink() {
    this.$store.commit("linker/setLabelType", LabelType.POS);
    this.$store.dispatch("linker/createLink");
  }

  save() {
    this.$store.dispatch("linker/save");
  }
}
</script>
