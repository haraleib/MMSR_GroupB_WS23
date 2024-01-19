from math import log2
from tqdm.notebook import tqdm

from retrieval import Retrieval
from utils import unpickle_or_compute, plot_ret_sys_dict
from precision_recall import RETRIEVAL_SYSTEMS


class Ndcg:
    def __init__(self, genres):
        self._n = 10
        self._genres = genres
        self._ret = Retrieval(n=self._n)
        self._ndcgs: dict[str, float] = {}

    def get_retrieval_results(self) -> dict[str, float]:
        return self._ndcgs

    def plot(self, ret_sys_filter: list[str]) -> None:
        plot_ret_sys_dict(
            self._ndcgs,
            xlabel="nDCG@10",
            ylabel="Retrieval System",
            filter=ret_sys_filter
        )

    def compute(self) -> None:
        chunk_size = 1000
        chunks = [
            self._genres.get_song_ids()[i:i + chunk_size]
            for i in range(0, len(self._genres.get_song_ids()), chunk_size)
        ]

        print(f"Prepared {len(chunks)} chunks to compute nDCG")

        for chunk_id, chunk in enumerate(tqdm(chunks, desc=f"Computing nDCG in chunks of {chunk_size}")):
            chunk_ndcgs = unpickle_or_compute(
                f"ndcg_{self._n}_chunk_{chunk_id}.pickle",
                lambda: self._compute_chunk(chunk)
            )
            for retrieval_name, ndcg in chunk_ndcgs.items():
                self._ndcgs[retrieval_name] = self._ndcgs.get(retrieval_name, 0) + ndcg

        for retrieval_name in self._ndcgs:
            self._ndcgs[retrieval_name] /= len(self._genres.get_song_ids())

    def _compute_chunk(self, chunk):
        ndcgs = {}
        for song_id in chunk:
            idcg = self._get_idcg(song_id)

            for retrieval_name, retrieval in RETRIEVAL_SYSTEMS.items():
                retrieved = retrieval(self._ret, song_id)
                retrieved = [song_id for song_id, _ in retrieved]

                dcg = self._get_dcg(song_id, retrieved)

                # Sanity check to prevent division by 0
                ndcg = dcg / idcg if idcg != 0.0 else 0.0
                ndcgs[retrieval_name] = ndcgs.get(retrieval_name, 0) + ndcg

        return ndcgs

    def _get_idcg(self, song_id):
        all_songs = self._genres.get_song_ids().copy()
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
