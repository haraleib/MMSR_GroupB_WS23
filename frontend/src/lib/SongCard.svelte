<script lang="ts">
    import { cx } from "$lib";
    import TagContainer from "./TagContainer.svelte";

    export let song: Song;
    export let vertical = false;
    export let imageClassName = "max-h-40";
</script>

<a
  class={cx(
    "flex bg-white border shadow-sm rounded-xl cursor-pointer transition-all hover:relative hover:z-10 duration-300 hover:scale-[105%] hover:shadow-xl",
    vertical ? "flex-col" : "flex-row"
  )}
  href="/song/{song.id}"
>
  <img
    class={cx(imageClassName, vertical ? "rounded-t-xl" : "rounded-l-xl")}
    src="https://img.youtube.com/vi/{song.ytId}/hqdefault.jpg"
    alt="Preview image for song [{song.song}] by [{song.artist}]"
  />

  <div class={cx("flex flex-col justify-between py-3 h-full", vertical ? "px-4 gap-y-2" : "pl-4 pr-8")}>
    <div class="flex flex-col">
      <h3 class="text-xl font-bold leading-5 tracking-tight text-gray-800">
        {song.song}
      </h3>
      <p class="text-lg font-medium text-gray-500 tracking-tight">
        {song.artist}
      </p>
    </div>

    <div>
      {#if song.score}
        <p class="text-base tracking-3 text-gray-500 mb-0.5">
          Similarity: <span class="font-bold text-gray-900">{Math.round(song.score * 100)}%</span>
        </p>
      {/if}
      <TagContainer genres={song.genres} />
    </div>
  </div>
</a>
