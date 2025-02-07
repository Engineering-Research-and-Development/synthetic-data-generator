<script lang="ts">
    import { onMount } from "svelte";
    import {
        Table,
        TableBody,
        TableBodyRow,
        TableBodyCell,
        TableHead,
        TableHeadCell,
        MultiSelect,
    } from "flowbite-svelte";
    import { BACKEND_URL } from "../../stores/shared";

    export let featuresName: string[] = [];
    export let featureFunction: FeatureFunction = {};

    let shownFunctions: { value: string; name: string;}[] = [];

    onMount(async () => {
        try {
            const response = await fetch(BACKEND_URL +'/functions');
            if (response.ok) {
                const data = await response.json();

                const fetchedFunctions: FunctionParameter[] = data.map((functionParameter: FunctionParameter) => ({
                    function: {
                        id: functionParameter.function.id,
                        name: functionParameter.function.name,
                        description: functionParameter.function.description,
                        function_reference: functionParameter.function.function_reference,
                    },
                    parameter: functionParameter.parameter.map((param: Parameter) => ({
                        id: param.id,
                        name: param.name,
                        value: param.value,
                        parameter_type: param.parameter_type,
                    })),
                }));

                shownFunctions = fetchedFunctions.map((Function) => ({
                    value: Function.function.id.toString(),
                    name: Function.function.name,
                }));
            }
        } catch (error) {
            console.error("Error fetching Functions:", error);
        }
    });

    export function updateFunctions(feature: string, Functions: string[]) {
        featureFunction[feature] = Functions;
    }
</script>

<Table class="w-3/4 text-gray-500 self-center dark:text-gray-400">
    <TableHead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
        {#each featuresName as feature}
            <TableHeadCell>{feature}</TableHeadCell>
        {/each}
    </TableHead>
    <TableBody tableBodyClass="divide-y">
        <TableBodyRow class="bg-white border-b dark:bg-gray-800 dark:border-gray-700">
            {#each featuresName as feature}
                <TableBodyCell>
                    <MultiSelect
                            items={shownFunctions}
                            bind:value={featureFunction[feature]}
                            placeholder="Select Functions"
                            class="text-gray-700 self-start"
                            on:change={() => updateFunctions(feature, featureFunction[feature])}
                    />
                </TableBodyCell>
            {/each}
        </TableBodyRow>
    </TableBody>
    <TableBody tableBodyClass="divide-y">
        <TableBodyRow class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 h-96">
        </TableBodyRow>
    </TableBody>
</Table>