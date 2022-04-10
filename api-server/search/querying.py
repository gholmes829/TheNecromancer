"""

"""

# from typing import Hashable, Tuple
import re
import numpy as np
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from unidecode import unidecode
from functools import lru_cache
from icecream import ic
import os.path as osp
import json

PAR_PATH = osp.dirname(osp.realpath(__file__))
ROOT_PATH = osp.join(PAR_PATH, '..', '..')
SEARCH_PATH = osp.join(ROOT_PATH, 'api-server', 'search')

with open(osp.join(SEARCH_PATH, 'index.json'), 'r') as f: index = json.load(f)
with open(osp.join(SEARCH_PATH, 'doc_names.json'), 'r') as f: doc_name_to_vec= json.load(f)
with open(osp.join(SEARCH_PATH, 'vocab_set.json'), 'r') as f: vocab_set = frozenset(json.load(f))


stemmer = PorterStemmer(); stemmer.stem('')  # loads stem
punc_ptn = re.compile(r'\W', re.ASCII)
stops = set(stopwords.words('english'))


@lru_cache(maxsize=50000)
def stem(token: str) -> str:
    return stemmer.stem(token)


def valid_token(token: str) -> bool:
    return token and token not in stops


def normalize(token: str) -> str:
    return stem(token.strip().lower())


def resolve_token(token: str) -> str:
    return normal if valid_token(normal := normalize(token)) else None


def preprocess(text: str) -> list[str]:
    return [resolve_token(token) for token in re.sub(punc_ptn, ' ', unidecode(text)).split()]

def smooth(x, smoothness: float = 1):
    return 2 * (1 / (1 + np.exp(-x / smoothness)) - 0.5)


def handle_boolean_query(index, query: str) -> list[tuple[str, float]]:
    raise NotImplementedError


def make_query_vector(query_tokens: list[str]) -> np.ndarray:
    query_tf = {term: query_tokens.count(term) for term in set(query_tokens)}
    query_vector = np.zeros(len(index))
    for term in query_tokens: query_vector[index[term]['idx']] = query_tf[term] * index[term]['idf']
    if not (query_norm := np.linalg.norm(query_vector)):
        return None
    normalized = query_vector / query_norm
    return normalized


def is_candidate(query: list[str], doc_name: str) -> bool:
    for q in query:
        if doc_name in index[q]['locs']: return True
    return False

# def cache_filter(_, query: str, *args, **kwargs) -> Tuple[Hashable, ...]: return hashkey(query)

def search(query: str, top_k: int = 10) -> list[tuple[str, float]]:    
    query_tokens = [term for term in preprocess(query) if term in index] # replce index with a vocab list
    doc_names = np.array([doc for doc in doc_name_to_vec if is_candidate(query_tokens, doc)])
    if not doc_names.shape[0]: return None
    doc_matrix = np.array([doc_name_to_vec[doc] for doc in doc_names])
    scores = doc_matrix @ make_query_vector(query_tokens)
    sorted_idx = np.argsort(scores)[::-1]
    flat = {
        "names": list(doc_names[sorted_idx][:top_k]),
        "scores": list(smooth(np.array(scores[sorted_idx][:top_k]), 0.05))
    }
    # generate dict with keys doc_names[sorted_idx][:top_k] and values smooth(np.array(scores[sorted_idx][:top_k]), 0.05)
    new_dict = {k: v for k, v in zip(flat['names'], flat['scores'])}
    return new_dict

if __name__ == "__main__":
    q = ""
    while q != 'exit':
        q = input("")
        ic(search(q))

#ic(search("death"))