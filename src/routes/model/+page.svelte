<script lang="ts">
import ModelNew from "../components/ModelNew.svelte";
import ModelPreTrained from "../components/ModelPreTrained.svelte";
import {Button} from "flowbite-svelte";
import CancelButton from "../components/CancelButton.svelte";
import NextButton from "../components/NextButton.svelte";
import BackButton from "../components/BackButton.svelte";
let useNewModel = true;

let selectedModel = String;
function submitModels() {
    console.log(useNewModel);
    console.log(selectedModel);

}
</script>

<h1 class="flex justify-center text-2xl font-bold my-4">Choose the AI model to use</h1>
<div class="flex items-center justify-center h-screen bg-gray-100 dark:bg-gray-900">
    <form on:submit|preventDefault={submitModels}>
        {#if useNewModel}
            <ModelNew
                bind:selected={selectedModel}/>
            <Button
                    class="ml-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-700"
                    on:click={() => (useNewModel = false)}
                    bind:value={useNewModel}
            >
                Use Pre-Trained Model
            </Button>
        {:else}
            <ModelPreTrained
                bind:slected={selectedModel}/>
            <Button
                    class="ml-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-700"
                    on:click={() => (useNewModel = true)}
            >
                Use New Model
            </Button>
        {/if}

        <NextButton/>
        <BackButton/>
        <CancelButton/>
    </form>
</div>