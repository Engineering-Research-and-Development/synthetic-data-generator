<script lang="ts">
    import ModelNew from "../components/ModelNew.svelte";
    import ModelPreTrained from "../components/ModelPreTrained.svelte";
    import { Button } from "flowbite-svelte";
    import CancelButton from "../components/CancelButton.svelte";
    import NextButton from "../components/NextButton.svelte";
    import BackButton from "../components/BackButton.svelte";
    import { goto } from "$app/navigation";
    import { onMount } from "svelte";
    import { BACKEND_URL } from "../../stores/shared";

    let useNewModel = true;
    let selectedModel: SelectedModel;
    let selectedVersion: number;
    let trained_models: PreTrainedModel[];
    let algorithms: NewAlgorithm[];
    let isLoading = true; // Add a loading state

    onMount(async () => {
        try {
            const response = await fetch(BACKEND_URL + '/algorithms/?include_allowed_datatypes=true')
            if (response.ok) {
                algorithms = await response.json()
            } else {
                console.error('Failed to fetch data:', response.statusText);
            }
        } catch (error) {
            console.error('Error fetching data:', error);

        }
        try {
            const response = await fetch(BACKEND_URL + '/trained_models/?include_version_ids=true');
            if (response.ok) {
                trained_models = await response.json();
            } else {
                console.error('Failed to fetch data:', response.statusText);
            }
        } catch (error) {
            console.error('Error fetching data:', error);
        } finally {
            isLoading = false; // Set loading to false after fetching data
        }
    });

    function submitModels() {
        sessionStorage.setItem('newModel', JSON.stringify(useNewModel));
        sessionStorage.setItem('selectedModel', JSON.stringify(selectedModel));
        sessionStorage.setItem('selectedVersion', JSON.stringify(selectedVersion))
        goto("/preview")
    }
</script>

<h1 class="text-2xl font-bold text-center my-6">Choose the AI model to use</h1>

<div class="flex items-center justify-center h-screen bg-gray-100 dark:bg-gray-900">
    <form on:submit|preventDefault={submitModels}
          class="w-full max-w-4xl p-6 bg-white rounded-lg shadow-md dark:bg-gray-800"
    >
        <!-- Models Side-by-Side -->
        <div class="flex flex-col md:flex-row gap-6 mb-6">
            <!-- New Model Box -->
            <div class={`flex-1 p-4 border rounded-lg transition ${
                    useNewModel ? "border-blue-500" : "border-gray-300 opacity-50 pointer-events-none"
                }`}
            >
                <h2 class="text-xl font-semibold mb-4 text-center">New Model</h2>
                {#if !isLoading}
                    <ModelNew availableAlgorithms={algorithms} bind:selectedModel />
                {:else}
                    <p>Loading...</p>
                {/if}
                <Button class="mt-4 w-full"
                        color="blue"
                        on:click={() => (useNewModel = false)}
                >
                    Use Pre-Trained Model
                </Button>
            </div>

            <!-- Pre-Trained Model Box -->
            <div class={`flex-1 p-4 border rounded-lg transition ${
                    useNewModel ? "border-gray-300 opacity-50 pointer-events-none" : "border-blue-500"
                }`}
            >
                <h2 class="text-xl font-semibold mb-4 text-center">Pre-Trained Model</h2>
                {#if !isLoading}
                    <ModelPreTrained trainedModels={trained_models} bind:selectedModel bind:selectedVersion/>
                {:else}
                    <p>Loading...</p>
                {/if}
                <Button class="mt-4 w-full"
                        color="blue"
                        on:click={() => (useNewModel = true)}
                >
                    Use New Model
                </Button>
            </div>
        </div>

        <!-- Buttons Below -->
        <div class="flex justify-end gap-4">
            <BackButton />
            <CancelButton />
            <NextButton />
        </div>
    </form>
</div>