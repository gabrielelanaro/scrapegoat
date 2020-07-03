import { Drawer, RectData, ArrowData } from "./models";

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

    drawArrow(arrow: ArrowData) {
        1
        return;
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
        this.ctx.fillStyle = "";
        this.ctx.strokeStyle = "";
    }

    drawRect(rect: RectData) {
        this.hitbox.drawRect(rect);

        // Draw a single rectangle to the canvas
        if (rect.stroke) {
            this.ctx.lineWidth = rect.lineWidth;
            this.ctx.strokeStyle = rect.stroke;
            this.ctx.strokeRect(rect.x, rect.y, rect.width, rect.height);
        }

        if (rect.fill) {
            this.ctx.fillStyle = rect.fill;
            this.ctx.fillRect(rect.x, rect.y, rect.width, rect.height);
        }
    }

    drawArrow(arrow: ArrowData) {
        this.ctx.lineWidth = arrow.lineWidth;
        this.ctx.strokeStyle = arrow.color;
        this.ctx.fillStyle = arrow.color; // for the triangle fill
        this.ctx.lineJoin = 'miter';

        const toX = arrow.to.x;
        const toY = arrow.to.y;

        const fromX = arrow.from.x;
        const fromY = arrow.from.y;

        const r = arrow.r;

        let angle;
        let x;
        let y;
        this.ctx.beginPath();
        this.ctx.moveTo(fromX, fromY);
        this.ctx.lineTo(toX, toY);


        angle = Math.atan2(toY - fromY, toX - fromX)
        x = r * Math.cos(angle) + toX;
        y = r * Math.sin(angle) + toY;

        this.ctx.moveTo(x, y);

        angle += (1 / 3) * (2 * Math.PI)
        x = r * Math.cos(angle) + toX;
        y = r * Math.sin(angle) + toY;

        this.ctx.lineTo(x, y);

        angle += (1 / 3) * (2 * Math.PI)
        x = r * Math.cos(angle) + toX;
        y = r * Math.sin(angle) + toY;

        this.ctx.lineTo(x, y);

        this.ctx.closePath();

        this.ctx.fill();
        this.ctx.stroke();
    }
}


