// Check linker predictions

import { LinkLabelInfo, LabelType, CandidateInfo } from '@/models';
import Vuex, { Store, Module, ActionContext, Action } from "vuex";
import { RootState } from './types';


interface SuggestLinkState {
    predictedLinks: LinkLabelInfo[];
}

const SuggestLink: Module<SuggestLinkState, RootState> = {
    namespaced: true,
    state: {
        predictedLinks: []
    },
    mutations: {
        setPredictedLinks(state, links: LinkLabelInfo[]) {
            state.predictedLinks = links;
        }
    },
    actions: {
        async predictLinks(context, { candidates, links }) {
            // Basically we ask, given candidates and links, wht we want to know

            const resp = await fetch("/api/predictLinks/", {
                method: "POST",
                body: JSON.stringify({ candidates, links })
            });

            const data = await resp.json() as LinkLabelInfo[];
            context.commit("setPredictedLinks", data);
        }
    }
}

export default SuggestLink;