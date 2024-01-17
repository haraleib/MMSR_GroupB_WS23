import os
import pandas as pd
from typing import Optional

from utils import read_tsv


class LocalDataset:
    def __init__(self, name: str, df: Optional[pd.DataFrame] = None):
        self.name = name

        if df is not None:
            self.df = df
        else:
            if not os.path.isdir("datasets"):
                raise RuntimeError(
                    "'datasets' directory not present. "
                    "Create it in the project root folder and place your dataset files there."
                )

            self.df: pd.DataFrame = read_tsv(f"datasets/id_{name}_mmsr.tsv")

        self.df = self.df[self.df["id"] != "03Oc9WeMEmyLLQbj"]

        if self.df.empty:
            print(f"WARN: DataFrame '{name}' is empty!")

    def __str__(self):
        return self.name


class Datasets:
    def __init__(self):
        self.blf_correlation = LocalDataset("blf_correlation")
        self.blf_deltaspectral = LocalDataset("blf_deltaspectral")
        self.blf_logfluc = LocalDataset("blf_logfluc")
        self.blf_spectralcontrast = LocalDataset("blf_spectralcontrast")
        self.blf_spectral = LocalDataset("blf_spectral")
        self.blf_vardeltaspectral = LocalDataset("blf_vardeltaspectral")
        self.genres = LocalDataset("genres")
        self.information = LocalDataset("information")
        self.ivec256 = LocalDataset("ivec256")
        self.ivec512 = LocalDataset("ivec512")
        self.ivec1024 = LocalDataset("ivec1024")
        self.mfcc_bow = LocalDataset("mfcc_bow")
        self.mfcc_stats = LocalDataset("mfcc_stats")
        self.musicnn = LocalDataset("musicnn")
        self.lyrics_bert = LocalDataset("lyrics_bert")
        self.tf_idf = LocalDataset("lyrics_tf-idf")
        self.word2vec = LocalDataset("lyrics_word2vec")
        self.url = LocalDataset("url")
        self.incp = LocalDataset("incp")
        self.resnet = LocalDataset("resnet")
        self.vgg = LocalDataset("vgg19")
        self.musicnn = LocalDataset("musicnn")
        self.resnet = LocalDataset("resnet")


datasets = Datasets()
