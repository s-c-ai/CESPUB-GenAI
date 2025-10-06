<script lang="ts">
  import type { Snippet } from "svelte";

  interface ButtonProps {
    children: Snippet;
    type?: "submit" | "button";
  }

  let { children, ...props }: ButtonProps = $props();
</script>

<button
  class="flex items-center gap-4 border rounded-xl py-3 px-10 border-primary hover:shadow-xl cursor-pointer"
  type="submit"
  {...props}
>
  {@render children()}
</button>
