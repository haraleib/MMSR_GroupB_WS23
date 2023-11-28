import pandas as pd


def read_tsv(file: str) -> pd.DataFrame:
    return pd.read_csv(file, sep="\t")
