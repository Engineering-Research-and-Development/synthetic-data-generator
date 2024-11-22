<script>
	import { onMount } from 'svelte';

	const endpoint = 'http://localhost:8111/';

	let data = [];
	let selectedValue = '';

	async function fetchModelData() {
		try {
			const response = await fetch(endpoint+"model");
			if (!response.ok) {
				throw new Error('Network response was not ok');
			}
			data = await response.json();
		} catch (error) {
			console.error('Error fetching data:', error);
		}
	}

	onMount(fetchModelData);
</script>

<div>
	<label for="select-data">Select an option:</label>
	<select id="select-data" bind:value={selectedValue}>
		<option value="">-- Select --</option>
		{#each data as item}
			<option value={item.value}>{item.label}</option>
		{/each}
	</select>

	{#if selectedValue}
		<p>You selected: {selectedValue}</p>
	{/if}
</div>