<script lang="ts">
    import Pagination from "./Pagination.svelte";
    import SongCard from "./SongCard.svelte";

    export let imageClassName = "max-h-24";
    export let songs: Song[] = [];

    let currentPage = 1;
    let pageSize = 24;
    let visibleSongs: Song[] = []

    // Prevent currentPage from being greater than the last page
    $: {
      if (currentPage > Math.ceil(songs.length / pageSize)) {
        currentPage = Math.ceil(songs.length / pageSize);
      }
      if (currentPage < 1) {
        currentPage = 1;
      }
      visibleSongs = songs.slice((currentPage - 1) * pageSize, currentPage * pageSize);
    }
</script>

<div class="mx-auto">
    {#key songs.length}
        <Pagination itemCount={songs.length} bind:currentPage {pageSize} />
    {/key}
    <div class="flex flex-col gap-y-2">
        {#each visibleSongs as song}
            <SongCard {song} {imageClassName} />
        {/each}
    </div>
    {#key songs.length}
        <Pagination itemCount={songs.length} bind:currentPage {pageSize} />
    {/key}
</div>
