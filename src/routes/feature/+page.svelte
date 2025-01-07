<script>
	import { onMount } from 'svelte';
	import {goto} from "$app/navigation";
	import NextButton from "../components/NextButton.svelte";
	import CancelButton from "../components/CancelButton.svelte";
	import FeaturesTable from "../components/FeaturesTable.svelte";

	let tableData = [];
	let headers = [];
	let selectedColumns = [];

	onMount(() => {
		const savedData = sessionStorage.getItem('userFile');
		if (savedData) {
			const parsedData = JSON.parse(savedData);
			if (parsedData.length > 0) {
				headers = Object.keys(parsedData[0]);
				tableData = parsedData;
			}
		} else {
			console.error("No data found in sessionStorage.");
		}
	});

	function toggleColumn(column= String) {
		selectedColumns = selectedColumns.includes(column)
				? selectedColumns.filter(name => name !== column) // Remove column
				: [...selectedColumns, column]; // Add column
	}

	function submitColumns(){
		sessionStorage.setItem('selectedColumns', JSON.stringify(selectedColumns))
		goto("/behaviour")
	}

</script>

<h1 class="flex justify-center text-2xl font-bold my-4">Uploaded CSV Data</h1>
<div class="flex items-center justify-center h-screen bg-gray-100 dark:bg-gray-900">
	<form on:submit|preventDefault={submitColumns}>
		<FeaturesTable
			headers={headers}
			tableData={tableData}
			selectedColumns={selectedColumns}
			onToggleColumn={toggleColumn} />
		<NextButton/>
		<CancelButton/>
	</form>
</div>
