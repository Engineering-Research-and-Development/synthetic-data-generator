<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from "$app/navigation";
	import NextButton from "../components/NextButton.svelte";
	import CancelButton from "../components/CancelButton.svelte";
	import FeaturesTable from "../components/FeaturesTable.svelte";
	import Error from "../components/Error.svelte";

	// Define types for table data and functions
	type RowData = { [key: string]: any }; // Represents a row of data with key-value pairs

	let tableData: RowData[] = []; // Array of row data
	let headers: string[] = []; // Array of column headers
	let selectedColumns: string[] = []; // Array of selected column names
	let showAlert: boolean = false; // Control visibility of the Alert

	onMount(() => {
		const savedData = sessionStorage.getItem('userFile');
		if (savedData) {
			try {
				const parsedData: RowData[] = JSON.parse(savedData);
				if (parsedData.length > 0) {
					headers = Object.keys(parsedData[0]);
					tableData = parsedData;
				}
			} catch (error) {
				console.error("Error parsing saved data:", error);
			}
		} else {
			console.error("No data found in sessionStorage.");
		}
	});

	// Toggle a column's selection
	function toggleColumn(column: string): void {
		selectedColumns = selectedColumns.includes(column)
				? selectedColumns.filter(name => name !== column) // Remove column
				: [...selectedColumns, column]; // Add column
	}

	// Submit the selected columns and navigate to the next page
	function submitColumns(): void {
		if (selectedColumns.length === 0) {
			showAlert = true;
			return;
		}
		showAlert = false; // Hide the Alert if columns are selected
		sessionStorage.setItem('selectedColumns', JSON.stringify(selectedColumns));
		goto("/behaviour");
	}
</script>

<h1 class="flex justify-center text-2xl font-bold my-4">Uploaded CSV Data</h1>
<div class="flex items-center justify-center h-screen bg-gray-100 dark:bg-gray-900">
	<form on:submit|preventDefault={submitColumns}>
		{#if showAlert}
			<Error message="Please select at least one column"/>
		{/if}
		<FeaturesTable
				headers={headers}
				tableData={tableData}
				selectedColumns={selectedColumns}
				onToggleColumn={toggleColumn}
		/>
		<div class="flex justify-end gap-4">
			<CancelButton />
			<NextButton />
		</div>
	</form>
</div>