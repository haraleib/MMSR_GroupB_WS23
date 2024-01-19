import numpy as np
from tqdm.notebook import tqdm

from genres import Genres
from retrieval import Retrieval, RETRIEVAL_SYSTEMS
from utils import unpickle_or_compute, plot_ret_sys_dict


class GenreDiversity:
    def __init__(self, genres: Genres, retrieval: Retrieval = None):
        self.n = 10
        self.diversity: dict[str, float] = {}

        self.genres = genres
        self.retrieval = retrieval if retrieval else Retrieval(n=self.n)

    def get_retrieval_results(self) -> dict[str, float]:
        return self.diversity

    def _compute_diversity(self, ret_sys, ret_sys_name: str) -> float:
        all_unique_genres = set()
        for genre in self.genres.song_genre_map.values():
            all_unique_genres.update(genre)

        n_total_genres = len(all_unique_genres)

        # Compute a unique genre-to-index mapping in order
        # to compute the genre distribution hassle-free
        genre_to_idx = {genre: idx for idx, genre in enumerate(all_unique_genres)}

        # Iterate through all song IDs
        entropy_list: list[float] = []

        for song_id in tqdm(self.genres.get_song_ids(), desc=f"Iterating songs for '{ret_sys_name}'", leave=False):
            top_10_songs = ret_sys(self.retrieval, song_id)
            top_10_songs = [song_id for song_id, _ in top_10_songs]

            # Iterate through the top 10 tracks and compute their respective genre distribution
            distribution = np.zeros(shape=(n_total_genres,))
            for retrieved_idx in top_10_songs:
                song_genres = self.genres.song_genre_map[retrieved_idx]
                n_song_genres = len(song_genres)

                # Update/accumulate genre frequency
                for song_genre in song_genres:
                    distribution[genre_to_idx[song_genre]] += 1.0 / n_song_genres

            # Normalize the distribution by dividing it with the number of top-K entries
            # (relative frequencies against top-K)
            distribution /= len(top_10_songs)

            # Measure diversity by applying Shannon's entropy formula to the distribution
            # (Entropy will be higher if the genres are distributed more evenly
            # and lower if they are concentrated in a few genres.)
            entropy = 0.0
            for p in distribution:
                if p > 0.0:
                    entropy -= p * np.log2(p)

            entropy_list.append(entropy)

        # Calculate the mean genre diversity for this retrieval system
        return sum(entropy_list) / len(entropy_list)

    def compute(self) -> None:
        self.diversity = {}

        for ret_sys_name, ret_sys in RETRIEVAL_SYSTEMS.items():
            self.diversity[ret_sys_name] = unpickle_or_compute(
                f"genre_diversity_{ret_sys_name}.pickle",
                lambda: self._compute_diversity(ret_sys, ret_sys_name)
            )

    def plot(self, ret_sys_filter: list[str]) -> None:
        plot_ret_sys_dict(
            ret_sys_dict=self.diversity,
            xlabel="Genre Diversity@10",
            ylabel="Retrieval System",
            filter=ret_sys_filter
        )
