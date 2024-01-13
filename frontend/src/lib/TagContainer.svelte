<script lang="ts">
    import Tag from "./Tag.svelte";

    export let genres: string[];

    const popularGenres = [
      "rock", "hip hop", "rap", "pop", "techno", "jazz"
    ];

    function filterGenres() {
      let res = [...genres];
      res.sort((a, b) => {
        if (a.length < b.length) {
          return -1;
        } else if (a.length > b.length) {
          return 1;
        } else {
          return a.localeCompare(b);
        }
      });
      res.sort((a, b) => popularGenres.includes(a) ? -1 : 0);

      // allow only first 5 short tags (<= 12 characters)
      let i = 0;
      for (; i < Math.min(res.length, 5); ++i) {
        if (res[i].length > 12) {
          break;
        }
      }

      return res.slice(0, i);
    }

    $: filteredGenres = filterGenres();
</script>

<div class="flex flex-wrap gap-x-1 gap-y-1">
  {#each filteredGenres as genre}
    <Tag label={genre} />
  {/each}
</div>


