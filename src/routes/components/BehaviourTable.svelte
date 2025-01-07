<script>
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

    export let featuresName = [];
    export let selectedBehaviours = {};

    let fetchedBehaviours = [];
    let behaviours = [
        { value: "Distribution", name: "Distribution" },
        { value: "Threshold", name: "Threshold" },
        { value: "Formula", name: "Formula" },
    ];

    onMount(async () => {
        try {
            const response = await fetch('/api/behaviours');
            if (response.ok) {
                fetchedBehaviours = await response.json();
                behaviours = fetchedBehaviours.length ? fetchedBehaviours : behaviours;
            }
        } catch (error) {
            console.error("Error fetching behaviours:", error);
        }
    });

    export function updateBehaviours(feature, behaviours) {
        selectedBehaviours[feature] = behaviours;
    }
</script>

<Table class="w-3/4 text-gray-500 self-center dark:text-gray-400" shadow>
    <TableHead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
        {#each featuresName as feature}
            <TableHeadCell>{feature}</TableHeadCell>
        {/each}
    </TableHead>
    <TableBody tableBodyClass="divide-y">
        <TableBodyRow class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 h-96">
            {#each featuresName as feature}
                <TableBodyCell>
                    <MultiSelect
                            items={behaviours}
                            bind:value={selectedBehaviours[feature]}
                            placeholder="Select behaviours"
                            class="text-gray-700 self-start"
                            on:change={() => updateBehaviours(feature, selectedBehaviours[feature])}
                    />
                </TableBodyCell>
            {/each}
        </TableBodyRow>
    </TableBody>
</Table>
