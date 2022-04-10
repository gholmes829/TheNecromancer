"""

"""

import sys
import os.path as osp, os
import argparse
from icecream import ic
from tqdm import tqdm

import nlp

PAR_PATH = osp.dirname(osp.realpath(__file__))
ROOT_PATH = osp.join(PAR_PATH, '..')
DATA_PATH = osp.join(ROOT_PATH, 'data')
sys.path.append(DATA_PATH)
from interface import CorpusInterface
CORPUS_PATH = osp.join(DATA_PATH, 'corpora', 'Romantic & Gothic')
PROCESSED_DOCS_PATH = osp.join(DATA_PATH, 'processed_docs')
EMBEDDINGS_PATH = osp.join(DATA_PATH, 'embeddings')


def make_argparser() -> argparse.ArgumentParser:
    argparser = argparse.ArgumentParser()
    return argparser


def main():
    argparser = make_argparser()
    args = argparser.parse_args()

    corpus = CorpusInterface().get_corpus(CORPUS_PATH)
    docs_sent_tokens = {doc.title: nlp.process_and_sent_tokenize(doc.text) for doc in tqdm(corpus, desc = 'Preprocessing docs')}
    
    for title, doc_sent_tokens in docs_sent_tokens.items():
        with open(osp.join(PROCESSED_DOCS_PATH, f'{title}.txt'), 'w') as f:
            f.write(' '.join(token for sent in doc_sent_tokens for token in sent))

    embedding_model = nlp.generate_embeddings(list(docs_sent_tokens.values()))
    embedding_model.save(osp.join(EMBEDDINGS_PATH, 'embeddings.model'))


if __name__ == '__main__':
    main()