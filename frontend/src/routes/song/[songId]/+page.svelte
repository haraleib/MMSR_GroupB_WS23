<script lang="ts">
    import SongList from "$lib/SongList.svelte";
    import type { PageData } from "./$types";

    export let data: PageData;

    let selectedResultType = "random";

    $: resultTypes = Object.keys(data.results);
</script>

<main>
    <h1>{data.song.song}</h1>
    <p>{data.song.artist}</p>
    <p>{data.song.id}</p>
    <p>
        <a href="https://youtu.be/{data.song.ytId}" target="_blank">YouTube</a>
    </p>

    <select bind:value={selectedResultType} class="bg-slate-700">
        {#each resultTypes as resultType}
            <option value={resultType}>{resultType}</option>
        {/each}
    </select>

    <h2>Related Songs ({selectedResultType})</h2>
    <SongList songs={data.results[selectedResultType]} />

    <h2>YouTube Embed</h2>
    <iframe
        width="560"
        height="315"
        src="https://www.youtube-nocookie.com/embed/{data.song.ytId}"
        title="YouTube video player"
        frameborder="0"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
        allowfullscreen
    ></iframe>
</main>

<style>
    main {
        padding: 20px;
    }
</style>
