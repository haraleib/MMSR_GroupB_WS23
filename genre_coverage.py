from tqdm.notebook import tqdm

from genres import Genres
from retrieval import Retrieval, RETRIEVAL_SYSTEMS
from utils import unpickle_or_compute, plot_ret_sys_dict


class GenreCoverage:
    def __init__(self, genres: Genres):
        self.n = 10
        self.ratio: dict[str, float] = {}

        self.genres = genres
        self.retrieval = Retrieval(n=self.n)

    def get_retrieval_results(self) -> dict[str, float]:
        return self.ratio

    def _compute_coverage_ratio(self, ret_sys, ret_sys_name: str) -> float:
        all_unique_genres = set()
        for genre in self.genres.song_genre_map.values():
            all_unique_genres.update(genre)

        n_total_unique_genres = len(all_unique_genres)

        # Initialize a set to keep track of unique genres for this retrieval system
        unique_genres_for_ret_sys = set()

        # Iterate through all song IDs
        for song_id in tqdm(self.genres.get_song_ids(), desc=f"Iterating songs for '{ret_sys_name}'", leave=False):
            top_10_songs = ret_sys(self.retrieval, song_id)
            top_10_songs = [song_id for song_id, _ in top_10_songs]

            # Iterate through the top 10 tracks and add their genres to the set
            for retrieved_idx in top_10_songs:
                unique_genres_for_ret_sys.update(self.genres.song_genre_map[retrieved_idx])

        # Calculate the genre coverage for this retrieval system
        return len(unique_genres_for_ret_sys) / n_total_unique_genres

    def compute(self) -> None:
        self.ratio = {}

        for ret_sys_name, ret_sys in RETRIEVAL_SYSTEMS.items():
            self.ratio[ret_sys_name] = unpickle_or_compute(
                f"genre_coverage_{ret_sys_name}.pickle",
                lambda: self._compute_coverage_ratio(ret_sys, ret_sys_name)
            )

    def plot(self, ret_sys_filter: list[str]) -> None:
        plot_ret_sys_dict(
            ret_sys_dict=self.ratio,
            xlabel="Genre Coverage@10",
            ylabel="Retrieval System",
            filter=ret_sys_filter
        )
