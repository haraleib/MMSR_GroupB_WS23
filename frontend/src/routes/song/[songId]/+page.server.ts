import type { PageServerLoad } from "./$types";

import { metadata, retrievals } from "$lib/server/songs";

const getRandomSongs = (count: number) => {
  const shuffledSongs = [...metadata].sort(() => 0.5 - Math.random());
  return shuffledSongs.slice(0, count);
};

export const load: PageServerLoad = async ({ params }) => {
  const { songId } = params;

  const song = metadata.find((song) => song.id === songId);
  if (!song) {
    throw new Error(`Song with id ${songId} not found`);
  }

  const results: Record<string, Song[]> = {
    random: getRandomSongs(10),
  };

  for (const [retrivalName, songs] of Object.entries(retrievals)) {
    const retrieved = songs[song.id];
    if (!retrieved) {
      console.log(`No results for ${retrivalName}`);
      continue;
    }

    results[retrivalName] = retrieved.slice(0, 10).map(([id, score]) => {
      const song = metadata.find((song) => song.id === id);
      if (!song) {
        throw new Error(`Song with id ${id} not found`);
      }
      return { ...song, score };
    });
  }

  return { song, results };
};
