<script lang="ts">
    import SongList from "./SongList.svelte";
    import type { Song } from "./song";

    export let songs: Song[] = [];
    export let query: string = "";

    let filteredSongs: Song[] = [];

    function filterSongs(songs: Song[], query: string) {
        if (query.trim() === "") {
            filteredSongs = songs;
        } else {
            console.log("filtering");
            const lowercaseQuery = query.toLowerCase();
            filteredSongs = songs.filter((song) => {
                const lowercaseTitle = song.song.toLowerCase();
                const lowercaseArtist = song.artist.toLowerCase();
                const lowercaseAlbum = song.genres.join(" ").toLowerCase();
                return (
                    lowercaseTitle.includes(lowercaseQuery) ||
                    lowercaseArtist.includes(lowercaseQuery) ||
                    lowercaseAlbum.includes(lowercaseQuery)
                );
            });
        }
    }

    $: filterSongs(songs, query);
</script>

<div>
    <SongList songs={filteredSongs} />
</div>
