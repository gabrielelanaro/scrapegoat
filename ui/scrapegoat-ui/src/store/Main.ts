import Vue from 'vue';
import Vuex, { ActionContext } from 'vuex';
import { RootState } from './types';
import { CandidateInfo } from '@/models'
import tagger from './Tagger';
import linker from "./Linker";
import suggestLink from "./SuggestLink";

Vue.use(Vuex);


export default new Vuex.Store<RootState>({
    state: {
        message: "hello",
        image: undefined,
    },
    modules: {
        tagger,
        linker,
        suggestLink
    },
    mutations: {
        setImage(state, image) {
            console.log("image set", image.width, image.height);
            state.image = image;
        },
    },
    actions: {
        async loadApp(context) {
            await context.dispatch('fetchImage');
            await context.dispatch('fetchCandidates');
            await context.dispatch('tagger/fetchLabels');
            await context.dispatch('linker/fetch');
        },
        async fetchImage(context) {
            const image = new window.Image();
            image.onload = () => context.commit('setImage', image);
            image.src = "/fs/screenshot.png";
        },
        async fetchCandidates(context) {
            const resp = await fetch("/fs/candidates.json")
            const data = await resp.json() as CandidateInfo[];
            context.commit('tagger/setCandidates', data);
        },
    }
});