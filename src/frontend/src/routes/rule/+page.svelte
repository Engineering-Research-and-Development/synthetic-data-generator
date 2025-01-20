<script lang="ts">
    import { onMount } from 'svelte';
    import {
        Table,
        TableBodyRow,
        TableBodyCell,
        TableHead,
        TableHeadCell,
        TableBody,
        Label,
        Input
    } from 'flowbite-svelte';
    import {BACKEND_URL} from "../../stores/sharedVars";
    import NextButton from "../components/NextButton.svelte";
    import BackButton from "../components/BackButton.svelte";
    import CancelButton from "../components/CancelButton.svelte";
    import {goto} from "$app/navigation";

    let selectedBehaviours: FeatureBehaviour = {};
    let behaviourData: Record<string, Behaviour[]> = {};

    onMount(async () => {
        selectedBehaviours = JSON.parse(sessionStorage.getItem("selectedBehaviours") || "{}");
        try {
            const fetchedData: Record<string, Behaviour[]> = {};
            for (const [feature, ids] of Object.entries(selectedBehaviours)) {
                fetchedData[feature] = await Promise.all(
                    ids.map(async (id) => {
                        const response = await fetch(`${BACKEND_URL}/behaviours/${id}`);

                        if (!response.ok) {
                            throw new Error(`HTTP error! Status: ${response.status}`);
                        }

                        return (await response.json()) as Behaviour;
                    })
                );
            }

            behaviourData = fetchedData;
        } catch (error) {
            console.error("Error fetching data:", error);
        }
    });

    function saveRulesData() {
        const rulesData: Record<string, Array<{
            behaviourName: string;
            parameters: Array<{ name: string; value: number }>
        }>> = {};

        for (const [feature, behaviours] of Object.entries(behaviourData)) {
            rulesData[feature] = [];

            for (const behaviour of behaviours) {
                const behaviourEntry = {
                    behaviourName: behaviour.name,
                    parameters: [] as Array<{ name: string; value: number }>
                };

                for (const param of behaviour.function_parameters) {
                    const inputElement = document.getElementById(`param-${behaviour.id}-${behaviour.function_parameters.indexOf(param)}`) as HTMLInputElement;
                    if (inputElement) {
                        behaviourEntry.parameters.push({
                            name: param.name,
                            value: parseFloat(inputElement.value)
                        });
                    }
                }

                rulesData[feature].push(behaviourEntry);
            }
        }

        sessionStorage.setItem("rulesData", JSON.stringify(rulesData));
        goto("/model");
    }
</script>


<h1 class="flex justify-center text-2xl font-bold my-4">Rules composition</h1>
<div class="flex items-center justify-center h-screen bg-gray-100 dark:bg-gray-900">
    <form on:submit|preventDefault={saveRulesData}>

    {#if Object.keys(behaviourData).length > 0}
        {#each Object.entries(behaviourData) as [feature, behaviours]}
            <h2 class="text-xl font-semibold mb-2 mt-4">Feature: {feature}</h2>
            <Table class="w-full">
                <TableHead class="bg-gray-200">
                    <TableHeadCell class="w-1/3">Name</TableHeadCell>
                    <TableHeadCell class="w-1/3">Description</TableHeadCell>
                    <TableHeadCell class="w-1/3">Parameters</TableHeadCell>
                </TableHead>
                <TableBody>
                    {#each behaviours as behaviour}
                        <TableBodyRow>
                            <TableBodyCell>{behaviour.name}</TableBodyCell>
                            <TableBodyCell>{behaviour.description}</TableBodyCell>
                            <TableBodyCell>
                                {#each behaviour.function_parameters as param, index}
                                    <Label for={`param-${behaviour.id}-${index}`} class="block text-sm font-medium text-gray-700">
                                        {param.name} ({param.type}):
                                    </Label>
                                    <Input
                                            id={`param-${behaviour.id}-${index}`}
                                            type="number"
                                            placeholder={param.value.toString()}
                                            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                                    />
                                {/each}
                            </TableBodyCell>
                        </TableBodyRow>
                    {/each}
                </TableBody>
            </Table>
        {/each}
        <div class="flex justify-end gap-4">
            <BackButton />
            <CancelButton />
            <NextButton />
        </div>
    {:else}
        <p class="text-gray-700">No behaviours selected or data available.</p>
    {/if}
    </form>
</div>

