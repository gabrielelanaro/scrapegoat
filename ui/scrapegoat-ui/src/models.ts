export enum LabelType {
    POS = 't',
    NEG = 'f'
}

export interface LabelInfo {
    ref: string;
    label_name: string;
    value: LabelType;
    remarks: string[];
}

export interface LinkLabelInfo {
    source: string;
    target: string;
    link_name: string;
    value: LabelType;
    remarks: string[];
}

export interface CandidateInfo {
    rect: { top: number; bottom: number; left: number; right: number };
    style: {
        background: { color: string };
    };
    border: string;
    color: string;
    font: { family: string; size: string; style: string; variant: string; weight: string };
    tag: string;
    text: string;
    url: string;
    path: string;
}

export interface RectData {
    key: string;
    x: number;
    y: number;
    z: number;
    width: number;
    height: number;
    stroke?: string;
    fill?: string;
}


export interface Drawable {
    draw: (drawer: Drawer) => void;
}

function autoImplement<T>(defaults?: Partial<T>) {
    // Utility function to initialize an object from an interface
    return class {
        constructor(data: T) {
            Object.assign(this, { ...defaults, ...data });
        }
    } as new (data: T) => T
}


export class Rect extends autoImplement<RectData>() implements Drawable {
    draw(drawer: Drawer) {
        drawer.drawRect(this);
    }
}

export interface Drawer {
    clear: () => void;
    drawRect: (rect: RectData) => void;
}
