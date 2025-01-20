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
	import {onMount} from "svelte";


	// Define types
	type RowData = { [key: string]: any };

	let selectedColumns: string[] = [];
	let userFile: RowData[] = [];
	let additionalRows: number = 0;
	let selectedBehaviours: FeatureBehaviour = {};
	let newModel: boolean = false;
	let selectedModel: string = "";
	let selectedVersion: number = 0;
	let featuresCreated: FeaturesCreated[] = [];
	let headers: string[] = [];
	let tableData: RowData[] = [];
	let maxRowsToShow = 4;

	async function loadUserFile(): Promise<void> {
		try {
			const userFileData = sessionStorage.getItem("userFile");
			userFile = userFileData ? JSON.parse(userFileData) : [];
			headers = Object.keys(userFile[0]); // Extract headers from the first row
			tableData = userFile
		} catch (error) {
			userFile = [];
		}
}

	onMount(async () => {
		await loadUserFile();
		selectedColumns = JSON.parse(sessionStorage.getItem("selectedColumns") || "[]");
		additionalRows = Number(sessionStorage.getItem("additionalRows")) || 0;
		selectedBehaviours = JSON.parse(sessionStorage.getItem("selectedBehaviours") || "{}");
		newModel = JSON.parse(sessionStorage.getItem("newModel") || "false");
		selectedModel = sessionStorage.getItem("selectedModel") || "";
		selectedVersion = Number(sessionStorage.getItem("selectedVersion")) || 0;
		featuresCreated = JSON.parse(sessionStorage.getItem("featuresCreated") || "[]");
	});


	let postData = {
		featuresCreated,
		selectedColumns,
		userFile,
		additionalRows,
		selectedBehaviours,
		newModel,
		selectedVersion,
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
	{#if featuresCreated.length>0}
	<div class="bg-green-200 rounded-lg shadow-md p-6 dark:bg-gray-800">
		<h2 class="text-center text-xl font-semibold mb-4">Features to create</h2>
		<Table class="w-full text-gray-500 dark:text-gray-400" shadow>
			<TableHead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
				{#each featuresCreated as feature}
					<TableHeadCell>
						{feature.name}
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

	{:else}
	<!-- User File Table -->
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
		<p>{selectedModel}
		{#if (!newModel)}
			Version {selectedVersion}
		{/if}
		</p>
	</div>

	<!-- Send Button -->
	<div class="flex justify-end gap-4">
		<BackButton/>
		<CancelButton />
		<Button color="blue" on:click={sendData}>Send</Button>
	</div>
</div>