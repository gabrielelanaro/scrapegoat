import { LabelInfo, LabelType, CandidateInfo } from '@/models';
import Vuex, { Store, Module, ActionContext } from "vuex";
import { RootState } from './types';


interface TaggerState {
    labels: LabelInfo[];
    labelValue: LabelType;
    labelName: string;
    candidates: CandidateInfo[];
    selected: { [key: string]: boolean };
    availableLabels: string[];
}


function recalculateSelected(state: TaggerState) {
    const labelMap: { [key: string]: LabelInfo } = {}

    state.labels.forEach(item => {
        if (item.label_name == state.labelName)
            labelMap[item.ref] = item;
    })
    const selected: { [key: string]: boolean } = {}
    state.candidates.forEach((item) => {
        const lbl = labelMap[item.url + item.path];
        if (lbl != undefined)
            selected[item.path] = lbl.value == state.labelValue;
        else
            selected[item.path] = false
    });
    return selected;
}

function hasLabel(state: TaggerState, label: LabelInfo) {
    return state.labels.filter((item) => (item.label_name == label.label_name && item.value == label.value && label.ref == item.ref)).length > 0;
}

function addLabel(state: TaggerState, label: LabelInfo) {
    state.labels.push(label);
    state.selected = recalculateSelected(state);

}

function removeLabel(state: TaggerState, label: LabelInfo) {
    state.labels = state.labels.filter((item) => !(item.label_name == label.label_name && item.value == label.value && label.ref == item.ref))
    state.selected = recalculateSelected(state);

}

const Tagger: Module<TaggerState, RootState> = {
    namespaced: true,
    state: {
        labels: [],
        labelValue: LabelType.POS,
        labelName: "",
        candidates: [],
        selected: {},
        availableLabels: [],
    } as TaggerState,
    mutations: {
        setCandidates(state: TaggerState, candidates: CandidateInfo[]) {
            state.candidates = candidates;
        },
        setLabels(state: TaggerState, labels: LabelInfo[]) {
            state.labels = labels
            state.availableLabels = [...new Set(labels.map(item => item.label_name))]
            state.labelName = state.availableLabels ? state.availableLabels[0] : "label";
            state.selected = recalculateSelected(state);
        },
        switchLabelName(state: TaggerState, name: string) {
            state.labelName = name;
            state.selected = recalculateSelected(state);
        },
        switchLabelValue(state: TaggerState, value: LabelType) {
            state.labelValue = value;
            state.selected = recalculateSelected(state);
        },

        toggleLabel(state: TaggerState, label: LabelInfo) {
            if (hasLabel(state, label))
                removeLabel(state, label);
            else
                addLabel(state, label);
        },
        addLabel,
        removeLabel,
    },
    getters: {

    },
    actions: {
        async fetchLabels(context) {
            const resp = await fetch("/fs/labels.json")
            let data: LabelInfo[] = [];
            if (resp.status == 200) {
                data = await resp.json();
            } else if (resp.status == 404) {
                data = [];
            }
            context.commit('setLabels', data);
        },

        async save(context) {
            const resp = await fetch("/fs/labels.json", {
                method: "PUT",
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(context.state.labels)
            });
            if (resp.status !== 200) {
                console.log("error saving");
            }
        }
    }
}

export default Tagger;