<script lang="ts">
    import { Label, Select } from 'flowbite-svelte';
    import {onMount} from "svelte";

    export let selected: string;
    let fetchedNewModels = [];

    let newModels = [
        { value: 'us', name: 'United States' },
        { value: 'ca', name: 'Canada' },
        { value: 'fr', name: 'France' }
    ];

    onMount(async () => {
        try {
            const response = await fetch('/api/newModels');
            if (response.ok) {
                fetchedNewModels = await response.json();
                newModels = fetchedNewModels.length ? fetchedNewModels : newModels;
            }
        } catch (error) {
            console.error("Error fetching behaviours:", error);
        }
    });
</script>

<Label>
    Select an option
    <Select class="mt-2" items={newModels} bind:value={selected} />
</Label>