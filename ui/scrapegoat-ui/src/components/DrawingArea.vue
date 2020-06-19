<template>
  <div id="drawingContainer">
    <img id="myimg" :src="img.src" />
    <canvas id="mycanvas" v-on:mousedown="click"></canvas>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
import { CandidateInfo } from "../Store";

interface Rect {
  index: number;
  x: number;
  y: number;
  width: number;
  height: number;
  stroke?: string;
  fill?: string;
}

function rectHit(rect: Rect, coord: { x: number; y: number }) {
  const withinX = coord.x >= rect.x && coord.x <= rect.x + rect.width;
  const withinY = coord.y >= rect.y && coord.y <= rect.y + rect.height;

  return withinX && withinY;
}

@Component
export default class DrawingArea extends Vue {
  @Prop() img!: HTMLImageElement;
  @Prop() candidates!: CandidateInfo[];
  @Prop() selected!: { [key: string]: boolean };
  @Prop() onselect!: (arg: CandidateInfo) => null;

  private canvasCtx: CanvasRenderingContext2D | null = null;
  private boxes: Rect[];
  private boxToCandidate: Map<number, CandidateInfo>;

  constructor() {
    super();
    const boxes: Rect[] = [];
    const boxToCandidate = new Map();

    this.candidates.forEach((item, index) => {
      const box = {
        index: index,
        x: item.rect.left,
        y: item.rect.top,
        width: item.rect.right - item.rect.left,
        height: item.rect.bottom - item.rect.top
      };

      if (box.x > 0 && box.y >= 0) {
        boxToCandidate.set(index, item);
        boxes.push(box);
      }
    });

    this.boxes = boxes;
    this.boxToCandidate = boxToCandidate;
  }

  computeBoxStyle(item: Rect) {
    const candidate = this.boxToCandidate.get(item.index);

    let isSelected = false;
    if (candidate) {
      isSelected = this.selected[candidate.path] || false;
    }

    const selectedStyle = {
      ...item,
      fill: "#FF000080",
      opacity: 0.5
    };
    const unselectedStyle = {
      ...item,
      stroke: "#000000"
    };

    return isSelected ? selectedStyle : unselectedStyle;
  }

  mounted() {
    const canvas = document.getElementById("mycanvas") as HTMLCanvasElement;
    canvas.width = this.img.width;
    canvas.height = this.img.height;
    const ctx = canvas.getContext("2d");
    this.canvasCtx = ctx;

    const styledBoxes = this.boxes.map(item => {
      return this.computeBoxStyle(item);
    });

    /// Draw all rectangles in bulk
    if (ctx) this.drawRects(ctx, styledBoxes);
  }

  drawRects(ctx: CanvasRenderingContext2D, rects: Rect[]) {
    ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);

    rects.forEach(item => {
      if (item.stroke) ctx.strokeStyle = item.stroke;
      ctx.strokeRect(item.x, item.y, item.width, item.height);

      if (item.fill) {
        ctx.fillStyle = item.fill;
        ctx.fillRect(item.x, item.y, item.width, item.height);
      }
    });
  }

  @Watch("selected", { deep: true })
  onselected(value: { [key: string]: boolean }) {
    const styledBoxes = this.boxes.map(item => {
      return this.computeBoxStyle(item);
    });

    /// Draw all rectangles in bulk
    if (this.canvasCtx) this.drawRects(this.canvasCtx, styledBoxes);
  }

  click(event: MouseEvent) {
    // I need to do a hit test and see which boxes are hit. Then we select the last
    const target = event.target as Element;

    const posX = event.x - target.getBoundingClientRect().left;
    const posY = event.y - target.getBoundingClientRect().top;

    const hitBoxes = this.boxes.filter(item =>
      rectHit(item, { x: posX, y: posY })
    );

    const hitCandidates = hitBoxes
      .map(item => this.boxToCandidate.get(item.index))
      .filter(a => a != null) as CandidateInfo[];

    hitCandidates.sort((a: CandidateInfo, b: CandidateInfo) => {
      const areaA = (a.rect.top - a.rect.bottom) * (a.rect.right - a.rect.left);
      const areaB = (b.rect.top - b.rect.bottom) * (b.rect.right - b.rect.left);

      return areaA > areaB ? 1 : -1;
    });
    // hitCandidates.forEach(item => this.onselect(item));
    if (hitCandidates.length > 0)
      this.onselect(hitCandidates[hitCandidates.length - 1]);
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
