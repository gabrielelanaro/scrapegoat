/** The main store */

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


export class Store {
    candidates: CandidateInfo[];
    image: HTMLImageElement;
    labelName: string;
    labelValue: LabelType;
    selected: { [key: string]: boolean } = {};
    labels: LabelInfo[] = [];
    availableLabels: string[] = [];

    constructor(candidates: CandidateInfo[], image: HTMLImageElement, labels: LabelInfo[]) {
        this.candidates = candidates;
        this.image = image;
        this.labels = labels;
        this.availableLabels = [...new Set(labels.map(item => item.label_name))]
        this.labelName = this.availableLabels ? this.availableLabels[0] : "label";

        this.labelValue = LabelType.POS;
        this.recalculateSelected();
    }

    switchLabelName(name: string) {
        this.labelName = name;
        this.recalculateSelected();
    }

    switchLabelValue(value: LabelType) {
        this.labelValue = value;
        this.recalculateSelected();
    }


    toggleLabel(label: LabelInfo) {
        if (this.hasLabel(label))
            this.removeLabel(label);
        else
            this.addLabel(label);
        this.recalculateSelected();

    }

    addLabel(label: LabelInfo) {
        this.labels.push(label);
    }

    removeLabel(label: LabelInfo) {
        this.labels = this.labels.filter((item) => !(item.label_name == label.label_name && item.value == label.value && label.ref == item.ref))
    }

    hasLabel(label: LabelInfo) {
        return this.labels.filter((item) => (item.label_name == label.label_name && item.value == label.value && label.ref == item.ref)).length > 0;
    }

    recalculateSelected() {
        const labelMap: { [key: string]: LabelInfo } = {}

        this.labels.forEach(item => {
            if (item.label_name == this.labelName)
                labelMap[item.ref] = item;
        })
        const selected: { [key: string]: boolean } = {}
        this.candidates.forEach((item) => {
            const lbl = labelMap[item.url + item.path];
            if (lbl != undefined)
                selected[item.path] = lbl.value == this.labelValue;
            else
                selected[item.path] = false
        });
        this.selected = selected;
    }

    public static async load() {
        const image = Store.fetchImage()
        const candidates = await Store.fetchCandidates();
        const labels = await Store.fetchLabels();
        return new Store(candidates, image, labels)
    }

    static fetchImage() {
        const image = new window.Image();
        image.src = "/fs/screenshot.png";
        return image;
    }
    static async fetchCandidates() {
        const resp = await fetch("/fs/candidates.json")
        const data = await resp.json() as CandidateInfo[];
        return data;
    }

    static async fetchLabels() {
        const resp = await fetch("/fs/labels.json")
        let data: LabelInfo[] = [];
        if (resp.status == 200) {
            data = await resp.json();
        } else if (resp.status == 404) {
            data = [];
        }
        return data;
    }

    async save() {
        const resp = await fetch("/fs/labels.json", {
            method: "PUT",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(this.labels)
        });

        if (resp.status !== 200) {
            console.log("error saving");
        }
    }

}