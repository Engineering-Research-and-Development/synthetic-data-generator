<script lang="ts">
    import { Alert } from 'flowbite-svelte';
    import { InfoCircleSolid } from 'flowbite-svelte-icons';

    export let message: string;
</script>

<Alert color="red" rounded={false} class="border-t-4">
    <InfoCircleSolid slot="icon" class="w-5 h-5" />
    <span class="font-medium">Error</span>
    {message}
</Alert>