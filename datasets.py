import pandas as pd
from typing import TypedDict, Literal

from utils import read_tsv


class RepresentationsMap(TypedDict):
    bert: pd.DataFrame
    tf_idf: pd.DataFrame
    word2vec: pd.DataFrame


class SampledHistory(TypedDict):
    bert: list[str]
    tf_idf: list[str]
    word2vec: list[str]


RepresentationKey = Literal["bert", "tf_idf", "word2vec"]


class Datasets:
    def __init__(self):
        self.representations: RepresentationsMap = {
            "bert": read_tsv("datasets/id_lyrics_bert_mmsr.tsv"),
            "tf_idf": read_tsv("datasets/id_lyrics_tf-idf_mmsr.tsv"),
            "word2vec": read_tsv("datasets/id_lyrics_word2vec_mmsr.tsv")
        }
        self.sampled: SampledHistory = {
            "bert": [],
            "tf_idf": [],
            "word2vec": []
        }


datasets = Datasets()
