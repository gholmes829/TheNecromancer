"""

"""

import sys
import os.path as osp, os
import argparse
from icecream import ic
from gensim.models import FastText
from pprint import pprint


PAR_PATH = osp.dirname(osp.realpath(__file__))
sys.path.append(osp.abspath(osp.join(PAR_PATH, '..'))); import core as _
from core.nlp import sim_by_threshold
ROOT_PATH = osp.join(PAR_PATH, '..', '..')
DATA_PATH = osp.join(ROOT_PATH, 'data')
CORPUS_PATH = osp.join(DATA_PATH, 'corpora', 'Romantic & Gothic')
EMBEDDINGS_PATH = osp.join(DATA_PATH, 'embeddings')
TARGET_EMBEDDING_PATH = osp.abspath(osp.join(EMBEDDINGS_PATH, 'embeddings.model'))

def make_argparser() -> argparse.ArgumentParser:
    argparser = argparse.ArgumentParser(description='test most similar tokens based on embeddings')
    argparser.add_argument('query', help = 'query with which to find most similar tokens')
    argparser.add_argument('--threshold', '-t', type = float, help = 'max number of results to return')
    return argparser


def main():
    argparser = make_argparser()
    args = argparser.parse_args()
    query: str = args.query
    t: int = args.threshold
    ic(t, type(t))
    embedding_model: FastText = FastText.load(TARGET_EMBEDDING_PATH)
    pprint(sim_by_threshold(embedding_model, query, t))
    # pprint([(token, score) for token, score in embedding_model.wv.most_similar(query, topn = n or len(embedding_model.wv) + 1) if score > 0.5 and query not in token])


if __name__ == '__main__':
    main()