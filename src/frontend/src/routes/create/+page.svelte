<script lang="ts">
	import { Section, TableHeader } from "flowbite-svelte-blocks";
	import { Button, Select } from "flowbite-svelte";
	import { CircleMinusSolid } from "flowbite-svelte-icons";
	import BackButton from "../components/BackButton.svelte";
	import CancelButton from "../components/CancelButton.svelte";
	import NextButton from "../components/NextButton.svelte";
	import { goto } from "$app/navigation";

	let features: Array<{ id: number, name: string, featureType: string, subType: string }> = [];
	let types = [
		{ value: 'String', name: 'String' },
		{ value: 'Integer', name: 'Integer' },
		{ value: 'Integer', name: 'Float' },
		{ value: 'Double', name: 'Double' },
	];
	let subTypes = [
		{ value: 'Continuous', name: "Continuous" },
		{ value: 'Categorical', name: "Categorical" }
	];

	// Function to add a new feature row
	function addFeature() {
		features = [...features, { id: features.length + 1, name: '', featureType: '', subType: '' }];
	}

	// Function to remove a feature row by its index
	function removeFeature(index: number) {
		features = features.filter((_, i) => i !== index);
	}

	// Function to handle the form submission
	function submit(event: Event) {
		event.preventDefault(); // Prevent the default form submission behavior
		const featureNames = features.map(feature => feature.name);
		const featuresCreated = features.map(feature => ({
			name: feature.name,
			featureType: feature.featureType,
			subType: feature.subType
		}));

		sessionStorage.setItem("selectedColumns", JSON.stringify(featureNames))
		sessionStorage.setItem("featuresCreated", JSON.stringify(featuresCreated))
		goto("/behaviour")
	}
</script>

<form on:submit={submit}>
	<Section name="tableheader" sectionClass="bg-gray-50 dark:bg-gray-900 h-80 flex pt-8">
		<TableHeader>
			<Button type="button" on:click={addFeature}>
				<svg class="h-3.5 w-3.5 mr-2" fill="currentColor" aria-hidden="true">
					<path clip-rule="evenodd" fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" />
				</svg>
				Add feature
			</Button>
		</TableHeader>

		<!-- Feature Input Rows -->
		<div class="w-full p-4">
			{#each features as feature, index}
				<div class="flex gap-4 mb-4 items-center">
					<!-- Delete button with minus icon -->
					<Button type="button" on:click={() => removeFeature(index)} color="red" class="p-2">
						<CircleMinusSolid class="h-5 w-5" />
					</Button>
					<input
							type="text"
							class="w-1/2 p-2 border rounded"
							placeholder="Feature Name"
							bind:value={feature.name}
							required
					/>
					<Select
							bind:value={feature.featureType}
							class="w-1/2 p-2 border rounded"
							required
					>
						{#each types as t}
							<option value={t.value}>{t.name}</option>
						{/each}
					</Select>
					<Select
							bind:value={feature.subType}
							class="w-1/2 p-2 border rounded"
							required
					>
						{#each subTypes as t}
							<option value={t.value}>{t.name}</option>
						{/each}
					</Select>
				</div>
			{/each}
		</div>
	</Section>

	<div class="flex justify-end gap-4">
		<BackButton />
		<CancelButton />
		<NextButton />
	</div>
</form>