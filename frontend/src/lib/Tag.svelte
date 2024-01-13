<script lang="ts">
    import { cx } from "$lib";

    export let label: string;

    const colorMap: Record<string, string> = {
      "hip hop": "bg-blue-700 text-blue-50",
      "rock": "bg-red-900 text-red-50",
      "rap": "bg-yellow-600 text-yellow-50",
      "pop": "bg-purple-800 text-purple-50",
      "folk": "bg-pink-700 text-pink-50",
      "jazz": "bg-green-700 text-green-50",
    };
</script>

<span
  class={cx(
    "text-sm font-medium px-2.5 py-0.5 rounded-full",
    label in colorMap ? colorMap[label] : "bg-gray-200 text-gray-800"
  )}
>
  {label}
</span>
