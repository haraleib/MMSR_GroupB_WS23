export const prerender = true;

// fetch songs from the API
export async function load({ page, fetch }) {
  const res = await fetch("/songMeta.json");
  const songs = await res.json();

  return {
    props: {
      songs,
    },
  };
}