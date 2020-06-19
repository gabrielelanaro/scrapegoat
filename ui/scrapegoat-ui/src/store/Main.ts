import Vue from 'vue';
import Vuex, { ActionContext } from 'vuex';
import { RootState } from './types';
import { CandidateInfo } from '@/models'
import tagger from './Tagger';

Vue.use(Vuex);


export default new Vuex.Store<RootState>({
    state: {
        message: "hello",
        image: undefined,
    },
    modules: {
        tagger
    },
    mutations: {
        setImage(state, image) {
            state.image = image;
        },
    },
    actions: {
        async loadApp(context) {
            await context.dispatch('fetchImage');
            await context.dispatch('fetchCandidates');
            await context.dispatch('tagger/fetchLabels');
        },
        async fetchImage(context) {
            const image = new window.Image();
            image.src = "/fs/screenshot.png";
            context.commit('setImage', image);
        },
        async fetchCandidates(context) {
            const resp = await fetch("/fs/candidates.json")
            const data = await resp.json() as CandidateInfo[];
            context.commit('tagger/setCandidates', data);
        },
    }
});