import matplotlib.pyplot as plt
from tqdm.notebook import tqdm
from dataclasses import dataclass

from genres import Genres
from utils import unpickle_or_compute
from retrieval import Retrieval, RETRIEVAL_SYSTEMS


@dataclass
class RetrievalEvalResult:
    n: int
    name: str
    precision_at_k: dict[int, float]
    recall_at_k: dict[int, float]


class PrecisionRecall:
    def __init__(self, genres: Genres):
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
        _ = plt.figure(figsize=(14, 7), dpi=200)

        distinct_colors = [
            "tab:cyan", "tab:blue", "tab:green", "tab:red", "tab:purple", "tab:pink", "tab:orange", "black"
        ]
        for i, res in enumerate(self._results):
            x, y = [], []
            for k in range(1, res.n + 1):
                x.append(res.recall_at_k[k])
                y.append(res.precision_at_k[k])

            plt.plot(x, y, label=res.name, zorder=3, color=distinct_colors[i])

        plt.grid(which="major", color="lightgrey", ls=":", lw=1)
        plt.grid(which="minor", color="lightgrey", ls=":", lw=0.5, alpha=0.8)

        plt.minorticks_on()

        def format_func(value, tick_number):
            return f"{value:.4f}".rstrip("0").rstrip(".")

        plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(format_func))

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
            n_relevant_songs = self._genres.get_relevant_song_counts(song_id)

            retrieved_songs = ret_sys(self._ret, song_id)
            retrieved_songs = list(retrieved_songs["id"])

            relevant_until_k = 0.0
            for k in range(1, self._n + 1):
                if self._genres.is_related(song_id, retrieved_songs[k - 1]):
                    relevant_until_k += 1.0
                
                precision_at_k[k] = precision_at_k.get(k, 0.0) + relevant_until_k / k

                # Sanity check: Prevent division by 0
                recall = recall_at_k.get(k, 0.0)
                if n_relevant_songs:
                    recall += relevant_until_k / n_relevant_songs

                recall_at_k[k] = recall

        n_songs = len(self._genres.get_song_ids())

        # calculate average precision and recall @ k across all tracks
        for k in range(1, self._n + 1):
            precision_at_k[k] /= n_songs
            recall_at_k[k] /= n_songs
        
        return precision_at_k, recall_at_k
        
