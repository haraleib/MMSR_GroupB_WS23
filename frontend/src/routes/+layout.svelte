<script lang="ts">
  import "../app.css";

  import FilteredSongList from "$lib/FilteredSongList.svelte";
  import type { LayoutData } from "./$types";

  let query = "";

  export let data: LayoutData;
</script>

<div class="flex items-center justify-center w-full h-16 bg-gray-100">
  <div class="relative w-full max-w-3xl px-6 py-3 text-gray-600">
    <input
      type="search"
      name="search"
      placeholder="Search"
      class="w-full h-10 px-5 pr-10 text-sm bg-white border-2 border-gray-300 rounded-full focus:outline-none"
      bind:value={query}
    />
    <div class="absolute top-0 right-0 mt-3 mr-4">
      <svg class="w-8" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"
        ><title>magnify</title><path
          fill="currentColor"
          d="M9.5,3A6.5,6.5 0 0,1 16,9.5C16,11.11 15.41,12.59 14.44,13.73L14.71,14H15.5L20.5,19L19,20.5L14,15.5V14.71L13.73,14.44C12.59,15.41 11.11,16 9.5,16A6.5,6.5 0 0,1 3,9.5A6.5,6.5 0 0,1 9.5,3M9.5,5C7,5 5,7 5,9.5C5,12 7,14 9.5,14C12,14 14,12 14,9.5C14,7 12,5 9.5,5Z"
        /></svg
      >
    </div>
  </div>
</div>

<div class="flex flex-row h-full">
  <div class="flex flex-col flex-1 h-full overflow-y-auto">
    <FilteredSongList songs={data.props.songs} {query} />
  </div>
  <div class="flex flex-col flex-1 h-full overflow-y-auto">
    <slot />
  </div>
</div>
