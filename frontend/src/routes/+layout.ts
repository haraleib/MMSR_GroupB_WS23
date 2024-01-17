// import { metadata } from "$lib/server/songs";

// fetch songs from the API
export async function load({ fetch }) {
  const res = await fetch("/songMeta.json");
  const songs = await res.json();

  return {
    props: {
      songs,
    },
  };
}
