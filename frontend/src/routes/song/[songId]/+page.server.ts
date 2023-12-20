import type { Song } from '$lib/song';
import type { PageServerLoad } from './$types';
import { promises as fsPromises } from 'fs';

interface Retrieval {
    [key: string]: [string, number][];
};

const getRetrievals = async (dir: string) => {
    const files = await fsPromises.readdir(dir);
    const map: Record<string, Retrieval> = {};
    try {
        for (const file of files) {
            const content = await fsPromises.readFile(`${dir}/${file}`, 'utf-8');
            map[file] = JSON.parse(content);
        }
    } catch (e) {
        console.log(e);
    }
    return map;
}

const retrievals = await getRetrievals('/workspaces/MMSR_GroupB_WS23/retrievals');

export const load: PageServerLoad = async ({ params }) => {
    const { songId } = params;

    const songMetaPath = '/workspaces/MMSR_GroupB_WS23/frontend/static/songMeta.json';
    const songMetaContent = await fsPromises.readFile(songMetaPath, 'utf-8');
    const songMeta: Song[] = JSON.parse(songMetaContent);

    const song = songMeta.find((song) => song.id === songId);

    if (!song) {
        throw new Error(`Song with id ${songId} not found`);
    }

    const results: Record<string, Song[]> = {
        random: getRandomSongs(songMeta, 10),
    };

    for (const [retrivalName, songs] of Object.entries(retrievals)) {
        const songResult = songs[song.id];
        if (!songResult) {
            console.log(`No results for ${retrivalName}`);
            continue;
        }
        results[retrivalName] = songResult.slice(0, 10).map(([id, score]) => {
            const song = songMeta.find((song) => song.id === id);
            if (!song) {
                throw new Error(`Song with id ${id} not found`);
            }
            return { ...song, score };
        })
    }

    return { song, results };
};

const getRandomSongs = (songs: Song[], count: number) => {
    const shuffledSongs = songs.sort(() => 0.5 - Math.random());
    return shuffledSongs.slice(0, count);
}
