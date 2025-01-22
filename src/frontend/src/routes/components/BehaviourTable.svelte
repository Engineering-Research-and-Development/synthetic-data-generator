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
    export let selectedFeatureBehaviour: FeatureBehaviour = {};

    let fetchedBehaviours: Behaviour[] = [];
    let shownBehaviours: { value: string; name: string;}[] = [];

    onMount(async () => {
        try {
            const response = await fetch(BACKEND_URL +'/behaviours');
            if (response.ok) {
                const data = await response.json();

                fetchedBehaviours = data.behaviours.map((behaviour: Behaviour) => ({
                    id: behaviour.id,
                    name: behaviour.name,
                    description: behaviour.description,
                    function_reference: behaviour.function_reference,
                    function_parameters: behaviour.function_parameters,
                }));

                shownBehaviours = fetchedBehaviours.map((behaviour) => ({
                    value: behaviour.id.toString(),
                    name: behaviour.name,
                }));
            }
        } catch (error) {
            console.error("Error fetching behaviours:", error);
        }
    });
    
    export function updateBehaviours(feature: string, behaviours: string[]) {
        selectedFeatureBehaviour[feature] = behaviours;
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
                            items={shownBehaviours}
                            bind:value={selectedFeatureBehaviour[feature]}
                            placeholder="Select behaviours"
                            class="text-gray-700 self-start"
                            on:change={() => updateBehaviours(feature, selectedFeatureBehaviour[feature])}
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