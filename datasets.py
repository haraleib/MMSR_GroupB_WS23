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


RepresentationKey = Literal["blf_correlation", "blf_deltaspectral", "blf_logfluc", "blf_spectralcontrast",
                            "blf_spectral", "blf_vardeltaspectral", "genres", "information", "ivec256",
                            "ivec512", "ivec1024", "mfcc_bow", "mfcc_stats", "musicnn" ]


class Datasets:
    def __init__(self):
        self.representations: RepresentationsMap = {
            "blf_correlation": read_tsv("datasets/id_blf_correlation_mmsr.tsv"),
            "blf_deltaspectral": read_tsv("datasets/id_blf_deltaspectral_mmsr.tsv"),
            "blf_logfluc": read_tsv("datasets/id_blf_logfluc_mmsr.tsv"),
            "blf_spectralcontrast": read_tsv("datasets/id_blf_spectralcontrast_mmsr.tsv"),
            "blf_spectral": read_tsv("datasets/id_blf_spectral_mmsr.tsv"),
            "blf_vardeltaspectral": read_tsv("datasets/id_blf_vardeltaspectral_mmsr.tsv"),
            "genres": read_tsv("datasets/id_genres_mmsr.tsv"),
            "information": read_tsv("datasets/id_information_mmsr.tsv"),
            "ivec256": read_tsv("datasets/id_ivec256_mmsr.tsv"),
            "ivec512": read_tsv("datasets/id_ivec512_mmsr.tsv"),
            "ivec1024": read_tsv("datasets/id_ivec1024_mmsr.tsv"),
            "mfcc_bow": read_tsv("datasets/id_mfcc_bow_mmsr.tsv"),
            "mfcc_stats": read_tsv("datasets/id_mfcc_stats_mmsr.tsv"),
            "musicnn": read_tsv("datasets/id_musicnn_mmsr.tsv"),

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

        }


datasets = Datasets()

