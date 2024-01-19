import matplotlib.pyplot as plt
from tqdm.notebook import tqdm
from dataclasses import dataclass
from genre_coverage import GenreCoverage
from genre_diversity import GenreDiversity

from genres import Genres
from ndcg import Ndcg
from precision_recall import PrecisionRecall
from retrieval import Retrieval, RETRIEVAL_SYSTEMS
from utils import plot_ret_sys_dict


@dataclass
class CombinedEvalResult:
    precision_at_10: float
    recall_at_10: float
    f1_score_at_10: float
    ndcg_at_10: float
    genre_coverage_at_10: float
    genre_diversity_at_10: float


class CombinedScore:
    def __init__(self, genres: Genres):
        self._n = 100
        self._results: dict[str, CombinedEvalResult] = {}
        self._scores: dict[str, float] = {}

        self._genres = genres
        self._ret = Retrieval(n=self._n)

    def compute(self) -> None:
        # no pickles needed here since all other results are pickled already

        pr = PrecisionRecall(self._genres)
        pr.compute()
        precision_recall_result = pr.get_retrieval_results()

        ndcg = Ndcg(self._genres)
        ndcg.compute()
        ndcg_result = ndcg.get_retrieval_results()

        gc = GenreCoverage(self._genres)
        gc.compute()
        genre_coverage_result = gc.get_retrieval_results()

        gd = GenreDiversity(self._genres)
        gd.compute()
        genre_diversity_result = gd.get_retrieval_results()

        for ret_sys_name, ret_sys in RETRIEVAL_SYSTEMS.items():
            precision = precision_recall_result[ret_sys_name].precision_at_k[10]
            recall = precision_recall_result[ret_sys_name].recall_at_k[10]
            ndcg = ndcg_result[ret_sys_name]
            genre_coverage = genre_coverage_result[ret_sys_name]
            genre_diversity = genre_diversity_result[ret_sys_name]
            f1_score = self.f1_score(precision, recall)

            self._results[ret_sys_name] = CombinedEvalResult(
                precision_at_10=precision,
                recall_at_10=recall,
                f1_score_at_10=f1_score,
                ndcg_at_10=ndcg,
                genre_coverage_at_10=genre_coverage,
                genre_diversity_at_10=genre_diversity,
            )

        sorted_by_f1 = sorted(self._results.items(), key=lambda x: x[1].f1_score_at_10, reverse=True)
        sorted_by_ndcg = sorted(self._results.items(), key=lambda x: x[1].ndcg_at_10, reverse=True)
        sorted_by_genre_coverage = sorted(self._results.items(), key=lambda x: x[1].genre_coverage_at_10, reverse=True)
        sorted_by_genre_diversity = sorted(self._results.items(), key=lambda x: x[1].genre_diversity_at_10, reverse=True)

        # compute the average position of each retrieval system in each of the sorted lists and average them
        self._scores = {}
        for ret_sys_name, _ in RETRIEVAL_SYSTEMS.items():
            # TODO: order ascending/descending depending on the metric
            f1 = sorted_by_f1.index((ret_sys_name, self._results[ret_sys_name])) + 1
            ndcg = sorted_by_ndcg.index((ret_sys_name, self._results[ret_sys_name])) + 1
            genre_coverage = sorted_by_genre_coverage.index((ret_sys_name, self._results[ret_sys_name])) + 1
            genre_diversity = sorted_by_genre_diversity.index((ret_sys_name, self._results[ret_sys_name])) + 1
            self._scores[ret_sys_name] = (f1 + ndcg + genre_coverage + genre_diversity) / 4

    def f1_score(self, precision: float, recall: float) -> float:
        return 2 * (precision * recall) / (precision + recall)

    def plot(self, ret_sys_filter: list[str]) -> None:
        plot_ret_sys_dict(
            ret_sys_dict=self._scores,
            xlabel="Combined Score@10",
            ylabel="Retrieval System",
            filter=ret_sys_filter
        )
