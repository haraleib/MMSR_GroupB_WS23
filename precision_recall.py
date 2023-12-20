import matplotlib.pyplot as plt
from tqdm.notebook import tqdm
from dataclasses import dataclass

from genres import Genres
from utils import unpickle_or_compute
from retrieval import Retrieval, RETRIEVAL_SYSTEMS


@dataclass
class RetrievalEvalResult:
    n: int
    precision_at_k: dict[int, float]
    recall_at_k: dict[int, float]


class PrecisionRecall:
    DISTINCT_COLORS = {
        "random_baseline": "tab:cyan",
        "text_tf_idf": "tab:blue",
        "text_bert": "tab:green",
        "text_word2vec": "tab:red",
        "mfcc_bow": "tab:purple",
        "blf_correlation": "tab:pink",
        "ivec256": "tab:orange",
        "musicnn": "black",
        "video_resnet": "tab:brown",
        # "late_fusion": "tab:olive",
        # "early_fusion": "tab:gray",
    }

    def __init__(self, genres: Genres):
        self._n = 100
        self._results: dict[str, RetrievalEvalResult] = {}

        self._genres = genres
        self._ret = Retrieval(n=self._n)

    def compute(self) -> None:
        # calculate average precision and recall @ k across all tracks for each retrieval method
        # plot precision and recall @ k for each retrieval method
        for ret_sys_name, ret_sys in RETRIEVAL_SYSTEMS.items():
            print(f"Calculating precision and recall for {ret_sys_name}")

            precision_at_k, recall_at_k = unpickle_or_compute(
                f"precision_recall_{ret_sys_name}.pickle",
                lambda: self._calculate_precision_recall(ret_sys, ret_sys_name)
            )

            self._results[ret_sys_name] = RetrievalEvalResult(
                n=self._n,
                precision_at_k=precision_at_k,
                recall_at_k=recall_at_k
            )

    def plot_all_single(self) -> None:
        fig, ax = plt.subplots(figsize=(14, 7), dpi=200)

        for name, results in self._results.items():
            x, y = [], []
            for k in range(1, results.n + 1):
                x.append(results.recall_at_k[k])
                y.append(results.precision_at_k[k])

            ax.plot(x, y, label=name, zorder=3, color=self.DISTINCT_COLORS[name])

        ax.grid(which="major", color="lightgrey", ls=":", lw=1)
        ax.grid(which="minor", color="lightgrey", ls=":", lw=0.5, alpha=0.8)

        ax.minorticks_on()

        def format_func(value, tick_number):
            return f"{value:.4f}".rstrip("0").rstrip(".")

        ax.xaxis.set_major_formatter(plt.FuncFormatter(format_func))

        ax.set_xlabel("Recall")
        ax.set_ylabel("Precision")
        ax.set_xlim(0, 0.02)
        ax.set_ylim(0, 0.71)
        ax.set_title(f"Precision-Recall Curves across all Retrieval Systems")

        plt.legend(loc="best")
        plt.show()

    def plot_each(self) -> None:
        fig, axes = plt.subplots(nrows=5, ncols=2, figsize=(12, 14), dpi=200)
        axes = axes.flatten()

        for i, (name, results) in enumerate(self._results.items()):
            x, y = [], []
            for k in range(1, results.n + 1):
                x.append(results.recall_at_k[k])
                y.append(results.precision_at_k[k])

            ax = axes[i]
            ax.plot(x, y, label=name, zorder=3, color=self.DISTINCT_COLORS[name])

            ax.grid(which="major", color="lightgrey", ls=":", lw=1)
            ax.grid(which="minor", color="lightgrey", ls=":", lw=0.5, alpha=0.8)

            ax.minorticks_on()

            def format_func(value, tick_number):
                return f"{value:.4f}".rstrip("0").rstrip(".")

            ax.xaxis.set_major_formatter(plt.FuncFormatter(format_func))
            ax.set_xlim(0, 0.02)
            ax.set_ylim(0, 0.71)
            ax.set_title(f"{name}")

        suptitle = fig.suptitle("Precision-Recall Curve for each Retrieval System", fontsize=16)
        suptitle.set_y(0.995)

        fig.supxlabel("Recall", fontsize=16)
        fig.supylabel("Precision", fontsize=16)

        plt.legend(loc="best")
        plt.tight_layout()
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
            retrieved_songs = [song_id for song_id, _ in retrieved_songs]

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
        
