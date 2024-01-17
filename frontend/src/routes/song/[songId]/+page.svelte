<script lang="ts">
  import SongCard from "$lib/SongCard.svelte";
  import type { PageData } from "./$types";

  export let data: PageData;

  const options: Record<string, string> = {
    "random": "Random Baseline",
    "blf_correlation.json": "(Audio) Correlation Pattern BLFs",
    "ivec256.json": "(Audio) i-vectors",
    "musicnn.json": "(Audio) MusiCNN",
    "mfcc_bow.json": "(Audio) MFCCs-BoAW",
    "lyrics_bert.json": "(Text) BERT",
    "lyrics_tf-idf.json": "(Text) TF-IDF",
    "lyrics_word2vec.json": "(Text) word2vec",
    "incp.json": "(Video) Inception3",
    "resnet.json": "(Video) ResNet",
    "vgg19.json": "(Video) VGG-19",
  };

  let selectedResultType = "random";
  $: embeddingTypes = Object.keys(data.results).sort((a, b) => {
    const first = Object.keys(options).findIndex((v) => v === a);
    const second = Object.keys(options).findIndex((v) => v === b);
    return first < second ? -1 : 1;
  });
</script>

<div class="flex flex-row w-full flex-wrap gap-x-4 gap-y-4">
  <div class="flex flex-col flex-grow gap-y-8">
    <div>
      <h1 class="text-4xl uhd:text-5xl font-black text-gray-900 tracking-tighter">
        {data.song.song}
      </h1>
      <p class="text-3xl font-bold text-gray-700 tracking-wide">{data.song.artist}</p>
    </div>

    <!--
    <div class="flex flex-col bg-white rounded-lg border border-gray-300">
      <div class="flex bg-gray-100 rounded-t-lg">
        <div class="w-1/4 p-2">System</div>
        <div class="w-1/4 p-2">Header 2</div>
        <div class="w-1/4 p-2">Header 3</div>
        <div class="w-1/4 p-2">Header 4</div>
      </div>
     
      <div class="flex">
        <div class="w-1/4 p-2">Data 1</div>
        <div class="w-1/4 p-2">Data 2</div>
        <div class="w-1/4 p-2">Data 3</div>
        <div class="w-1/4 p-2">Data 4</div>
      </div>
    </div>
    -->
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

<div class="flex flex-row items-center gap-x-3 mt-6 mb-4">
  <h2 class="text-3xl font-bold text-gray-800 tracking-tight">Related</h2>
  <div>
    <select
      bind:value={selectedResultType}
      class="min-w-32 rounded-lg cursor-pointer bg-white px-3 py-1.5
    text-gray-700 shadow transition-all hover:shadow-lg"
    >
      {#each embeddingTypes as resultType}
        <option value={resultType}>{options[resultType]}</option>
      {/each}
    </select>
  </div>
</div>

<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 uhd:grid-cols-4 gap-6">
  {#each data.results[selectedResultType] as song}
    <SongCard vertical={true} imageClassName="max-h-96" {song} />
  {/each}
</div>
