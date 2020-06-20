<template>
  <div id="drawingContainer">
    <img id="myimg" :src="image.src" />
    <canvas id="mycanvas" v-on:mousedown="click"></canvas>
  </div>
</template>

<script lang="ts">
// Draw colored stuff on top of an image.
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
import { Drawer, RectData, Drawable } from "../models";
import { CanvasDrawer } from "../drawing";

@Component
export default class DrawingBoard extends Vue {
  @Prop() image!: HTMLImageElement;
  @Prop() shapes!: Drawable[];

  private drawer?: CanvasDrawer;

  mounted() {
    const canvas = document.getElementById("mycanvas") as HTMLCanvasElement;
    canvas.width = this.image.width;
    canvas.height = this.image.height;
    const ctx = canvas.getContext("2d");

    /// Draw all rectangles in bulk
    if (ctx) {
      this.drawer = new CanvasDrawer(ctx);
    } else {
      console.log("Canvas context not available?");
    }
  }

  @Watch("shapes")
  onShapeChanged() {
    console.log("Shapes have changed");
    if (this.drawer) this.redrawShapes(this.drawer);
  }

  redrawShapes(drawer: Drawer) {
    drawer.clear();
    this.shapes.forEach(shape => shape.draw(drawer));
  }

  click(event: MouseEvent) {
    if (!this.drawer) {
      return;
    }
    // I need to do a hit test and see which boxes are hit. Then we select the last
    const target = event.target as Element;

    const x = event.x - target.getBoundingClientRect().left;
    const y = event.y - target.getBoundingClientRect().top;

    const hitBoxes = this.drawer.hitbox.hitTest({ x, y });
    console.log(hitBoxes);
    if (hitBoxes.length > 0) this.$emit("click", hitBoxes[hitBoxes.length - 1]);
  }
}
</script>
<style scoped>
#drawingContainer {
  min-width: 800px;
  min-height: 1000px;
}

#myimg {
  position: absolute;
  z-index: 1;
}

#mycanvas {
  position: absolute;
  z-index: 20;
}
</style>
