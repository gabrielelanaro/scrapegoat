import { CandidateInfo } from './models';

export function extractBoxSize(cand: CandidateInfo) {
    const width = cand.rect.right - cand.rect.left;
    const height = cand.rect.bottom - cand.rect.top

    return {
        key: cand.path,
        x: cand.rect.left,
        y: cand.rect.top,
        width,
        height,
        z: - width * height,
    }
}