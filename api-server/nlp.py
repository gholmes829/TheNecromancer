"""

"""

from nltk.corpus import stopwords as stopwords_model
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize, sent_tokenize
from unidecode import unidecode
from gensim.models import FastText
from gensim.models.callbacks import CallbackAny2Vec
from functools import lru_cache
from psutil import cpu_count
from tqdm import tqdm
import math
import re
from icecream import ic

LEMMATIZER = WordNetLemmatizer()
STOPWORDS = set(stopwords_model.words('english'))
REMOVE_PTN = re.compile(r'[^a-z]+')

@lru_cache(maxsize=2**15)  # 2**15 = 32768
def _lemmatize(target: str) -> str:
    return LEMMATIZER.lemmatize(target)
_lemmatize('')  # loads model when running for first time


def _preprocess(text: str) -> str:
    return re.sub(REMOVE_PTN, lambda m: ' ', unidecode(text).lower())


def _valid_token(token: str) -> bool:
    return token not in STOPWORDS and len(token) > 1


def process_and_word_tokenize(text: str) -> list[str]:
    """Turns raw text string into list of preprocessed tokens."""
    return [_lemmatize(token) for token in word_tokenize(_preprocess(text)) if _valid_token(token)]


def process_and_sent_tokenize(text: str) -> list[list[str]]:
    """Turns raw text string into list of preprocessed tokens."""
    return [[_lemmatize(token) for token in word_tokenize(_preprocess(sent)) if _valid_token(token)] for sent in sent_tokenize(text)]


class _EmbeddingProgress(CallbackAny2Vec):
    def __init__(self, max_epochs) -> None:
        super().__init__()
        self.epoch = 0
        self.pbar = tqdm(total = max_epochs, desc = 'generating embeddings')

    def on_epoch_end(self, _) -> None:
        self.pbar.update()
        self.epoch += 1
    
    def on_train_end(self, _) -> None:
        del self.pbar


def sim_by_threshold(embedding_model, query, threshold):
    return [(token, score) for token, score in embedding_model.wv.most_similar(query, topn = len(embedding_model.wv) + 1) if score > threshold and query not in token]


def generate_embeddings(docs_sent_tokens: set[list[list[str]]], epochs: int = 5) -> FastText:
    sent_tokens = [sent for doc_sent_tokens in docs_sent_tokens for sent in doc_sent_tokens]
    return FastText(
        sent_tokens,
        sample = 0.001,                             # default
        vector_size = 100,                          # default
        window = 4,                                 # 5 default
        epochs = epochs,                            # 5 is default
        min_count = 5,                              # default
        workers = math.floor(0.75 * cpu_count()),   # default is 3
        sg = 1,                                     # default is 0
        callbacks = (_EmbeddingProgress(epochs),)    # default is None
    )