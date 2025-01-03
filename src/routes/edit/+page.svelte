<script>
	import {
		Table,
		TableBody,
		TableBodyCell,
		TableBodyRow,
		TableHead,
		TableHeadCell,
		Checkbox,
		Button, Modal
	} from 'flowbite-svelte';

	import { onMount } from 'svelte';
	import {ExclamationCircleOutline} from "flowbite-svelte-icons";
	import {goto} from "$app/navigation";

	let tableData = [];
	let headers = [];
	let selectedColumns = [];
	let showCancelPopup = false;

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
		goto("/features")
	}

	function cancelProcedure(){
		sessionStorage.removeItem('csvFile')
		goto("/")
	}

</script>

<h1 class="flex justify-center text-2xl font-bold my-4">Uploaded CSV Data</h1>
<div class="flex items-center justify-center h-screen bg-gray-100 dark:bg-gray-900">
	<form on:submit|preventDefault={submitColumns}>
		<Table class="w-3/4 text-gray-500 dark:text-gray-400" shadow>
			<TableHead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
				{#each headers as header}
					<TableHeadCell>
						<div class="flex items-center space-x-2">
							<Checkbox
									checked={selectedColumns.includes(header)}
									on:change={() => toggleColumn(header)}
							/>
							<span>{header}</span>
						</div>
					</TableHeadCell>
				{/each}
			</TableHead>
			<TableBody tableBodyClass="divide-y">
				{#each tableData.slice(0, 10) as row}
					<TableBodyRow class="bg-white border-b dark:bg-gray-800 dark:border-gray-700">
						{#each headers as header}
							<TableBodyCell>
								{row[header]}
							</TableBodyCell>
						{/each}
					</TableBodyRow>
				{/each}
			</TableBody>
		</Table>

		<Button
				type="submit"
				class="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600"
		>
			Next
		</Button>
		<Button
				on:click={() => (showCancelPopup = true)}
				class="text-gray-500 bg-white border border-gray-300 rounded-md px-4 py-2 mr-2 hover:bg-gray-100"
		>
			Cancel
		</Button>
		<Modal bind:open={showCancelPopup} size="xs" autoclose>
			<div class="text-center">
				<ExclamationCircleOutline class="mx-auto mb-4 text-gray-400 w-12 h-12 dark:text-gray-200" />
				<h3 class="mb-5 text-lg font-normal text-gray-500 dark:text-gray-400">This will cause the data loss</h3>
				<Button color="red" class="me-2" on:click={cancelProcedure}>Yes, I'm sure</Button>
				<Button color="alternative">No, cancel</Button>
			</div>
		</Modal>
	</form>
</div>
