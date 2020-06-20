<template>
  <DrawingBoard :image="img" :shapes="shapes" @click="$emit('select', candidateById[$event.key])" />
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
import { CandidateInfo, Drawable, Rect } from "../models";
import DrawingBoard from "./DrawingBoard.vue";

@Component({
  components: { DrawingBoard }
})
export default class VisualSelector extends Vue {
  @Prop() img!: HTMLImageElement;
  @Prop() candidates!: CandidateInfo[];
  @Prop() selected!: { [key: string]: boolean };

  private shapes: Drawable[] = [];

  get candidateById() {
    // Performance optimization
    const map: { [key: string]: CandidateInfo } = {};

    this.candidates.forEach(item => {
      map[item.path] = item;
    });
    return map;
  }

  @Watch("candidates")
  onCandidatesUpdated() {
    this.recalculateShapes();
  }

  @Watch("selected")
  onSelectedChanged() {
    this.recalculateShapes();
  }

  recalculateShapes() {
    const boxes: Rect[] = [];

    const selectedStyle = {
      fill: "#FF000080"
    };
    const unselectedStyle = {
      stroke: "#000000"
    };

    this.candidates.forEach((item, index) => {
      const box = {
        key: index,
        x: item.rect.left,
        y: item.rect.top,
        width: item.rect.right - item.rect.left,
        height: item.rect.bottom - item.rect.top
      };
      if (box.x > 0 && box.y >= 0 && box.width > 0 && box.height > 0) {
        const style = this.selected[item.path]
          ? selectedStyle
          : unselectedStyle;
        boxes.push(
          new Rect({
            ...box,
            z: -box.width * box.height,
            key: item.path,
            ...style
          })
        );
      }
    });

    this.shapes = boxes;
  }
}
</script>

