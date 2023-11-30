from song import songs
from datasets import datasets
import json
from utils import unpickle_or_compute


class Genres():
    """Precomputes some data for the analysis and caches it on disk."""
    def __init__(self) -> None:
        data = unpickle_or_compute("precomputed_genres.pickle", lambda: self._compute_data())
        self.song_genre_map = data['song_genre_map']
        self.song_ids = data['song_ids']
        self.relevant_song_counts = data['relevant_song_counts']

    def get_song_genre(self, song_id):
        return self.song_genre_map.get(song_id, None)

    def get_song_ids_with_genre_info(self):
        return self.song_ids
    
    def get_relevant_song_counts(self, song_id):
        return self.relevant_song_counts.get(song_id, 0)

    def song_is_relevant(self, song_a, song_b):
        if song_a not in self.song_genre_map:
            return False
        if song_b not in self.song_genre_map:
            return False
        return self._is_relevant(song_a, song_b, self.song_genre_map)

    def _compute_data(self):
        genre = self._get_song_genre_map()
        ids = list(genre.keys())
        return {
            'song_genre_map': genre,
            'song_ids': ids,
            'relevant_song_counts': self._get_relevant_song_counts(ids, genre)
        }

    def _get_song_genre(self, song_id):
        genre_df = datasets.get_dataset("genres")
        try:
            genre = genre_df[genre_df["id"] == song_id].iloc[0]["genre"]
            # non standard json -> uses ' instead of "
            genre = genre.replace("'", "\"")
            genre = json.loads(genre)
            return genre
        except json.JSONDecodeError as e:
            print(e)
            print(f"Could not decode genre for song {song_id}")
        except IndexError as e:
            print(f"Could not find genre for song {song_id}")
        return None

    def _get_song_genre_map(self):
        song_genre_map = {}
        for song in songs.info["id"]:
            genre = self._get_song_genre(song)
            if genre is None:
                continue
            song_genre_map[song] = genre
        print(f"Found {len(song_genre_map)} songs with genre information")

        return song_genre_map

    # def _get_relevant_song_map(self):
    #     relevant_song_map = {}
    #     for song in self.song_ids:
    #         for other_song in self.song_ids:
    #             if song == other_song:
    #                 continue
    #             canonical_id = self._get_canonical_song_pair_id(song, other_song)
    #             if canonical_id in relevant_song_map:
    #                 continue
    #             genre_a = set(self.song_genre_map[song])
    #             genre_b = set(self.song_genre_map[other_song])
    #             relevant_song_map[canonical_id] = len(genre_a.intersection(genre_b)) > 0
    #             del genre_a
    #             del genre_b
    #     print(f"Found {len(relevant_song_map)} relevant song pairs")
    #     return relevant_song_map

    def _get_canonical_song_pair_id(self, song_a, song_b):
        return "".join(sorted([song_a, song_b]))

    def _get_relevant_song_counts(self, song_ids, song_genre_map):
        relevant_song_counts = {}
        i = 0
        for song in song_ids:
            relevant_song_counts[song] = sum([1 for other_song in song_ids if self._is_relevant(song, other_song, song_genre_map)])
            i += 1
            if i % 100 == 0:
                print(f"Processed {i} song relevances")
        return relevant_song_counts

    def _is_relevant(self, song_a, song_b, song_genre_map):
        for genre_a in song_genre_map[song_a]:
            for genre_b in song_genre_map[song_b]:
                if genre_a == genre_b:
                    return True
        return False
