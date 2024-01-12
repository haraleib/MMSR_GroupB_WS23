<script lang="ts">
    import Pagination from "./Pagination.svelte";
import type { Song } from "./song";

    export let songs: Song[] = [];

    let currentPage = 1;
    let pageSize = 20;

    $: visibleSongs = songs.slice((currentPage - 1) * pageSize, currentPage * pageSize);

    // Prevent currentPage from being greater than the last page
    $: if (currentPage > Math.ceil(songs.length / pageSize)) {
        currentPage = Math.ceil(songs.length / pageSize);
    }
</script>

<ul>
    {#key songs.length}
        <Pagination itemCount={songs.length} bind:currentPage {pageSize} />
    {/key}

    {#each visibleSongs as song}
        <li>
            {song.song} - {song.artist} - {song.genres}
            <a href="/song/{song.id}">View</a>
            <a href="https://youtu.be/{song.ytId}" target="_blank">YouTube</a>
            {#if song.score}
                <span>Score: {song.score}</span>
            {/if}
        </li>
    {/each}
</ul>
