<script lang="ts">
    import { Label, Select, Table, TableHead, TableBody, TableBodyCell, TableBodyRow, TableHeadCell } from 'flowbite-svelte';
    import { onMount } from 'svelte';

    export let trainedModels;
    export let selectedModel: string;
    export let selectedVersion: number;

    let fetchedModels: {
        name: string;
        id: number;
        dataset_name: string;
        input_shape: string;
        algorithm_name: string;
        size: string;
        version_ids: number[];
    }[] = [];
    let models: typeof fetchedModels[number] | null = null;
    let selectedVersionLabel: { value: number; name: string }[] = [];
    let newModels: { value: string; name: string }[] = [];
    let selectedModelVersions: string = "";

    onMount(async () => {
        try {
                fetchedModels = trainedModels || [];
                newModels = fetchedModels.map((model) => ({
                    value: model.name,
                    name: model.name
                }));
        } catch (error) {
            console.error('Error fetching trained models:', error);
        }
    });

    $: models = fetchedModels.find((model) => model.name === selectedModel) || null;
    $: selectedVersionLabel = models ? models.version_ids.map((id) => ({ value: id, name: `Version ${id}` })): [];
    $: selectedModelVersions = models? models.version_ids.join(", "): "";
</script>

<div class="w-full">
    <!-- Dropdown for model selection -->
    <div class="w-full">
        <Label>
            Select a model
            <Select class="mt-2" items={newModels} bind:value={selectedModel} />
        </Label>
    </div>

    <!-- Label list for selecting version_id -->
    <div class="w-full">
            <Label>
                Available Version IDs:
                <Select class="mt-2" items={selectedVersionLabel} bind:value={selectedVersion}/>
            </Label>
    </div>

    <!-- Table to display selected model details -->
    <div class="w-full mt-8">
        {#if models}
            <Table>
                <TableHead>
                    <TableHeadCell class="font-bold">Property</TableHeadCell>
                    <TableHeadCell class="font-bold">Value</TableHeadCell>
                </TableHead>
                <TableBody>
                    <TableBodyRow>
                        <TableBodyCell>Name</TableBodyCell>
                        <TableBodyCell>{models.name}</TableBodyCell>
                    </TableBodyRow>
                    <TableBodyRow>
                        <TableBodyCell>Dataset Name</TableBodyCell>
                        <TableBodyCell>{models.dataset_name}</TableBodyCell>
                    </TableBodyRow>
                    <TableBodyRow>
                        <TableBodyCell>Input Shape</TableBodyCell>
                        <TableBodyCell>{models.input_shape}</TableBodyCell>
                    </TableBodyRow>
                    <TableBodyRow>
                        <TableBodyCell>Algorithm</TableBodyCell>
                        <TableBodyCell>{models.algorithm_name}</TableBodyCell>
                    </TableBodyRow>
                    <TableBodyRow>
                        <TableBodyCell>Size</TableBodyCell>
                        <TableBodyCell>{models.size}</TableBodyCell>
                    </TableBodyRow>
                    <TableBodyRow>
                        <TableBodyCell>Version ID</TableBodyCell>
                        <TableBodyCell>{selectedModelVersions}</TableBodyCell>
                    </TableBodyRow>
                </TableBody>
            </Table>
        {:else}
            <p class="text-gray-500">Please select a model from the dropdown.</p>
        {/if}
    </div>
</div>
