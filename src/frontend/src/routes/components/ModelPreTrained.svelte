<script lang="ts">
    import { Label, Select } from 'flowbite-svelte';
    import {onMount} from "svelte";

    export let selected: string;
    let existingModels = [];

    let newModels = [
        { value: 'us', name: 'United States' },
        { value: 'ca', name: 'Canada' },
        { value: 'fr', name: 'France' }
    ];

    onMount(async () => {
        try {
            const response = await fetch('/api/existingModels');
            if (response.ok) {
                existingModels = await response.json();
                newModels = existingModels.length ? existingModels : newModels;
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