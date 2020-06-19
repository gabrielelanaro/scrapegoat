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

