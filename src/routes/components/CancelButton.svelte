<script>
    import {Button, Modal} from "flowbite-svelte";
    import {ExclamationCircleOutline} from "flowbite-svelte-icons";
    import {goto} from "$app/navigation";

    let showCancelPopup = false;

    function cancelProcedure(){
        sessionStorage.removeItem('csvFile')
        sessionStorage.removeItem("selectedColumns");
        goto("/")
    }

</script>

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