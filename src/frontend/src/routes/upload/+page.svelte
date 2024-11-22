<script>
	import { goto } from '$app/navigation';

	let file;

	async function handleFileChange(event) {
		file = event.target.files[0];
		if (file) {
			// Store the file in memory (using localStorage for simplicity)
			const reader = new FileReader();
			reader.onload = () => {
				localStorage.setItem('csvFile', reader.result);
				goto('/preview');
			};
			reader.readAsText(file);
		}
	}
</script>

<main>
	<h1>Upload CSV File</h1>
	<input type="file" accept=".csv" on:change={handleFileChange} />
</main>