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
	import {goto} from "$app/navigation";
	type RowData = { [key: string]: any };

	let userFile: RowData[] = [];
	let additionalRows: number = 0;
	let functionData: Record<string, Array<{
		functionName: string;
		parameters: Array<Parameter>
	}>> = {};
	let newModel: boolean = false;
	let selectedModel: SelectedModel | null = null;
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
		additionalRows = Number(sessionStorage.getItem("additionalRows")) || 0;
		functionData = JSON.parse(sessionStorage.getItem("functionData") || "{}");
		newModel = JSON.parse(sessionStorage.getItem("newModel") || "false");
		selectedModel = JSON.parse(sessionStorage.getItem("selectedModel") || "");
		selectedVersion = Number(sessionStorage.getItem("selectedVersion")) || 0;
		featuresCreated = JSON.parse(sessionStorage.getItem("featuresCreated") || "[]");
	});


	function sendData() {
		goto("/send")
	}
</script>

<h1 class="text-2xl font-bold text-center my-6">Review and Send Data</h1>

<div class="flex flex-col gap-6 w-3/4 mx-auto">

	<!-- Features Created -->
	{#if featuresCreated.length>0}
	<div class="bg-green-200 rounded-lg shadow-md p-6 dark:bg-gray-800">
		<h2 class="text-center text-xl font-semibold mb-4">Features to create</h2>
		<Table class="w-full text-gray-500 dark:text-gray-400" shadow>
			<TableHead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
				{#each featuresCreated as feature}
					<TableHeadCell>
						{feature.feature}
					</TableHeadCell>
				{/each}
			</TableHead>
			<TableBody tableBodyClass="divide-y">
				{#each featuresCreated as feature}
					<TableBodyCell class="bg-white border-b dark:bg-gray-800 dark:border-gray-700">
						<TableBodyRow>
							{feature.type}
							<br>
							{feature.category}
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

	<!-- Selected Functions -->
	<div class="bg-green-200 rounded-lg shadow-md p-6 dark:bg-gray-800">
		<h2 class="text-center text-xl font-semibold mb-4">Selected Functions</h2>

		{#if Object.keys(functionData).length > 0}
			<Table class="w-full text-gray-500 dark:text-gray-400" shadow>
				<TableHead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
					<TableHeadCell>Feature</TableHeadCell>
					<TableHeadCell>Function Name</TableHeadCell>
					<TableHeadCell>Parameters</TableHeadCell>
				</TableHead>
				<TableBody tableBodyClass="divide-y">
					{#each Object.entries(functionData) as [feature, functionParameter]}
						{#each functionParameter as func, index}
							<TableBodyRow class="bg-white border-b dark:bg-gray-800 dark:border-gray-700">
								{#if index === 0}
									<TableBodyCell rowspan={functionParameter.length} class="font-semibold">{feature}</TableBodyCell>
								{/if}
								<TableBodyCell>{func.functionName}</TableBodyCell>
								<TableBodyCell>
									<ul class="list-disc pl-6">
										{#each func.parameters as param}
											<li>
												<strong>{param.name}:</strong> {param.value}
											</li>
										{/each}
									</ul>
								</TableBodyCell>
							</TableBodyRow>
						{/each}
					{/each}
				</TableBody>
			</Table>
		{:else}
			<p class="text-center text-gray-700 dark:text-gray-300">No Functions selected or data available.</p>
		{/if}
	</div>



	<!-- New Model -->
	<div class="bg-green-200 rounded-lg shadow-md p-6 dark:bg-gray-800">
		<h2 class="text-center text-xl font-semibold mb-4">New Model</h2>
		<p>{newModel ? "Yes" : "No"}</p>
	</div>

	<!-- Selected Model -->
	<div class="bg-green-200 rounded-lg shadow-md p-6 dark:bg-gray-800">
		<h2 class="text-center text-xl font-semibold mb-4">Selected Model</h2>
		{#if selectedModel}
			<p>{selectedModel.name}
			{#if (!newModel)}
				Version {selectedVersion}
			{/if}
			</p>
		{/if}
	</div>

	<!-- Send Button -->
	<div class="flex justify-end gap-4">
		<BackButton/>
		<CancelButton />
		<Button color="blue" on:click={sendData}>Send</Button>
	</div>
</div>