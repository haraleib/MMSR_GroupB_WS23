from typing import Tuple, Optional
from dataclasses import dataclass

from datasets import datasets


@dataclass
class Song:
    title: str
    artist: str


class SongTable:
    def __init__(self):
        self.info = datasets.information.df

    def get_match(self, song: Song) -> Optional[Tuple[Song, int]]:
        matches = self.info[
            (self.info["song"] == song.title) &
            (self.info["artist"] == song.artist)
        ]

        if len(matches) != 1:
            print("Query must match *exactly* 1 song, but matched the following song(s):")
            print(matches)
            return None
        else:
            return song, matches.iloc[0]["id"]

    def prompt_song_query(self) -> Tuple[Song, int]:
        """
        Ask user for input and try to match it to a song in our dataset.
        :return: A tuple containing the relevant Song object and the song (row) id.
        """
        while True:
            # Allow the user to input the song title and artist name
            song_title = input("Enter the song title: ")
            artist_name = input("Enter the artist name: ")

            match = self.get_match(Song(song_title, artist_name))
            if match is not None:
                return match
            else:
                continue


songs = SongTable()
