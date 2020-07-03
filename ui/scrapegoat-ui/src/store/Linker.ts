import { LinkLabelInfo, LabelType, CandidateInfo } from '@/models';
import Vuex, { Store, Module, ActionContext } from "vuex";
import { RootState } from './types';

enum SelectionFocus {
    SOURCE = 'source',
    TARGET = 'target'
}

interface LinkerState {
    links: LinkLabelInfo[];
    selectedLinkName: string;
    labelType: LabelType;
    candidates: CandidateInfo[];
    focus: SelectionFocus;
    selectedSource?: CandidateInfo;
    selectedTarget?: CandidateInfo;
    availableLabels: string[];
}


const Linker: Module<LinkerState, RootState> = {
    namespaced: true,
    state: {
        links: [],
        selectedLinkName: "",
        labelType: LabelType.POS,
        candidates: [],
        focus: SelectionFocus.SOURCE,
        selectedSource: undefined,
        selectedTarget: undefined,
        availableLabels: []
    },
    mutations: {
        setCandidates(state, candidates: CandidateInfo[]) {
            state.candidates = candidates;
        },
        setSource(state, arg: CandidateInfo) {
            state.selectedSource = arg;
        },
        setTarget(state, arg: CandidateInfo) {
            state.selectedTarget = arg;
        },
        setLabelType(state, arg: LabelType) {
            state.labelType = arg;
        },
        addLink(state, arg: LinkLabelInfo) {
            state.links.push(arg);
        },
        removeLink(state, arg: LinkLabelInfo) {
            state.links = state.links.filter((item) => (item.source != arg.source || item.target != arg.target));
        },
        setLinks(state, arg: LinkLabelInfo[]) {
            state.links = arg;
        }
    },
    getters: {

    },
    actions: {
        async createLink(context) {
            if (context.state.selectedSource && context.state.selectedTarget) {
                const link: LinkLabelInfo = {
                    value: context.state.labelType,
                    linkName: context.state.labelType,
                    source: context.state.selectedSource.path,
                    target: context.state.selectedTarget.path,
                    remarks: ["manual"]
                }
                context.commit('addLink', link)
            }
        },
        async save(context) {
            const resp = await fetch("/fs/linkLabels.json", {
                method: "PUT",
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(context.state.links)
            });
            if (resp.status !== 200) {
                console.log("error saving");
            }
        },

        async fetch(context) {
            const resp = await fetch("/fs/linkLabels.json")
            let data: LinkLabelInfo[] = [];
            if (resp.status == 200) {
                data = await resp.json();
            } else if (resp.status == 404) {
                data = [];
            }
            context.commit('setLinks', data);
        },
    }
}

export default Linker;