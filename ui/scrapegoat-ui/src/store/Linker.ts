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
    selectedLinkValue: LabelType;
    candidates: CandidateInfo[];
    focus: SelectionFocus;
    selectedSource: { [key: string]: boolean };
    selectedTarget: { [key: string]: boolean };
    availableLabels: string[];
}


const Linker: Module<LinkerState, RootState> = {
    namespaced: true,
    state: {
        links: [],
        selectedLinkName: "",
        selectedLinkValue: LabelType.POS,
        candidates: [],
        focus: SelectionFocus.SOURCE,
        selectedSource: {},
        selectedTarget: {},
        availableLabels: []
    },
    mutations: {
        setCandidates(state, candidates: CandidateInfo[]) {
            state.candidates = candidates;
        }
    },
    getters: {

    },
    actions: {

    }
}

export default Linker;