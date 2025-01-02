<script>
	import { onMount } from 'svelte';

	let csvContent = localStorage.getItem('csvFile');
	let selectedColumns = JSON.parse(localStorage.getItem('selectedColumns'));

	onMount(async () => {
		const response = await fetch('https://external-endpoint.com/upload', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				csvContent,
				selectedColumns
			})
		});

		if (response.ok) {
			alert('File sent successfully!');
		} else {
			alert('Failed to send file.');
		}
	});
</script>

<main>
	<h1>Sending Data...</h1>
</main>