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
    import { BACKEND_URL } from "../../stores/shared";
    import NextButton from "../components/NextButton.svelte";
    import BackButton from "../components/BackButton.svelte";
    import CancelButton from "../components/CancelButton.svelte";
    import { goto } from "$app/navigation";

    let selectedFunctions: FeatureFunction = {};
    let functionData: Record<string, FunctionParameter[]> = {};

    onMount(async () => {
        selectedFunctions = JSON.parse(sessionStorage.getItem("featureFunction") || "{}");

        try {
            // Collect all unique IDs from selectedFunctions
            const allFunctionIds = new Set<string>();
            for (const ids of Object.values(selectedFunctions)) {
                ids.forEach(id => allFunctionIds.add(id));
            }

            // Fetch data for all unique IDs
            const fetchedData: Record<string, FunctionParameter[]> = {};
            const uniqueIds = Array.from(allFunctionIds);

            // Fetch data for all unique IDs
            const responses = await Promise.all(
                uniqueIds.map(async (id) => {
                    const response = await fetch(`${BACKEND_URL}/functions/${id}`);

                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    }

                    return response.json();
                })
            );

            // Associate the fetched data with the corresponding feature
            uniqueIds.forEach((id, index) => {
                const functionParameter = responses[index] as FunctionParameter;
                for (const [feature, ids] of Object.entries(selectedFunctions)) {
                    if (ids.includes(id)) {
                        if (!fetchedData[feature]) {
                            fetchedData[feature] = [];
                        }
                        fetchedData[feature].push(functionParameter);
                    }
                }
            });

            functionData = fetchedData;
        } catch (error) {
            console.error("Error fetching data:", error);
        }
    });

    function saveFunctionData() {
        const functionDataToSave: Record<string, Array<{
            functionId: number;
            functionName: string;
            parameters: Array<{ name: string; value: number }>
        }>> = {};

        for (const [feature, functionParameters] of Object.entries(functionData)) {
            functionDataToSave[feature] = [];

            for (const functionParameter of functionParameters) {
                const functionEntry = {
                    functionId: functionParameter.function.id,
                    functionName: functionParameter.function.name,
                    parameters: [] as Array<{ name: string; value: number }>
                };

                for (const param of functionParameter.parameter) {
                    const inputElement = document.getElementById(`param-${functionParameter.function.id}-${param.id}`) as HTMLInputElement;
                    if (inputElement) {
                        functionEntry.parameters.push({
                            name: param.name,
                            value: parseFloat(inputElement.value)
                        });
                    }
                }

                functionDataToSave[feature].push(functionEntry);
            }
        }

        sessionStorage.setItem("functionData", JSON.stringify(functionDataToSave));
        goto("/model");
    }
</script>

<h1 class="flex justify-center text-2xl font-bold my-4">Function Composition</h1>
<div class="flex items-center justify-center bg-gray-100 dark:bg-gray-900">
    <form on:submit|preventDefault={saveFunctionData}>
        {#if Object.keys(functionData).length > 0}
            {#each Object.entries(functionData) as [feature, functionParameters]}
                <h2 class="text-xl font-semibold mb-2 mt-4">Feature: {feature}</h2>
                <Table class="w-full">
                    <TableHead class="bg-gray-200">
                        <TableHeadCell class="w-1/3">Name</TableHeadCell>
                        <TableHeadCell class="w-1/3">Description</TableHeadCell>
                        <TableHeadCell class="w-1/3">Parameters</TableHeadCell>
                    </TableHead>
                    <TableBody>
                        {#each functionParameters as functionParameter}
                            <TableBodyRow>
                                <TableBodyCell>{functionParameter.function.name}</TableBodyCell>
                                <TableBodyCell>{functionParameter.function.description}</TableBodyCell>
                                <TableBodyCell>
                                    {#each functionParameter.parameter as param}
                                        <Label for={`param-${functionParameter.function.id}-${param.id}`} class="block text-sm font-medium text-gray-700">
                                            {param.name} ({param.parameter_type}):
                                        </Label>
                                        <Input
                                                id={`param-${functionParameter.function.id}-${param.id}`}
                                                type="number" step="0.01"
                                                placeholder={param.value}
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
            <p class="text-gray-700">No functions selected or data available.</p>
        {/if}
    </form>
</div>