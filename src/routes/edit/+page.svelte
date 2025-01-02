<script>
	import {goto} from '$app/navigation';

	let csvContent = sessionStorage.getItem('userFile');
	let lines = csvContent.split('\n').slice(0, 10);
	let headers = lines[0].split(',');
	let selectedColumns = [];

	function handleColumnSelection(event) {
		selectedColumns = Array.from(event.target.selectedOptions, option => option.value);
	}

	function goToSendPage() {
		goto('/send');
	}
</script>

<main>
	<h1>Preview CSV File</h1>
	<p>First 10 lines:</p>
	<pre>{lines.join('\n')}</pre>

	<h2>Select Columns</h2>
	<select multiple on:change={handleColumnSelection}>
		{#each headers as header}
			<option value={header}>{header}</option>
		{/each}
	</select>

	<button on:click={goToSendPage}>Next</button>
</main>