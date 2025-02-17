<script lang="ts">
    import {Label,Select,Table,TableHead,TableBody,TableBodyCell,TableBodyRow,TableHeadCell} from 'flowbite-svelte';
    import { onMount } from 'svelte';

    export let availableAlgorithms: NewAlgorithm[];
    export let selectedModel: SelectedModel

    let fetchedAlgorithms: NewAlgorithm[] = [];
    let chosenAlgo: typeof fetchedAlgorithms[number] | null = null;
    let algorithms: { value: string; name: string }[] = [];
    let algorithmName: string;


    onMount(async ()=>{
        algorithms = availableAlgorithms.map((model) => ({
            value: model.name,
            name: model.name
        }));
    });

    $: {
        chosenAlgo = availableAlgorithms.find((model) => model.name === algorithmName) || null;
        if (chosenAlgo) {
            selectedModel = {id: chosenAlgo.id, name:chosenAlgo.name}
        }
    }
</script>

<div class="w-full">
        <Label>
            Select an option
            <Select class="mt-2" items={algorithms} bind:value={algorithmName} />
        </Label>

    <div class="w-full mt-8">
        {#if chosenAlgo}
            <Table>
                <TableHead>
                    <TableHeadCell class="font-bold">Property</TableHeadCell>
                    <TableHeadCell class="font-bold">Value</TableHeadCell>
                </TableHead>
                <TableBody tableBodyClass="divide-y">
                    <TableBodyRow>
                        <TableBodyCell>Name</TableBodyCell>
                        <TableBodyCell>{chosenAlgo.name}</TableBodyCell>
                    </TableBodyRow>
                    <TableBodyRow>
                        <TableBodyCell>Description</TableBodyCell>
                        <TableBodyCell>{chosenAlgo.description}</TableBodyCell>
                    </TableBodyRow>
                    <TableBodyRow>
                        <TableBodyCell>Loss Function</TableBodyCell>
                        <TableBodyCell>{chosenAlgo.default_loss_function}</TableBodyCell>
                    </TableBodyRow>
                    <TableBodyRow>
                        <TableBodyCell>Allowed Data</TableBodyCell>
                        <TableBodyCell>
                            {#each chosenAlgo.allowed_data as data}
                                <div>{data.datatype} ({data.is_categorical ? 'categorical' : 'non-categorical'})</div>
                            {/each}
                        </TableBodyCell>
                    </TableBodyRow>
                </TableBody>
            </Table>
        {:else}
            <p class="text-gray-500">Please select a model from the dropdown.</p>
        {/if}
    </div>
</div>
