import { Vue } from "vue-property-decorator";

function truncate(text: string, length: number, clamp?: string) {
    clamp = clamp || '...';
    const node = document.createElement('div');
    node.innerHTML = text;
    const content = node.textContent || "";
    return content.length > length ? content.slice(0, length) + clamp : content;
}


export default function registerFilters(Vue: Vue) {
    Vue.filter('truncate', truncate);
}