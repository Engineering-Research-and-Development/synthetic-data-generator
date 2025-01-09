<script lang="ts">
	import {
		Table,
		TableBody,
		TableBodyCell,
		TableBodyRow,
		TableHead,
		TableHeadCell,
	} from 'flowbite-svelte';
	import { Button } from 'flowbite-svelte';
	import BackButton from "../components/BackButton.svelte";
	import CancelButton from "../components/CancelButton.svelte";

	// Define types
	type RowData = { [key: string]: any };
	type SelectedBehaviours = { [feature: string]: string[] };
	type FeaturesCreated = { id: number, name: string, featureType: string, subType: string }

	// Variables initialized from sessionStorage
	let selectedColumns: string[] = JSON.parse(sessionStorage.getItem("selectedColumns") || "[]");
	let userFile: RowData[] = JSON.parse(sessionStorage.getItem("userFile") || "[]");
	let additionalRows: number = Number(sessionStorage.getItem("additionalRows")) || 0;
	let selectedBehaviours: SelectedBehaviours = JSON.parse(sessionStorage.getItem("selectedBehaviours") || "{}");
	let newModel: boolean = JSON.parse(sessionStorage.getItem("newModel") || "false");
	let selectedModel: string = sessionStorage.getItem("selectedModel") || "";
	let featuresCreated: FeaturesCreated[] = JSON.parse(sessionStorage.getItem("featuresCreated") || "[]");

	// Data to send
	let postData = {
		featuresCreated,
		selectedColumns,
		userFile,
		additionalRows,
		selectedBehaviours,
		newModel,
		selectedModel,
	};

	// Function to send data with POST
	async function sendData() {
		console.log(JSON.stringify(postData));
		try {
			const response = await fetch("https://example.com/endpoint", {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify(postData),
			});
			if (!response.ok) {
				console.log("An error occurred");
			}
			const result = await response.json();
			console.log("Data sent successfully:", result);
			sessionStorage.clear();
		} catch (error) {
			console.error("Error sending data:", error);
		}
	}

	// Table-specific logic
	let headers: string[] = Object.keys(userFile[0]); // Extract headers from the first row
	let tableData: RowData[] = userFile; // Use userFile as table data
	let maxRowsToShow = 4; // Show only the first 4 rows
</script>

<h1 class="text-2xl font-bold text-center my-6">Review and Send Data</h1>

<div class="flex flex-col gap-6 w-3/4 mx-auto">
	<!-- Selected Columns -->
	<div class="bg-green-200 rounded-lg shadow-md p-6 dark:bg-gray-800">
		<h2 class="text-center text-xl font-semibold mb-4">Selected Columns</h2>
		<ul class="list-disc pl-6">
			{#each selectedColumns as column}
				<li>{column}</li>
			{/each}
		</ul>
	</div>

	<!-- Features Created -->
	{#if featuresCreated}
	<div class="bg-green-200 rounded-lg shadow-md p-6 dark:bg-gray-800">
		<h2 class="text-center text-xl font-semibold mb-4">Features to create</h2>
		<Table class="w-full text-gray-500 dark:text-gray-400" shadow>
			<TableHead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
				{#each featuresCreated as feature}
					<TableHeadCell>
						<span>{feature.name}</span>
					</TableHeadCell>
				{/each}
			</TableHead>
			<TableBody tableBodyClass="divide-y">
				{#each featuresCreated as feature}
					<TableBodyCell class="bg-white border-b dark:bg-gray-800 dark:border-gray-700">
						<TableBodyRow>
							{feature.featureType}
							<br>
							{feature.subType}
						</TableBodyRow>
					</TableBodyCell>
				{/each}
			</TableBody>
		</Table>
	</div>
	{/if}

	<!-- User File Table -->
	{#if tableData}
	<div class="bg-green-200 rounded-lg shadow-md p-6 dark:bg-gray-800">
		<h2 class="text-center text-xl font-semibold mb-4">User File (First {maxRowsToShow} Rows)</h2>
		<Table class="w-full text-gray-500 dark:text-gray-400" shadow>
			<TableHead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
				{#each headers as header}
					<TableHeadCell>
						<span>{header}</span>
					</TableHeadCell>
				{/each}
			</TableHead>
			<TableBody tableBodyClass="divide-y">
				{#each tableData.slice(0, maxRowsToShow) as row}
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
	</div>
	{/if}

	<!-- Additional Rows -->
	<div class="bg-green-200 rounded-lg shadow-md p-6 dark:bg-gray-800">
		<h2 class="text-center text-xl font-semibold mb-4">Additional Rows</h2>
		<p>{additionalRows}</p>
	</div>

	<!-- Selected Behaviours -->
	<div class="bg-green-200 rounded-lg shadow-md p-6 dark:bg-gray-800">
		<h2 class="text-center text-xl font-semibold mb-4">Selected Behaviours</h2>
		<ul class="list-disc pl-6">
			{#each Object.entries(selectedBehaviours) as [feature, behaviours]}
				<li>
					<strong>{feature}:</strong>
					<ul class="list-circle pl-6">
						{#each behaviours as behaviour}
							<li>{behaviour}</li>
						{/each}
					</ul>
				</li>
			{/each}
		</ul>
	</div>

	<!-- New Model -->
	<div class="bg-green-200 rounded-lg shadow-md p-6 dark:bg-gray-800">
		<h2 class="text-center text-xl font-semibold mb-4">New Model</h2>
		<p>{newModel ? "Yes" : "No"}</p>
	</div>

	<!-- Selected Model -->
	<div class="bg-green-200 rounded-lg shadow-md p-6 dark:bg-gray-800">
		<h2 class="text-center text-xl font-semibold mb-4">Selected Model</h2>
		<p>{selectedModel}</p>
	</div>

	<!-- Send Button -->
	<div class="flex justify-end gap-4">
		<BackButton/>
		<CancelButton />
		<Button color="blue" on:click={sendData}>Send</Button>
	</div>
</div>