<script lang="ts">
    import { createPagination, createSync, melt } from "@melt-ui/svelte";
    import { ChevronLeft, ChevronRight } from "lucide-svelte";

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
</script>

<nav
    class="flex flex-col items-center gap-4"
    aria-label="pagination"
    use:melt={$root}
>
    <p class="text-center text-teal-900">
        Showing items {$range.start} - {$range.end}
    </p>
    <div class="flex items-center gap-2">
        <button
            class="grid h-8 items-center rounded-md bg-white px-3 text-sm text-teal-900 shadow-sm
      hover:opacity-75 disabled:cursor-not-allowed disabled:opacity-50 data-[selected]:bg-teal-900
      data-[selected]:text-white"
            use:melt={$prevButton}><ChevronLeft class="square-4" /></button
        >
        {#each $pages as page (page.key)}
            {#if page.type === "ellipsis"}
                <span>...</span>
            {:else}
                <button
                    class="grid h-8 items-center rounded-md bg-white px-3 text-sm text-teal-900 shadow-sm
          hover:opacity-75 disabled:cursor-not-allowed disabled:opacity-50 data-[selected]:bg-teal-900
        data-[selected]:text-white"
                    use:melt={$pageTrigger(page)}>{page.value}</button
                >
            {/if}
        {/each}
        <button
            class="grid h-8 items-center rounded-md bg-white px-3 text-sm text-teal-900 shadow-sm
      hover:opacity-75 disabled:cursor-not-allowed disabled:opacity-50 data-[selected]:bg-teal-900
    data-[selected]:text-white"
            use:melt={$nextButton}><ChevronRight class="square-4" /></button
        >
    </div>
</nav>
