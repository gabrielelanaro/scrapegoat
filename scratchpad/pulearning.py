# Basically we have found the following facts:
# Making edge prediction only doesn't work, there are just too many possibilities, therefore we need to
# first do node classification, and then we need to tdo edge classification.
#
# And how do we do node classification?
# Two approaches: one of them would involve first performing a regular classification with the tagging tool
# and this is probably a good method anyway.
#
# Another approach can do everything together and it is as follows:
#
# 1. use the features to classify what can a "node" be. You need to extract the number of candidates. and this could be probably
# an hyperparameter of the range of 100 or whatever your capacity is. This is a PU labeling and can be done using a PUBagging classifier
# strategy.
#
# 2. use the candidates obtained to do link prediction. Again this is a PU learning problem and can be done using PUBagging or other methods.

from scrapegoat.store import Store
from scrapegoat.learn.link_extractor_pipeline import (
    suggest_new_links,
    LinkType,
    PULabelType,
)
import json

store = Store("immoscout/store")
page = store.get_page(
    "https://www.immobilienscout24.de/Suche/de/berlin/berlin/wohnung-mieten?numberofrooms=2.0-&price=-1300.0&enteredFrom=one_step_search"
)

candidates = page.get_candidates()
links = json.load((page._path / "linkLabels.json").open())


candidates_by_id = {c.path: c for c in candidates}


for link in links:
    source = candidates_by_id[link["source"]]
    target = candidates_by_id[link["target"]]

    print(source.text, "->", target.text)

links_typed = [
    LinkType(
        source=link["source"], target=link["target"], value=PULabelType(link["value"])
    )
    for link in links
]

nl = suggest_new_links(candidates, links_typed)

print("SUggetsted links")
for l in nl:
    print(candidates_by_id[l.source].text, "->", candidates_by_id[l.target].text)


1 / 0
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import LinearSVC
from scrapegoat.transforms import CandidateTransform
from scrapegoat.bagging_pu import BaggingClassifierPU
import random
import numpy as np


def train_graph(candidates, link_labels):
    true_edges = {(l["source"], l["target"]) for l in link_labels}
    print("training")
    positive = []
    unlabeled = []
    for source in candidates:
        for target in candidates:
            if (source.path, target.path) in true_edges:
                positive.append((source, target))
            else:
                unlabeled.append((source, target))

    # Let's do a naive approach, treat a sample as negative
    # negatives = random.choices(unlabeled, k=len(link_labels) * 10)
    negatives = unlabeled
    tf = CandidateTransform()

    X = []
    y = []

    for (source, target) in positive:
        X.append(encode_pair(tf.encode(source), tf.encode(target)))
        y.append(1.0)

    for (source, target) in negatives:
        X.append(encode_pair(tf.encode(source), tf.encode(target)))
        y.append(0.0)

    model = RandomForestClassifier()

    mdl = model.fit(X, y)
    proba = mdl.predict_proba(X[: len(positive)])

    return model, proba[:, 1].min(), proba[:, 1].max()


def predict_graph(candidates, model, min_thr, max_thr):
    tf = CandidateTransform()

    features = [tf.encode(candidate) for candidate in candidates]
    positive_links = []
    print("predicting")
    for i, source in enumerate(candidates):
        X = []
        for j, target in enumerate(candidates):
            X.append(encode_pair(features[i], features[j]))

        pred = model.predict_proba(X)[:, 1]

        for i, p in enumerate(pred):
            target = candidates[i]
            if p >= max_thr:
                print("p=", p, source.text[:100], "->", target.text[:100])
                positive_links.append({"source": source.path, "target": target.path})

    return positive_links


def _dedup_links(source, target):
    pass


links = links

for n in range(10):
    print("Step", n)
    print("---")

    reduced_list = train_binary(candidates, links)
    model, min_thr, max_thr = train_graph(reduced_list, links)

    new_links = predict_graph(reduced_list, model, min_thr, max_thr)

    links.extend(new_links)

