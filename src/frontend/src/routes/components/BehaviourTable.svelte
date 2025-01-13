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

    type Behaviour = { value: string; name: string };
    type SelectedBehaviours = { [feature: string]: string[] };

    export let featuresName: string[] = [];
    export let selectedBehaviours: SelectedBehaviours = {};

    let fetchedBehaviours: Behaviour[] = [];
    let behaviours: Behaviour[] = [
        { value: "Distribution", name: "Distribution" },
        { value: "Threshold", name: "Threshold" },
        { value: "Formula", name: "Formula" },
        { value: "Randomization", name: "Randomization" },
        { value: "Aggregation", name: "Aggregation" },
        { value: "Normalization", name: "Normalization" },
        { value: "Optimization", name: "Optimization" },
        { value: "Validation", name: "Validation" },
        { value: "Transformation", name: "Transformation" },
        { value: "Segmentation", name: "Segmentation" },
        { value: "Clustering", name: "Clustering" },
        { value: "Prediction", name: "Prediction" },
        { value: "Classification", name: "Classification" },
    ];

    onMount(async () => {
        try {
            const response = await fetch('/api/behaviours');
            if (response.ok) {
                const data: Behaviour[] = await response.json();
                fetchedBehaviours = data;
                behaviours = fetchedBehaviours.length ? fetchedBehaviours : behaviours;
            }
        } catch (error) {
            console.error("Error fetching behaviours:", error);
        }
    });

    export function updateBehaviours(feature: string, behaviours: string[]) {
        selectedBehaviours[feature] = behaviours;
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
    <TableBody tableBodyClass="divide-y">
        <TableBodyRow class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 h-96">
        </TableBodyRow>
    </TableBody>
</Table>
