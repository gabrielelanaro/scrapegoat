import { Drawer, RectData } from "./models";

interface Box {
    key: string;
    x: number;
    y: number;
    width: number;
    height: number;
    z: number;
}



function boxHitTest(box: Box, coord: { x: number; y: number }) {
    const withinX = coord.x >= box.x && coord.x <= box.x + box.width;
    const withinY = coord.y >= box.y && coord.y <= box.y + box.height;

    return withinX && withinY;
}

export class HitBoxDrawer implements Drawer {
    boxes: Box[] = [];

    clear() {
        this.boxes = [];
    }

    drawRect(rect: RectData) {
        this.boxes.push(rect);
    }

    hitTest(coord: { x: number; y: number }) {
        console.log(this.boxes.length);

        const hitBoxes = this.boxes.filter(item =>
            boxHitTest(item, coord)
        );

        return hitBoxes.sort((a, b) => a.z - b.z);
    }
}


export class CanvasDrawer implements Drawer {
    public hitbox = new HitBoxDrawer();
    private ctx: CanvasRenderingContext2D;

    constructor(ctx: CanvasRenderingContext2D) {
        this.ctx = ctx;
    }

    clear() {
        this.hitbox.clear();
        this.ctx.clearRect(0, 0, this.ctx.canvas.width, this.ctx.canvas.height);
    }

    drawRect(rect: RectData) {
        this.hitbox.drawRect(rect);

        // Draw a single rectangle to the canvas
        if (rect.stroke) this.ctx.strokeStyle = rect.stroke;
        this.ctx.strokeRect(rect.x, rect.y, rect.width, rect.height);

        if (rect.fill) {
            this.ctx.fillStyle = rect.fill;
            this.ctx.fillRect(rect.x, rect.y, rect.width, rect.height);
        }
    }
}


