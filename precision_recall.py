import matplotlib.pyplot as plt
from tqdm.notebook import tqdm
from dataclasses import dataclass

from genres import Genres
from datasets import datasets
from utils import unpickle_or_compute
from retrieval import Retrieval, SimilarityMeasure

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


@dataclass
class RetrievalEvalResult:
    n: int
    name: str
    precision_at_k: dict[int, float]
    recall_at_k: dict[int, float]


class PrecisionRecall:
    def __init__(self, genres):
        self._n = 100
        self._results: list[RetrievalEvalResult] = []

        self._genres = genres
        self._ret = Retrieval(n=self._n)

    def compute(self) -> None:
        self._results = []

        # calculate average precision and recall @ k across all tracks for each retrieval method
        # plot precision and recall @ k for each retrieval method
        for ret_sys_name, ret_sys in RETRIEVAL_SYSTEMS.items():
            print(f"Calculating precision and recall for {ret_sys_name}")

            precision_at_k, recall_at_k = unpickle_or_compute(
                f"precision_recall_{ret_sys_name}.pickle",
                lambda: self._calculate_precision_recall(ret_sys, ret_sys_name)
            )

            self._results.append(RetrievalEvalResult(
                n=self._n,
                name=ret_sys_name,
                precision_at_k=precision_at_k,
                recall_at_k=recall_at_k
            ))

    def plot(self) -> None:
        for res in self._results:
            x, y = [], []
            for k in range(1, res.n + 1):
                x.append(res.recall_at_k[k])
                y.append(res.precision_at_k[k])

            plt.plot(x, y, label=res.name)

        plt.xlabel("Recall")
        plt.ylabel("Precision")
        plt.xlim(0, 0.02)
        plt.ylim(0, 1)
        plt.title("Precision-Recall Curve")
        plt.legend()
        plt.show()

    def _calculate_precision_recall(self, ret_sys, ret_sys_name) -> tuple[dict[int, float], dict[int, float]]:
        precision_at_k: dict[int, float] = {}
        recall_at_k: dict[int, float] = {}

        for song_id in tqdm(
                self._genres.get_song_ids(),
                desc=f"Calculating precision recall: {ret_sys_name}"
        ):
            retrieved_songs = ret_sys(self._ret, song_id)
            retrieved_songs = list(retrieved_songs["id"])

            n_relevant_songs = self._genres.get_relevant_song_counts(song_id)

            relevant_until_k = 0
            for k in range(1, self._n + 1):
                if self._genres.is_related(song_id, retrieved_songs[k - 1]):
                    relevant_until_k += 1
                
                precision_at_k[k] = precision_at_k.get(k, 0) + relevant_until_k / k

                # Sanity check: Prevent division by 0
                recall = recall_at_k.get(k, 0)
                if n_relevant_songs:
                    recall += relevant_until_k / n_relevant_songs

                recall_at_k[k] = recall

        n_songs = len(self._genres.get_song_ids())

        # calculate average precision and recall @ k across all tracks
        for k in range(1, self._n + 1):
            precision_at_k[k] /= n_songs
            recall_at_k[k] /= n_songs
        
        return precision_at_k, recall_at_k
        
