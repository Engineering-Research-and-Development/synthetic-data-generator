<script>
import { browser } from "$app/environment";
import {Button} from "flowbite-svelte";


function nav_back() {
    if (browser) window.history.back();
}
</script>

<Button
        on:click={() => (nav_back())}
        class="text-gray-500 bg-white border border-gray-300 rounded-md px-4 py-2 mr-2 hover:bg-gray-100"
>
    Back
</Button>