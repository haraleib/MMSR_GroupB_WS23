<script lang="ts">
    import type { Song } from "./song";

    export let songs: Song[] = [];
</script>

<ul>
    {#each songs as song}
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
