import json
import time
import threading
from enum import IntEnum
from pathlib import Path
from typing import Union, Any
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import pandas as pd
from tqdm.notebook import tqdm
from sklearn.metrics.pairwise import cosine_similarity

from song import songs
from datasets import datasets, LocalDataset
from late_fusion import LateFusion


def do_late_fusion(retN, query: str) -> list[list[Union[int, Any]]]:
    results1 = retN.top_similar_tracks(query, datasets.ef_bert_mfcc)
    results2 = retN.top_similar_tracks(query, datasets.resnet)
    lf = LateFusion(
        df1=Retrieval.create_df_from_tracks(results1),
        df2=Retrieval.create_df_from_tracks(results2),
        df1_weight=0.5,
        df2_weight=0.5,
        method="rank"
    )
    return [
        [
            row["id"],
            row["similarity"]
        ] for idx, row in lf.df[:retN.n].iterrows()
    ]


RETRIEVAL_SYSTEMS = {
    "random_baseline": lambda retN, query: retN.random_baseline(query),
    # lyrics
    "text_tf_idf": lambda retN, query: retN.top_similar_tracks(query, datasets.tf_idf),
    "text_bert": lambda retN, query: retN.top_similar_tracks(query, datasets.lyrics_bert),
    "text_word2vec": lambda retN, query: retN.top_similar_tracks(query, datasets.word2vec),

    # audio
    "musicnn": lambda retN, query: retN.top_similar_tracks(query, datasets.musicnn),
    "mfcc_bow": lambda retN, query: retN.top_similar_tracks(query, datasets.mfcc_bow),
    "mfcc_stats": lambda retN, query: retN.top_similar_tracks(query, datasets.mfcc_stats),
    "ivec256": lambda retN, query: retN.top_similar_tracks(query, datasets.ivec256),
    "ivec512": lambda retN, query: retN.top_similar_tracks(query, datasets.ivec512),
    "ivec1024": lambda retN, query: retN.top_similar_tracks(query, datasets.ivec1024),
    "blf_correlation": lambda retN, query: retN.top_similar_tracks(query, datasets.blf_correlation),
    "blf_deltaspectral": lambda retN, query: retN.top_similar_tracks(query, datasets.blf_deltaspectral),
    "blf_logfluc": lambda retN, query: retN.top_similar_tracks(query, datasets.blf_logfluc),
    "blf_spectral": lambda retN, query: retN.top_similar_tracks(query, datasets.blf_spectral),
    "blf_spectralcontrast": lambda retN, query: retN.top_similar_tracks(query, datasets.blf_spectralcontrast),
    "blf_vardeltaspectral": lambda retN, query: retN.top_similar_tracks(query, datasets.blf_vardeltaspectral),

    # video
    "video_resnet": lambda retN, query: retN.top_similar_tracks(query, datasets.resnet),
    "video_incp": lambda retN, query: retN.top_similar_tracks(query, datasets.incp),
    "video_vgg19": lambda retN, query: retN.top_similar_tracks(query, datasets.vgg19),

    # fusion
    "ef_bert_musicnn": lambda retN, query: retN.top_similar_tracks(query, datasets.ef_bert_musicnn),
    "ef_bert_mfcc": lambda retN, query: retN.top_similar_tracks(query, datasets.ef_bert_mfcc),

    "lf_bert_mfcc_musicnn": do_late_fusion,
}


class SimilarityMeasure(IntEnum):
    COSINE = 0


class Retrieval:
    def __init__(self, n: int, use_cache: bool = True):
        self.n = n

        self._cache = {}
        self._cache_lock = threading.Lock()

        self._cache_dir = Path("retrievals")
        self._cache_dir.mkdir(exist_ok=True)

        if use_cache:
            self.sync_cache_with_disk()

    def sync_cache_with_disk(self):
        cache_was_empty = len(self._cache) == 0

        with self._cache_lock:
            for p in self._cache_dir.iterdir():
                try:
                    if p.name == "songMeta" or p.suffix != ".json":
                        continue

                    if p.stem == "songMeta":
                        continue

                    with p.open() as fp:
                        old_cache = json.load(fp)

                    dataset_name = p.stem
                    if dataset_name not in self._cache:
                        self._cache[dataset_name] = {}

                    self._cache[dataset_name].update(old_cache)
                except Exception as e:
                    print(f"Error syncing cache for '{p.name}' with disk: {e}")

            if not cache_was_empty:
                for dataset_name in self._cache:
                    with (self._cache_dir / (dataset_name + ".json")).open("w") as fp:
                        json.dump(self._cache[dataset_name], fp)

    def precompute_all(self, threads: int):
        self.sync_cache_with_disk()

        with ThreadPoolExecutor(max_workers=threads) as executor:
            for retrieval in RETRIEVAL_SYSTEMS:
                if retrieval != "random_baseline":
                    executor.submit(self.precompute, retrieval)

    def precompute(self, retrieval):
        ret_sys = RETRIEVAL_SYSTEMS[retrieval]
        for idx, song_id in tqdm(
            enumerate(songs.info["id"]),
            total=len(songs.info["id"]),
            desc=f"Precomputing top-{self.n} tracks for retrieval '{retrieval}'",
        ):
            ret_sys(self, song_id)

            if idx % 1000 == 0:
                self.sync_cache_with_disk()

        print(f"Precomputed results for: '{retrieval}'")
        self.sync_cache_with_disk()

    def random_baseline(self, song_id) -> list[list[Union[int, Any]]]:
        # Exclude the query song from the dataset (if it exists)
        # and select N random songs from the filtered data
        random_results = songs.info[songs.info["id"] != song_id].sample(n=self.n)
        return [[id, 1] for id in random_results["id"].values]

    def top_similar_tracks(self, query_track_id, dataset: LocalDataset):
        with self._cache_lock:
            if dataset.name not in self._cache:
                self._cache[dataset.name] = {}

            if query_track_id in self._cache[dataset.name]:
                cached = self._cache[dataset.name][query_track_id][:self.n]
                # only return cached if it is the same length as n
                if len(cached) == self.n:
                    return cached

        result = self._top_similar_tracks(query_track_id, dataset)
        with self._cache_lock:
            self._cache[dataset.name][query_track_id] = result

        return result

    # Function to retrieve top N similar tracks
    def _top_similar_tracks(self, query_track_id, dataset: LocalDataset):
        start_time = time.time()
        features_data = dataset.df if isinstance(dataset, LocalDataset) else dataset
        if query_track_id not in features_data['id'].values:
            # print(f"Track ID {query_track_id} not found in the data.")
            raise ValueError(f"Track ID {query_track_id} not found in the data.")
        
        query_track_features = features_data[
            features_data['id'] == query_track_id
        ].iloc[:, features_data.columns != "id"].values

        # Calculate similarity with the given features
        similarity_matrix = cosine_similarity(
            query_track_features,
            features_data.iloc[:, features_data.columns != "id"].values
        )

        # Get the indices of the top N similar tracks
        # similarity 1 = the song itself, hence it should not be returned
        top_indices = np.argsort(similarity_matrix[0])[-(self.n+1):-1][::-1]

        # Create a list to store rows
        result_rows = []

        # Populate the list with song and artist information
        for track_index in top_indices:
            track_id = features_data.iat[track_index, features_data.columns.get_loc('id')]
            similarity = similarity_matrix[0][track_index]
            result_rows.append([track_id, similarity])

        return result_rows

    @staticmethod
    def create_df_from_tracks(tracks):
        result_rows = []
        for [track_id, similarity] in tracks:
            info_row = songs.info[songs.info['id'] == track_id]
            if not info_row.empty:
                artist = info_row['artist'].values[0]
                song = info_row['song'].values[0]
                album_name = info_row['album_name'].values[0]
                result_rows.append({
                    'id': track_id,
                    'similarity': similarity,
                    'song': song,
                    'artist': artist,
                    'album_name': album_name,
                })
        result_df = pd.DataFrame(result_rows)
        # Sort the DataFrame based on "Similarity" column
        result_df = result_df.sort_values(by='similarity', ascending=False)
        return result_df
