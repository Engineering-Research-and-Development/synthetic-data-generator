<script>
    import { onMount } from "svelte";
    import CancelButton from "../components/CancelButton.svelte";
    import NextButton from "../components/NextButton.svelte";
    import BehaviourTable from "../components/BehaviourTable.svelte";
    import BackButton from "../components/BackButton.svelte";

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

    function submitBehaviours() {
        sessionStorage.setItem('selectedBehaviours', JSON.stringify(selectedBehaviours));
    }
</script>

<h1 class="flex justify-center text-2xl font-bold my-4">Behaviour selection</h1>
<div class="flex items-center justify-center bg-gray-100 dark:bg-gray-900">
    <form on:submit|preventDefault={submitBehaviours}>
        <BehaviourTable
                featuresName={featuresName}
                selectedBehaviours={selectedBehaviours}
                />
        <NextButton/>
        <BackButton/>
        <CancelButton/>
    </form>
</div>
