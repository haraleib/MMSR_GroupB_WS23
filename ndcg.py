from math import log2
import time

from matplotlib import pyplot as plt
from precision_recall import retrievals
from utils import unpickle_or_compute

class Ndcg:
    def __init__(self, n, genres):
        self._n = n
        self._genres = genres

    def plot(self):
        ndcgs = self._compute()

        retrieval_names = []
        ndcg_values = []
        for retrieval_name, ndcg in ndcgs.items():
            retrieval_names.append(retrieval_name)
            ndcg_values.append(ndcg)
        ndcg_values, retrieval_names = zip(*sorted(zip(ndcg_values, retrieval_names), reverse=False))
        plt.bar(retrieval_names, ndcg_values)
        plt.xlabel("Retrieval method")
        plt.ylabel("NDCG")
        # plt.xticks(rotation=45)
        plt.xticks(rotation=30, ha='right')
        plt.title(f"NDCG@{self._n}")
        plt.show()

    def _compute(self):
        ndcgs = {}
        i = 0
        chunk_size = 1000
        chunks = [self._genres.get_song_ids_with_genre_info()[i:i + chunk_size] for i in range(0, len(self._genres.get_song_ids_with_genre_info()), chunk_size)]
        for chunk_id, chunk in enumerate(chunks):
            print(f"Processing chunk {chunk_id + 1}/{len(chunks)}")

            chunk_ndcgs = unpickle_or_compute(f"ndcg_{self._n}_chunk_{chunk_id}.pickle", lambda: self._compute_chunk(chunk))
            for retrieval_name, ndcg in chunk_ndcgs.items():
                ndcgs[retrieval_name] = ndcgs.get(retrieval_name, 0) + ndcg
            
        for retrieval_name in ndcgs:
            ndcgs[retrieval_name] /= len(self._genres.get_song_ids_with_genre_info())
        
        return ndcgs

    def _compute_chunk(self, chunk):
        start_time = time.time()
        i = 0
        ndcgs = {}
        for song_id in chunk:
            idcg = self._get_idcg(song_id)

            for retrieval_name, retrieval in retrievals.items():
                retrieved = retrieval(self._n, song_id)
                retrieved = list(retrieved["id"])
                dcg = self._get_dcg(song_id, retrieved)
                ndcg = dcg / idcg
                ndcgs[retrieval_name] = ndcgs.get(retrieval_name, 0) + ndcg

                print(f"NDCG for {retrieval_name} on {song_id}: {ndcg} (DCG: {dcg}, IDCG: {idcg})")

            i += 1
            current_time = time.time()
            time_per_song = (current_time - start_time) / i
            remaining = time_per_song * (len(chunk) - i)
            print(f"Processed {i} songs, about {round(remaining / 60)} minutes remaining for chunk")
        return ndcgs

    def _get_idcg(self, song_id):
        all_songs = self._genres.get_song_ids_with_genre_info().copy()
        all_songs.sort(key=lambda song: self._get_relevance(song_id, song), reverse=True)
        retrieved_songs = all_songs[:self._n]
        return self._get_dcg(song_id, retrieved_songs)

    def _get_dcg(self, query_id, retrieval):
        dcg = self._get_relevance(query_id, retrieval[0])
        for i in range(1, self._n):
            dcg += self._get_relevance(query_id, retrieval[i]) / (log2(i + 1))
        return dcg

    def _get_relevance(self, query_song, other_song):
        query_genres = self._genres.get_song_genre(query_song)
        other_song_genres = self._genres.get_song_genre(other_song)
        if query_genres is None or other_song_genres is None:
            return 0
        query_genres = set(query_genres)
        other_song_genres = set(other_song_genres)
        return 2 * len(query_genres.intersection(other_song_genres)) / (len(query_genres) + len(other_song_genres))
