<script lang="ts">
    import { Label, Select, Table, TableHead, TableBody, TableBodyCell, TableBodyRow } from 'flowbite-svelte';
    import { onMount } from 'svelte';

    export let trainedModels;
    export let selected: string;

    let fetchedTrainedModels: {
        name: string;
        id: number;
        dataset_name: string;
        input_shape: string;
        algorithm_name: string;
        size: string;
        version_ids: number[];
    }[] = [];
    let selectedModel: typeof fetchedTrainedModels[number] | null = null;
    let selectedVersionLabel: string = '';
    let newModels: { value: string; name: string }[] = [];

    onMount(async () => {
        try {
                fetchedTrainedModels = trainedModels || [];
                newModels = fetchedTrainedModels.map((model) => ({
                    value: model.name,
                    name: model.name
                }));
        } catch (error) {
            console.error('Error fetching trained models:', error);
        }
    });

    $: selectedModel = fetchedTrainedModels.find((model) => model.name === selected) || null;
    $: selectedVersionLabel = selectedModel?.version_ids.join(', ') || '';
</script>

<div class="w-full">
    <!-- Dropdown for model selection -->
    <div class="w-1/2">
        <Label>
            Select a model
            <Select class="mt-2" items={newModels} bind:value={selected} />
        </Label>
    </div>

    <!-- Label list for selecting version_id -->
    <div class="w-1/2 mt-4">
        {#if selectedModel}
            <Label>
                Available Version IDs:
                <span class="ml-2 font-medium text-gray-700">{selectedVersionLabel}</span>
            </Label>
        {:else}
            <p class="text-gray-500">No model selected. Please select a model from the dropdown.</p>
        {/if}
    </div>

    <!-- Table to display selected model details -->
    <div class="w-full mt-8">
        {#if selectedModel}
            <Table>
                <TableHead>
                    <TableBodyRow>
                        <TableBodyCell class="font-bold">Property</TableBodyCell>
                        <TableBodyCell class="font-bold">Value</TableBodyCell>
                    </TableBodyRow>
                </TableHead>
                <TableBody>
                    <TableBodyRow>
                        <TableBodyCell>Name</TableBodyCell>
                        <TableBodyCell>{selectedModel.name}</TableBodyCell>
                    </TableBodyRow>
                    <TableBodyRow>
                        <TableBodyCell>Dataset Name</TableBodyCell>
                        <TableBodyCell>{selectedModel.dataset_name}</TableBodyCell>
                    </TableBodyRow>
                    <TableBodyRow>
                        <TableBodyCell>Input Shape</TableBodyCell>
                        <TableBodyCell>{selectedModel.input_shape}</TableBodyCell>
                    </TableBodyRow>
                    <TableBodyRow>
                        <TableBodyCell>Algorithm</TableBodyCell>
                        <TableBodyCell>{selectedModel.algorithm_name}</TableBodyCell>
                    </TableBodyRow>
                    <TableBodyRow>
                        <TableBodyCell>Size</TableBodyCell>
                        <TableBodyCell>{selectedModel.size}</TableBodyCell>
                    </TableBodyRow>
                    <TableBodyRow>
                        <TableBodyCell>Version ID</TableBodyCell>
                        <TableBodyCell>{selectedVersionLabel}</TableBodyCell>
                    </TableBodyRow>
                </TableBody>
            </Table>
        {:else}
            <p class="text-gray-500">No model selected. Please select a model from the dropdown.</p>
        {/if}
    </div>
</div>
