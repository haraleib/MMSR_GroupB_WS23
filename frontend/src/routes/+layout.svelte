<script lang="ts">
  import "../app.css";

  import { createPopover, melt } from '@melt-ui/svelte';
  import { fade } from 'svelte/transition';
  import { X } from 'lucide-svelte';

  import Tag from "$lib/Tag.svelte";

  import FilteredSongList from "$lib/FilteredSongList.svelte";
  import Informative from "$lib/icons/informative.svelte";

  import type { LayoutData } from "./$types";

  let query = "";

  const {
    elements: { trigger, content, arrow, close },
    states: { open },
  } = createPopover({
    forceVisible: true,
    closeOnOutsideClick: true
  });

  // TODO: Add transitions/animations?
  export let data: LayoutData;
</script>

<div class="flex flex-row h-full pt-8 pb-16 px-8">
  <div class="relative w-full max-w-2xl uhd:max-w-3xl px-6 text-gray-600">
    <div class="flex flex-col w-full gap-y-1">
      <input
        type="search"
        name="search"
        placeholder="Search"
        class="w-full shadow outline-none transition-all duration-300 hover:scale-[101%] hover:ring hover:ring-magnum-200 focus:ring-[5px] focus:ring-magnum-400 focus:border-magnum-400"
        bind:value={query}
      />
      <p
        class="flex self-end flex-row gap-x-1 items-center group cursor-pointer font-medium text-gray-700"
        use:melt={$trigger}
      >
        <Informative className="w-4 h-4 fill-gray-700 group-hover:fill-gray-900 transition-all duration-100" />
        <span class="underline underline-offset-1 decoration-gray-300 group-hover:text-gray-900 group-hover:decoration-gray-900 transition-all duration-100">
          Find out how the User Interface functions.
        </span>
      </p>
    </div>

    {#if $open}
      <div
        use:melt={$content}
        transition:fade={{ duration: 100 }}
        class="content"
      >
        <div use:melt={$arrow} />
        <div class="flex flex-col gap-4">
          <div>
            <h1 class="text-lg font-bold tracking-tight">Search</h1>
            <p>
              Search is possible across three distinct fields:
              <span class="font-bold">song title</span>,
              <span class="font-bold">artist name</span> and <span class="font-bold">genres</span>.
              The search is performed by searching for the query inside each of the mentioned fields (needle-in-a-haystack approach).
            </p>
          </div>
          <div>
            <h1 class="text-lg font-bold tracking-tight">Similarity score</h1>
            <p>
              The Similarity Score is shown on all related results and <span class="font-bold">only</span>
              when the selected retrieval system is <span class="font-bold">not</span> Random Baseline.
              <br />
              <br />
              The displayed value is rounded to the next closest value. Additionally, the Similarity Score can be hovered, and the browser will show a hint on the <span class="italic">exact</span> metric value.
            </p>
          </div>
          <div>
            <h1 class="text-lg font-bold tracking-tight">Genre pills</h1>
            <div class="flex flex-col">
              Genre pills are limited to a maximum 5 per song. All genres longer than 12 characters are ignored, in order not to clutter the interface and also avoid a negative impact on user experience.
              <br />
              <br />

              <div class="whitespace-normal">
                The default, and most common, pill is <Tag label="default" />, however, the most popular genre pills are colored differently: {#each [
                  "rock", "hip hop", "rap", "pop", "folk", "jazz"
                ] as genre}
                  <Tag className="inline-block mr-0.5 my-0.5" label={genre} />
                {/each}
              </div>
              <br />
              This was done in order to keep primary focus on the broadest and most common genres.
            </div>
          </div>
        </div>
        <button class="close" use:melt={$close}>
          <X class="square-4" />
        </button>
      </div>
    {/if}

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

  .close {
    @apply absolute right-1.5 top-1.5 flex h-7 w-7 items-center justify-center rounded-full;
    @apply text-magnum-900 transition-colors hover:bg-magnum-500/10;
    @apply focus-visible:ring focus-visible:ring-magnum-400 focus-visible:ring-offset-2;
    @apply bg-white p-0 text-sm font-medium;
  }

  .content {
    @apply z-10 min-w-96 w-[20vw] rounded-lg bg-white p-5 shadow-xl border border-gray-300;
  }
</style>
