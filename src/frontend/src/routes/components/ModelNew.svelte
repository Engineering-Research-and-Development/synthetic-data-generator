<script lang="ts">
    import {Label, Select, Table, TableHead, TableBody, TableBodyCell, TableBodyRow} from 'flowbite-svelte';
    import { onMount } from 'svelte';

    export let builtInModels;
    export let selected: string;

    let fetchedBuiltInModels: {
        name: string;
        description: string;
        loss_function: string;
        allowed_datatype: string[];
        is_categorical: boolean[];
    }[] = [];
    let selectedModel: typeof fetchedBuiltInModels[number] | null = null;
    let newModels: { value: string; name: string }[] = [];

    onMount(async ()=>{
        fetchedBuiltInModels = builtInModels || [];
        newModels = fetchedBuiltInModels.map((model) => ({
            value: model.name,
            name: model.name
        }));
    });

    $: selectedModel = fetchedBuiltInModels.find((model) => model.name === selected) || null;
</script>

<div class="w-full">
        <Label>
            Select an option
            <Select class="mt-2" items={newModels} bind:value={selected} />
        </Label>

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
                        <TableBodyCell>Description</TableBodyCell>
                        <TableBodyCell>{selectedModel.description}</TableBodyCell>
                    </TableBodyRow>
                    <TableBodyRow>
                        <TableBodyCell>Loss Function</TableBodyCell>
                        <TableBodyCell>{selectedModel.loss_function}</TableBodyCell>
                    </TableBodyRow>
                    <TableBodyRow>
                        <TableBodyCell>Allowed Datatypes</TableBodyCell>
                        <TableBodyCell>{selectedModel.allowed_datatype.join(', ')}</TableBodyCell>
                    </TableBodyRow>
                    <TableBodyRow>
                        <TableBodyCell>Is Categorical</TableBodyCell>
                        <TableBodyCell>
                            {selectedModel.is_categorical.map((val) => (val ? 'Yes' : 'No')).join(', ')}
                        </TableBodyCell>
                    </TableBodyRow>
                </TableBody>
            </Table>
        {:else}
            <p class="text-gray-500">No model selected. Please select a model from the dropdown.</p>
        {/if}
    </div>
</div>
