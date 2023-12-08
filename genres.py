import json
from typing import Optional
from tqdm.notebook import tqdm

from datasets import datasets
from utils import unpickle_or_compute


class Genres:
    """Precomputes some data for the analysis and caches it on disk."""
    def __init__(self) -> None:
        data = unpickle_or_compute("precomputed_genres.pickle", lambda: self._compute_data())

        self.song_ids: list[int] = data['song_ids']
        self.song_genre_map: dict[int, set[str]] = data['song_genre_map']
        self.relevant_song_counts: dict[int, int] = data['relevant_song_counts']

    def get_song_genre(self, song_id: int) -> Optional[set[str]]:
        return self.song_genre_map.get(song_id, None)

    def get_song_ids(self) -> list[int]:
        return self.song_ids
    
    def get_relevant_song_counts(self, song_id) -> int:
        return self.relevant_song_counts.get(song_id, 0)

    def _compute_data(self):
        self.song_genre_map = self._get_song_genre_map()
        self.song_ids = list(self.song_genre_map.keys())
        self.relevant_song_counts = self._get_relevant_song_counts()

        return {
            'song_ids': self.song_ids,
            'song_genre_map': self.song_genre_map,
            'relevant_song_counts': self.relevant_song_counts
        }

    def _get_song_genre_map(self) -> dict[int, set[str]]:
        song_genre_map: dict[int, set[str]] = {}
        for _, row in datasets.genres.df.iterrows():
            genre = row["genre"].replace("'", "\"")
            song_genre_map[row["id"]] = set(json.loads(genre))

        print(f"Found {len(song_genre_map)} songs with genre information")
        return song_genre_map

    def _get_relevant_song_counts(self) -> dict[int, int]:
        relevant_song_counts = {}

        for song in tqdm(self.song_ids, "Computing number of relevant songs"):
            relevant_song_counts[song] = sum([
                1 for other_song in self.song_ids
                if self.is_related(song, other_song) and song != other_song
            ])

        return relevant_song_counts

    def is_related(self, song_a: int, song_b: int) -> int:
        # Check whether two sets intersect and by how many elements
        return len(self.song_genre_map[song_a] & self.song_genre_map[song_b])
