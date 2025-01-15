<script lang="ts">
    import {Modal, Fileupload, Button, Spinner} from 'flowbite-svelte';
    import Papa from 'papaparse';
    import { goto } from "$app/navigation";
    import CancelButton from "./CancelButton.svelte";

    export let showPopup: boolean;
    export let uploadedFile: File | null;
    let isSubmitting: boolean = false;

    function handleFileUpload(event: Event): void {
        const target = event.target as HTMLInputElement;
        const file = target.files?.[0];

        if (!file) {
            alert('No file selected.');
            return;
        }

        if (file.size > 10 * 1024 * 1024) {
            alert('File size exceeds 10 MB. Please upload a smaller file.');
            return;
        }

        uploadedFile = file;
    }

    async function submitForm(event: Event): Promise<void> {
        event.preventDefault();

        if (!uploadedFile) {
            alert('No file uploaded. Please upload a file first.');
            return;
        }
        isSubmitting = true;

        try {
            const reader = new FileReader();

            reader.onloadend = () => {
                if (reader.result) {
                    Papa.parse(reader.result.toString(), {
                        header: true,
                        skipEmptyLines: true,
                        complete: (result) => {
                            sessionStorage.setItem('userFile', JSON.stringify(result.data));
                            goto('/feature');
                        },
                        error: (error: Error) => {
                            console.error('Parsing failed:', error);
                            alert('Parsing failed. Please check your file and try again.');
                        },
                    });
                } else {
                    alert('Failed to read file. Please try again.');
                }
            };

            reader.readAsText(uploadedFile);
        } catch (error) {
            console.error('Error during file upload:', error);
            alert('An error occurred while uploading the file. Please try again.');
        } finally {
            isSubmitting = false;
        }
    }
</script>

{#if isSubmitting}
    <div class="absolute inset-0 bg-black opacity-90 flex items-center justify-center z-50">
        <div class="flex flex-col items-center">
            <Spinner size="xl"/>
            <span class="text-white mt-4">Uploading...</span>
        </div>
    </div>
{/if}


<Modal bind:open={showPopup} size="md" autoclose outsideclose>
    <div slot="header">Upload CSV</div>

    <div class="p-4">
        <form>
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