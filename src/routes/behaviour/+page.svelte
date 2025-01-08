<script lang="ts">
    import { onMount } from "svelte";
    import CancelButton from "../components/CancelButton.svelte";
    import NextButton from "../components/NextButton.svelte";
    import BehaviourTable from "../components/BehaviourTable.svelte";
    import BackButton from "../components/BackButton.svelte";
    import { Label, Input, InputAddon, ButtonGroup } from 'flowbite-svelte';
    import { PlusOutline } from 'flowbite-svelte-icons';
    import { goto } from "$app/navigation";

    // Define types for features and selected behaviours
    type SelectedBehaviours = { [feature: string]: string[] };

    let featuresName: string[] = []; // Array of feature names
    let selectedBehaviours: SelectedBehaviours = {}; // Mapping feature -> selected behaviours
    let additionalRows: number = 0; // Number of additional rows to create

    onMount(() => {
        const features = sessionStorage.getItem("selectedColumns");
        if (features) {
            try {
                featuresName = JSON.parse(features);
                featuresName.forEach((feature) => {
                    if (!selectedBehaviours[feature]) {
                        selectedBehaviours[feature] = [];
                    }
                });
            } catch (error) {
                console.error("Error parsing selected columns:", error);
            }
        }
    });

    function submitBehaviours(): void {
        sessionStorage.setItem('selectedBehaviours', JSON.stringify(selectedBehaviours));
        sessionStorage.setItem('additional_rows', additionalRows.toString());
        goto("/model");
    }
</script>

<h1 class="flex justify-center text-2xl font-bold my-4">Behaviour Selection</h1>
<div class="flex items-center justify-center h-screen bg-gray-100 dark:bg-gray-900">
    <form on:submit|preventDefault={submitBehaviours}
        class="w-full max-w-4xl p-6 bg-white rounded-lg shadow-md dark:bg-gray-800"
          >
        <div class="flex flex-col md:flex-row gap-6 mb-6">
            <BehaviourTable
                    featuresName={featuresName}
                    selectedBehaviours={selectedBehaviours}
            />
        </div>

        <Label for="additional_rows" class="block mb-2">Additional number of rows to create</Label>
        <ButtonGroup class="w-full">
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

        <div class="flex justify-end gap-4">
            <BackButton />
            <CancelButton />
            <NextButton />
        </div>
    </form>
</div>
