<script lang="ts">
  import SongCard from "$lib/SongCard.svelte";
  import type { PageData } from "./$types";

  export let data: PageData;

  import { createSelect } from "@melt-ui/svelte";
  import { Check, ChevronDown } from "lucide-svelte";
  import { fade } from "svelte/transition";

  // TODO: Map these nice labels to IDs. Also, assign a default value.
  // -- can this be done while instantiating the select element in createSelect? --
  const options = {
    Audio: ["MusiCNN", "MFCCs-BoAW", "i-vectors", "Correlation Pattern BLFs"],
    Text: ["BERT", "TF-IDF", "word2vec"],
    Random: ["Baseline"],
  };

  const {
    elements: { trigger, menu, option, group, groupLabel, label },
    states: { selectedLabel, open },
    helpers: { isSelected },
  } = createSelect<string>({
    forceVisible: true,
    positioning: {
      placement: "bottom",
      fitViewport: true,
    },
  });

  let selectedResultType = "random";
  const embeddingTypes = Object.keys(data.results);
</script>

<div class="flex flex-row w-full flex-wrap gap-y-4">
  <div class="flex flex-col flex-grow">
    <h1 class="text-5xl font-black text-gray-900 tracking-tighter">
      {data.song.song}
    </h1>
    <p class="text-3xl font-bold text-gray-700">{data.song.artist}</p>

    <div class="mt-4">
      <!-- svelte-ignore a11y-label-has-associated-control - $label contains the 'for' attribute -->
      <label class="block text-gray-900" {...$label} use:label>Select embedding:</label>

      <button
        class="flex h-10 min-w-[220px] items-center justify-between rounded-lg bg-white px-3 py-2
  text-gray-700 shadow transition-opacity hover:opacity-90"
        {...$trigger}
        use:trigger
        aria-label="Food"
      >
        {$selectedLabel || "Select a flavor"}
        <ChevronDown class="square-5" />
      </button>

      {#if $open}
        <div
          class="z-10 flex max-h-[300px] flex-col
    overflow-y-auto rounded-lg bg-white p-1
    shadow focus:!ring-0"
          {...$menu}
          use:menu
          transition:fade={{ duration: 150 }}
        >
          {#each Object.entries(options) as [key, arr]}
            <div {...$group(key)} use:group>
              <div
                class="py-1 pl-4 pr-4 font-semibold capitalize text-neutral-800"
                {...$groupLabel(key)}
                use:groupLabel
              >
                {key}
              </div>
              {#each arr as item}
                <div
                  class="relative cursor-pointer rounded-lg py-1 pl-8 pr-4 text-neutral-800
              hover:bg-magnum-100 focus:z-10
              focus:text-magnum-700
              data-[highlighted]:bg-magnum-200 data-[highlighted]:text-magnum-900
              data-[disabled]:opacity-50"
                  {...$option({ value: item, label: item })}
                  use:option
                >
                  <div class="check {$isSelected(item) ? 'inline' : 'hidden'}">
                    <Check class="square-4" />
                  </div>

                  {item}
                </div>
              {/each}
            </div>
          {/each}
        </div>
      {/if}
    </div>
  </div>
  <iframe
    title="Youtube Embed Video for song [{data.song.song}] by [{data.song
      .artist}]"
    width={"640px"}
    height={"360px"}
    src={`https://www.youtube-nocookie.com/embed/${data.song.ytId}?autoplay=0&showinfo=0`}
    frameBorder="0"
    allowFullScreen
  />
</div>

<h2 class="text-3xl font-bold text-gray-800 tracking-tight mt-6 mb-2">
  Related
</h2>
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
  {#each data.results[selectedResultType] as song}
    <SongCard vertical={true} imageClassName="max-h-96" {song} />
  {/each}
</div>

<style lang="postcss">
  .check {
    position: absolute;
    left: theme(spacing.2);
    top: 50%;
    z-index: theme(zIndex.20);
    translate: 0 calc(-50% + 1px);
    color: theme(colors.black);
  }
</style>
