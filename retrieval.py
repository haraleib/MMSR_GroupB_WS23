import pandas as pd
import sklearn.metrics as metrics
from enum import IntEnum

from song import Song, songs
from datasets import datasets, RepresentationKey


class SimilarityMeasure(IntEnum):
    COSINE = 0


class Retrieval:
    def __init__(self, n: int):
        self.n = n

    def random_baseline(self, song: Song) -> pd.DataFrame:
        # Exclude the query song from the dataset (if it exists)
        exclude_mask = (songs.info["song"] != song.title) | (songs.info["artist"] != song.artist)

        # Select N random songs from the filtered data
        random_results = songs.info[exclude_mask].sample(n=self.n)

        return random_results[["song", "artist"]]

    def text_based_similarity(
            self,
            song_id: int,
            feature: RepresentationKey,
            similarity_measure: SimilarityMeasure
    ) -> pd.DataFrame:
        representations = datasets.representations[feature]

        # representation of the query song
        query_repr = representations[(representations["id"] == song_id)]
        query_repr = query_repr.loc[:, query_repr.columns != "id"]

        # representation of all songs
        all_songs_repr = representations.loc[:, representations.columns != "id"]

        # Measure similarity between all (other) songs and the queried song
        if similarity_measure == SimilarityMeasure.COSINE:
            similarity = metrics.pairwise.cosine_similarity(X=all_songs_repr, Y=query_repr)
        else:
            raise ValueError(f"bad similarity measure supplied: {similarity_measure}")

        # Create a new dataframe with original representations
        # but also append a similarity column
        repr_with_similarity = representations.copy()
        repr_with_similarity.insert(1, "similarity", similarity)

        # sort by similarity and select top N results (excluding the query, which should be at index 0)
        repr_with_similarity = repr_with_similarity.sort_values(
            by="similarity",
            ascending=False
        ).iloc[1:self.n + 1]

        filtered = songs.info.loc[songs.info["id"].isin(repr_with_similarity["id"])]

        # sort the filtered dataframe by the order of the repr_with_similarity dataframe
        # include the similarity column in the sort so that the filtered dataframe is sorted by similarity
        filtered = filtered.merge(
            repr_with_similarity,
            on="id",
            suffixes=("", "_")
        ).sort_values("similarity", ascending=False)

        return filtered[["id", "similarity", "song", "artist"]]
