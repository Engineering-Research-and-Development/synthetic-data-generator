<script lang="ts">
    import { onMount } from "svelte";
    import CancelButton from "../components/CancelButton.svelte";
    import NextButton from "../components/NextButton.svelte";
    import FunctionsTable from "../components/FunctionsTable.svelte";
    import BackButton from "../components/BackButton.svelte";
    import { Label, Input, InputAddon, ButtonGroup } from 'flowbite-svelte';
    import { PlusOutline } from 'flowbite-svelte-icons';
    import { goto } from "$app/navigation";
    import Error from "../components/Error.svelte";

    let featuresName: string[] = [];
    let featureFunction: FeatureFunction = {};
    let additionalRows: number = 0;
    let errorMessage: string;

    onMount(() => {
        const features = sessionStorage.getItem("selectedColumns");
        if (features) {
            try {
                featuresName = JSON.parse(features);
                featuresName.forEach((feature) => {
                    if (!featureFunction[feature]) {
                        featureFunction[feature] = [];
                    }
                });
            } catch (error) {
                errorMessage="Error parsing selected columns:"+ error;
            }
        }
    });

    function submitFunctions(): void {
        sessionStorage.setItem('featureFunction', JSON.stringify(featureFunction));
        sessionStorage.setItem('additionalRows', additionalRows.toString());
        goto("/parameters");
    }
</script>

{#if errorMessage}
    <Error message={errorMessage}/>
{/if}

<h1 class="flex justify-center text-2xl font-bold my-4">Functions Selection</h1>
<div class="flex items-center justify-center bg-white dark:bg-gray-900">
    <form
            on:submit|preventDefault={submitFunctions}
            class="p-6 bg-white rounded-lg shadow-md dark:bg-gray-800"
    >
        <FunctionsTable
                featuresName={featuresName}
                featureFunction={featureFunction}
        />

        <div class="flex items-center justify-center bg-gray-100 dark:bg-gray-900">
            <div class="p-6 bg-white rounded-lg shadow-md dark:bg-gray-800">
                <Label for="additional_rows" class="block mb-2">Additional number of rows to create</Label>
                <ButtonGroup>
                    <InputAddon>
                        <PlusOutline class="w-4 h-4 text-gray-500 dark:text-gray-400" />
                    </InputAddon>
                    <Input
                            id="additional_rows"
                            bind:value={additionalRows}
                            placeholder="0"
                            type="number"
                            required
                    />
                </ButtonGroup>
            </div>
        </div>
        <div class="flex justify-end gap-4">
            <BackButton />
            <CancelButton />
            <NextButton />
        </div>
    </form>
</div>
