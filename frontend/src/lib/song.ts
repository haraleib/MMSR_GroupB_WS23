export interface Song {
    id: string;
    artist: string;
    song: string;
    ytId: string;
    genres: string[];

    score?: number;
}
