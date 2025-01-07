<script>
    import { Img, Button, Modal, Fileupload, Spinner } from 'flowbite-svelte';
    import { goto } from "$app/navigation";
    import Papa from 'papaparse';
    import CancelButton from "./components/CancelButton.svelte";

    const createEndpoint = '/create';
    let showPopup = false;
    let uploadedFile = File;
    let isSubmitting = false;

    function handleFileUpload(event) {
        const file = event.target.files[0];

        if (file.size > 10 * 1024 * 1024) {
            alert('File size exceeds 10 MB. Please upload a smaller file.');
            return;
        }

        uploadedFile = file;
    }

    async function submitForm(event) {
        event.preventDefault();
        isSubmitting = true;

        const reader = new FileReader();

        reader.onloadend = () => {
            Papa.parse(reader.result, {
                header: true,
                skipEmptyLines: true,
                complete: (result) => {
                    sessionStorage.setItem('userFile', JSON.stringify(result.data));
                    isSubmitting = false;
                    goto('/feature');
                },
            });
        };

        reader.readAsText(uploadedFile);
    }
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
                    href="{createEndpoint}"
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

<Modal bind:open={showPopup} size="md" autoclose outsideclose>
    <div slot="header">Upload CSV</div>

    <div class="p-4">
        <form on:submit|preventDefault={submitForm}>
            <div class="mb-4">
                <label
                        for="csvFile"
                        class="block text-sm font-medium text-gray-700 mb-2"
                >
                    Choose a CSV file
                </label>
                <Fileupload
                        id="csvFile"
                        type="file"
                        accept=".csv"
                        on:change={handleFileUpload}
                        class="block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 focus:outline-none focus:ring focus:border-blue-300"
                        required
                />
            </div>
            <div class="flex justify-end">
                <CancelButton/>
                <Button
                        type="submit"
                        on:click={submitForm}
                        class="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600"
                >
                    Upload
                </Button>
            </div>
        </form>
    </div>
</Modal>
