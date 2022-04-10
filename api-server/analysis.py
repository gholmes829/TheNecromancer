"""

"""

import sys
import os.path as osp, os
from icecream import ic
from gensim.models import FastText
from collections import defaultdict
from tqdm import tqdm
from functools import lru_cache
import numpy as np
import json
import numpy as np


PAR_PATH = osp.dirname(osp.realpath(__file__))
sys.path.append(osp.abspath(osp.join(PAR_PATH, '..'))) #; import mgcore as _
import nlp
ROOT_PATH = osp.join(PAR_PATH, '..')
DATA_PATH = osp.join(ROOT_PATH, 'data')
EMBEDDINGS_PATH = osp.join(DATA_PATH, 'embeddings')
TARGET_EMBEDDING_PATH = osp.abspath(osp.join(EMBEDDINGS_PATH, 'embeddings.model'))
PROCESSED_DOCS_PATH = osp.join(DATA_PATH, 'processed_docs')

EMBEDDING_MODEL: FastText = FastText.load(TARGET_EMBEDDING_PATH)
METADATA_PATH = osp.join(DATA_PATH, 'corpora', 'Romantic & Gothic', 'info.json')

@lru_cache(maxsize=2**16)
def similarity(w1: str, w2: str):
    return (EMBEDDING_MODEL.wv.similarity(w1, w2) + 1) / 2

with open(METADATA_PATH, 'r') as f:
    METADATA: list[dict] = json.load(f)

DOC_TERMS = {}
for doc_path in os.listdir(PROCESSED_DOCS_PATH):
    with open(osp.join(PROCESSED_DOCS_PATH, doc_path), 'r') as f:
        DOC_TERMS[osp.splitext(osp.basename(doc_path))[0]] = f.read().split()

earliest = float('inf')
latest = float('-inf')

year_to_titles = defaultdict(set)

for data in METADATA:
    title = data['title']
    year = data['year']
    if year < earliest:
        earliest = year
    if year > latest:
        latest = year
    year_to_titles[year].add(title)
    
years_range = latest - earliest


def prev_over_time(query: list[str], window: int = 5):
    query_tokens = nlp.process_and_word_tokenize(query)
    t_scores = []
    for t in tqdm(range(earliest, latest + 1)):
        docs_t = [DOC_TERMS[title] for title in year_to_titles[t]]
        if not docs_t:
            t_scores.append(0)
            continue
        t_scores.append(sum([sim for qt in query_tokens for doc in docs_t for dt in doc if (sim := similarity(qt, dt)) > 0.7]) / (len(query_tokens) * sum([len(doc) for doc in docs_t])))
    smoothed_t_scores = []
    for i in range(window, latest - earliest + 1):
        smoothed_t_scores.append(sum(t_scores[i - window:i]) / window)
    T = list(range(earliest + window, latest + 1))
    Y = smoothed_t_scores
    text = [str(len(year_to_titles[t])) + ' docs' for t in range(earliest + window, latest + 1)]
    return {
        'x': T,
        'y': Y,
        'text': text,
        }

def statistics(query: list[str]):
    query_tokens = nlp.process_and_word_tokenize(query)
    d = defaultdict(lambda: {'c': 0, 's': 0})
    for token in query_tokens:
        closest_words = [(word, score) for word, score in EMBEDDING_MODEL.wv.most_similar(token, topn = 50) if token not in word]
        for word, score in closest_words:
            d[word]['c'] += 1
            d[word]['s'] += score

    relevant_words = [(word, data['c'], data['s'] / data['c']) for word, data in d.items()]
    relevant_words.sort(key = lambda x: (lambda word, count, avg_s: count + avg_s)(*x), reverse = True)
    return list(np.array(relevant_words[:10])[:, 0])

prev_over_time('death')