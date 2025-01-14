<script lang="ts">
    import { Img, Button, Spinner } from 'flowbite-svelte';
    import UploadModal from "./components/UploadModal.svelte";

    const createEndpoint = '/create';
    let showPopup: boolean = false;
    let isSubmitting: boolean = false;
    let uploadedFile: File | null = null;
</script>

<div class="h-screen w-screen bg-cover bg-center flex items-center justify-center relative"
     style="background-image: url('/pexels-markusspiske-1089438.jpg');">
    <div class="text-center relative z-10">
        <Img src="ENG-LOGO-LIGHT.png" alt="ENG logo" size="max-w-xs" alignment="mx-auto"/>
        <h1 class="text-white text-4xl md:text-6xl font-bold mb-6">Data Synthetic Generator</h1>
        <div class="flex justify-center space-x-4">
            <Button
                    on:click={() => (showPopup = true)}
                    class="px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg shadow-md hover:bg-blue-700 transition">
                Enhance Existing dataset
            </Button>
            <Button
                    href={createEndpoint}
                    class="px-6 py-3 bg-gray-600 text-white font-semibold rounded-lg shadow-md hover:bg-gray-700 transition">
                Create a dataset from scratch
            </Button>
        </div>
    </div>

    {#if isSubmitting}
        <div class="absolute inset-0 bg-black opacity-90 flex items-center justify-center z-50">
            <div class="flex flex-col items-center">
                <Spinner size="xl"/>
                <span class="text-white mt-4">Uploading...</span>
            </div>
        </div>
    {/if}
</div>

<UploadModal bind:showPopup bind:isSubmitting bind:uploadedFile />
