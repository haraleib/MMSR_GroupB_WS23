#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
from typing import TypedDict, Literal

from utils import read_tsv


class RepresentationsMap(TypedDict):
    blf_correlation: pd.DataFrame
    blf_deltaspectral: pd.DataFrame
    blf_logfluc: pd.DataFrame
    blf_spectralcontrast: pd.DataFrame
    blf_spectral: pd.DataFrame
    blf_vardeltaspectral: pd.DataFrame
    genres: pd.DataFrame
    information: pd.DataFrame
    ivec256: pd.DataFrame
    ivec512: pd.DataFrame
    ivec1024: pd.DataFrame
    mfcc_bow: pd.DataFrame
    mfcc_stats: pd.DataFrame
    musicnn: pd.DataFrame
    bert: pd.DataFrame
    tf_idf: pd.DataFrame
    word2vec: pd.DataFrame

            
class SampledHistory(TypedDict):
    blf_correlation: list[str]
    blf_deltaspectral: list[str]
    blf_logfluc: list[str]
    blf_spectralcontrast: list[str]
    blf_spectral: list[str]
    blf_vardeltaspectral: list[str]
    genres: list[str]
    information: list[str]
    ivec256: list[str]
    ivec512: list[str]
    ivec1024: list[str]
    mfcc_bow: list[str]
    mfcc_stats: list[str]
    musicnn: list[str]
    bert: list[str]
    tf_idf: list[str]
    word2vec: list[str]


RepresentationKey = Literal["blf_correlation", "blf_deltaspectral", "blf_logfluc", "blf_spectralcontrast",
                            "blf_spectral", "blf_vardeltaspectral", "genres", "information", "ivec256",
                            "ivec512", "ivec1024", "mfcc_bow", "mfcc_stats", "musicnn", "bert", "tf_idf", "word2vec"]


class Datasets:
    def __init__(self):
        self._paths = {
            "blf_correlation": "datasets/id_blf_correlation_mmsr.tsv",
            "blf_deltaspectral": "datasets/id_blf_deltaspectral_mmsr.tsv",
            "blf_logfluc": "datasets/id_blf_logfluc_mmsr.tsv",
            "blf_spectralcontrast": "datasets/id_blf_spectralcontrast_mmsr.tsv",
            "blf_spectral": "datasets/id_blf_spectral_mmsr.tsv",
            "blf_vardeltaspectral": "datasets/id_blf_vardeltaspectral_mmsr.tsv",
            "genres": "datasets/id_genres_mmsr.tsv",
            "information": "datasets/id_information_mmsr.tsv",
            "ivec256": "datasets/id_ivec256_mmsr.tsv",
            "ivec512": "datasets/id_ivec512_mmsr.tsv",
            "ivec1024": "datasets/id_ivec1024_mmsr.tsv",
            "mfcc_bow": "datasets/id_mfcc_bow_mmsr.tsv",
            "mfcc_stats": "datasets/id_mfcc_stats_mmsr.tsv",
            "musicnn": "datasets/id_musicnn_mmsr.tsv",
            "bert": "datasets/id_lyrics_bert_mmsr.tsv",
            "tf_idf": "datasets/id_lyrics_tf-idf_mmsr.tsv",
            "word2vec": "datasets/id_lyrics_word2vec_mmsr.tsv"
        }
        self.sampled: SampledHistory = {
            "blf_correlation": [],
            "blf_deltaspectral": [],
            "blf_logfluc": [],
            "blf_spectralcontrast" : [],
            "blf_spectral" : [],
            "blf_vardeltaspectral" : [],
            "genres" : [],
            "information" : [],
            "ivec256" : [],
            "ivec512" : [],
            "ivec1024" : [],
            "mfcc_bow" : [],
            "mfcc_stats" : [],
            "musicnn" : [],
            "bert": [],
            "tf_idf": [],
            "word2vec": []
        }
        self._cached = {}

    def get_dataset(self, key: RepresentationKey) -> pd.DataFrame:
        if key in self._cached:
            return self._cached[key]
        df = read_tsv(self._paths[key])
        self._cached[key] = df
        return df

datasets = Datasets()

