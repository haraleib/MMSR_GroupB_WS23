<script lang="ts">
  import { createPagination, createSync, melt } from "@melt-ui/svelte";
  import { ChevronLeft, ChevronRight } from "lucide-svelte";

  import { cx } from "$lib";

  export let currentPage = 1;
  export let itemCount = 10;
  export let pageSize = 10;

  let {
    elements: { root, pageTrigger, prevButton, nextButton },
    states: { pages, range, page },
  } = createPagination({
    count: itemCount,
    perPage: pageSize,
    defaultPage: currentPage,
    siblingCount: 2,
  });

  const sync = createSync({ page });
  $: sync.page(currentPage, (v) => (currentPage = v));

  const buttonClass = cx(
    "grid h-10 items-center rounded-3xl bg-white border border-gray-300 px-4 transition-all text-sm text-gray-900 shadow",
    "hover:bg-gray-100 disabled:cursor-not-allowed disabled:bg-gray-100 data-[selected]:bg-gray-900",
    "data-[selected]:text-white"
  );
</script>

<nav
  class="flex flex-col items-center gap-1 my-4"
  aria-label="pagination"
  use:melt={$root}
>
  <p class="text-center text-gray-900">
    Showing items {$range.start} - {$range.end}
  </p>

  <div class="flex items-center gap-2">
    <button class={buttonClass} use:melt={$prevButton}>
      <ChevronLeft class="square-4" />
    </button>

    {#each $pages as page (page.key)}
      {#if page.type === "ellipsis"}
        <span>...</span>
      {:else}
        <button class={buttonClass} use:melt={$pageTrigger(page)}>
          {page.value}
        </button>
      {/if}
    {/each}

    <button class={buttonClass} use:melt={$nextButton}>
      <ChevronRight class="square-4" />
    </button>
  </div>
</nav>
