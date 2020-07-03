from typing import List

from ..types import Candidate, LabelValue
from .node_extraction import NodeExtractionModel, PULabelType
from .edge_extraction import EdgeExtractionModel, LinkType


def suggest_new_links(
    candidates: List[Candidate], links: List[LinkType]
) -> List[LinkType]:
    # We use a transductive model to find the possible nodes for linking
    node_extraction = NodeExtractionModel(pos_thr=0.5)
    # Extract source and target
    pos_links = [l for l in links if l.value == PULabelType.POS]
    neg_links = [l for l in links if l.value == PULabelType.NEG]

    node_set = {l.source for l in pos_links}.union({l.target for l in pos_links})

    labels = [
        PULabelType.POS if c.path in node_set else PULabelType.UNK for c in candidates
    ]
    pred_labels = node_extraction.learn(candidates, labels)

    pred_nodes = [
        c
        for c, l in zip(candidates, pred_labels)
        if l.label == PULabelType.POS or c.path in node_set
    ]

    # We use a linking model to find the edges.
    # We need to first of all filter out the links that are not related to the pred nodes
    relevant_nodes = {p.path for p in pred_nodes}
    relevant_links = [
        l for l in links if l.source in relevant_nodes and l.target in relevant_nodes
    ]

    edge_extraction = EdgeExtractionModel()
    pred_links = edge_extraction.learn(pred_nodes, relevant_links)
    pred_links = sorted(pred_links, key=lambda x: x.p)

    # Now, we could return the links
    labeled_links = {(l.source, l.target) for l in links}

    return [
        pl.link
        for pl in pred_links
        if pl.link.value == PULabelType.POS
        and ((pl.link.source, pl.link.target) not in labeled_links)
    ]
