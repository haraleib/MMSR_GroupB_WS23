<script lang="ts">
  import SongList from "./SongList.svelte";

  export let songs: Song[];
  export let query: string;

  // TODO: Add fuzzy search?
  let filteredSongs: Song[] = [];

  $: {
    const searchText = query.trim().toLowerCase();

    if (!searchText.length) {
      filteredSongs = songs;
    } else {
      filteredSongs = songs.filter((s) => {
        const title = s.song.toLowerCase();
        const artist = s.artist.toLowerCase();
        const album = s.genres.join(" ").toLowerCase();
        return (
          title.includes(searchText) ||
          artist.includes(searchText) ||
          album.includes(searchText)
        );
      });
    }
  }
</script>

<SongList songs={filteredSongs} />
