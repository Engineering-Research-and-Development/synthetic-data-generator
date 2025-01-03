<script>
    import { onMount } from "svelte";
    import {
        Table,
        TableBody,
        TableBodyRow,
        TableBodyCell,
        TableHead,
        TableHeadCell,
        MultiSelect, Button, Modal,
    } from "flowbite-svelte";
    import {ExclamationCircleOutline} from "flowbite-svelte-icons";
    import {goto} from "$app/navigation";

    let behaviours = [
        { value: "Distribution", name: "Distribution" },
        { value: "Threshold", name: "Threshold" },
        { value: "Formula", name: "Formula" },
    ];
    let showCancelPopup = false;
    let featuresName = [];
    let selectedBehaviours = {};

    onMount(() => {
        const features = sessionStorage.getItem("selectedColumns");
        if (features) {
            featuresName = JSON.parse(features);
            featuresName.forEach((feature) => {
                if (!selectedBehaviours[feature]) {
                    selectedBehaviours[feature] = [];
                }
            });
        }
    });

    function updateBehaviours(feature=String, behaviours=String) {
        selectedBehaviours[feature] = behaviours;
        console.log(selectedBehaviours)
    }

    function cancelProcedure(){
        sessionStorage.removeItem('csvFile')
        goto("/")
    }
</script>

<div class="flex items-center justify-center bg-gray-100 dark:bg-gray-900">
    <Table class="w-3/4 text-gray-500 h-screen dark:text-gray-400" shadow>
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
                                class="text-gray-700"
                                on:change={() => updateBehaviours(feature, selectedBehaviours[feature])}
                        />
                    </TableBodyCell>
                {/each}
            </TableBodyRow>
        </TableBody>
    </Table>
    <Button
            type="submit"
            class="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600"
    >
        Next
    </Button>
    <Button
            on:click={() => (showCancelPopup = true)}
            class="text-gray-500 bg-white border border-gray-300 rounded-md px-4 py-2 mr-2 hover:bg-gray-100"
    >
        Cancel
    </Button>
    <Modal bind:open={showCancelPopup} size="xs" autoclose>
        <div class="text-center">
            <ExclamationCircleOutline class="mx-auto mb-4 text-gray-400 w-12 h-12 dark:text-gray-200" />
            <h3 class="mb-5 text-lg font-normal text-gray-500 dark:text-gray-400">This will cause the data loss</h3>
            <Button color="red" class="me-2" on:click={cancelProcedure}>Yes, I'm sure</Button>
            <Button color="alternative">No, cancel</Button>
        </div>
    </Modal>
</div>
