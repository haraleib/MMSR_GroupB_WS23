import numpy as np
import pandas as pd
from enum import IntEnum
from sklearn.metrics.pairwise import cosine_similarity

from song import songs
from datasets import datasets, LocalDataset


RETRIEVAL_SYSTEMS = {
    "random_baseline": lambda retN, query: retN.random_baseline(query),
    "text_tf_idf": lambda retN, query: retN.text_based_similarity(query, datasets.tf_idf, SimilarityMeasure.COSINE),
    "text_bert": lambda retN, query: retN.text_based_similarity(query, datasets.lyrics_bert, SimilarityMeasure.COSINE),
    "text_word2vec": lambda retN, query: retN.text_based_similarity(query, datasets.word2vec, SimilarityMeasure.COSINE),
    "mfcc_bow": lambda retN, query: retN.top_similar_tracks(query, datasets.mfcc_bow),
    "blf_correlation": lambda retN, query: retN.top_similar_tracks(query, datasets.blf_correlation),
    "ivec256": lambda retN, query: retN.top_similar_tracks(query, datasets.ivec256),
    "musicnn": lambda retN, query: retN.top_similar_tracks(query, datasets.musicnn),
}


class SimilarityMeasure(IntEnum):
    COSINE = 0


class Retrieval:
    def __init__(self, n: int):
        self.n = n

    def random_baseline(self, song_id) -> pd.DataFrame:
        # Exclude the query song from the dataset (if it exists)
        # exclude_mask = (songs.info["song"] != song.title) | (songs.info["artist"] != song.artist)
        exclude_mask = (songs.info["id"] != song_id)

        # Select N random songs from the filtered data
        random_results = songs.info[exclude_mask].sample(n=self.n)

        return random_results[["id", "song", "artist"]]

    def text_based_similarity(
            self,
            song_id: int,
            dataset: LocalDataset,
            similarity_measure: SimilarityMeasure
    ) -> pd.DataFrame:
        representations = dataset.df

        # representation of the query song
        query_repr = representations[(representations["id"] == song_id)]
        query_repr = query_repr.loc[:, query_repr.columns != "id"]

        # representation of all songs
        all_songs_repr = representations.loc[:, representations.columns != "id"]

        # Measure similarity between all (other) songs and the queried song
        if similarity_measure == SimilarityMeasure.COSINE:
            similarity = cosine_similarity(X=all_songs_repr, Y=query_repr)
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

    # Function to retrieve top N similar tracks
    def top_similar_tracks(self, query_track_id, dataset: LocalDataset):
        features_data = dataset.df
        if query_track_id not in features_data['id'].values:
            # print(f"Track ID {query_track_id} not found in the data.")
            raise ValueError(f"Track ID {query_track_id} not found in the data.")
        
        query_track_features = features_data[features_data['id'] == query_track_id].iloc[:, 1:].values

        # Calculate similarity with the given features
        similarity_matrix = cosine_similarity(query_track_features, features_data.iloc[:, 1:].values)

        # Get the indices of the top N similar tracks
        # similarity 1 = the song itself, hence it should not be returned
        top_indices = np.argsort(similarity_matrix[0])[-(self.n+1):-1][::-1]

        # Create a list to store rows
        result_rows = []

        # Populate the list with song and artist information
        for track_index in top_indices:
            track_id = features_data.loc[track_index, 'id']

            info_row = songs.info[songs.info['id'] == track_id]
            if not info_row.empty:
                artist = info_row['artist'].values[0]
                song = info_row['song'].values[0]

                result_rows.append({
                    'id': track_id,
                    'similarity': similarity_matrix[0][track_index],
                    'song': song,
                    'artist': artist,
                })
                
        # Create the DataFrame from the list of dictionaries
        result_df = pd.DataFrame(result_rows)

        # Sort the DataFrame based on "Similarity" column
        result_df = result_df.sort_values(by='similarity', ascending=False)

        # Display sorted results
        # print(f"\nTop {self.n} Similar Tracks:")
        # print(result_df)
        return result_df
