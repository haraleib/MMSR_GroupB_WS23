<script lang="ts">
  import "../app.css";

  import FilteredSongList from "$lib/FilteredSongList.svelte";
  import type { LayoutData } from "./$types";

  let query = "";

  // TODO: Add transitions/animations?
  export let data: LayoutData;
</script>

<div class="flex flex-row h-full pt-8 pb-16 px-8">
  <div class="relative w-full max-w-3xl px-6 text-gray-600">
      <input
        type="search"
        name="search"
        placeholder="Search"
        class="w-full shadow outline-none focus:ring focus:ring-magnum-400 focus:border-magnum-400"
        bind:value={query}
      />

    <FilteredSongList songs={data.props.songs} {query} />
  </div>
  <div class="flex flex-col px-8">
    <slot />
  </div>
</div>

<style lang="postcss">
  input {
    height: theme(spacing.10);
    flex-shrink: 0;
    flex-grow: 1;
    border-radius: theme(borderRadius.xl);
    border: 1px solid theme(colors.gray.300);
    padding-inline: theme(spacing[2.5]);
    line-height: 1;
    color: theme(colors.neutral.900);
  }
</style>
