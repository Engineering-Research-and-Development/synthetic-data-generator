<script lang="ts">
	import { Section, TableHeader } from "flowbite-svelte-blocks";
	import {
		Button,
		Search,
		Select
	} from "flowbite-svelte";
	import { ChevronDownOutline, CircleMinusSolid } from "flowbite-svelte-icons";

	let features: Array<{ id: number, name: string, featureType: string, subType: string}> = [];
	let types = [
		{ value: 'str', name: 'String' },
		{ value: 'int', name: 'Integer' },
		{ value: 'flt', name: 'Float' },
		{ value: 'dbl', name: 'Double' },
	]
	let subTypes= [
		{value: 'cont', name: "Continuous"},
		{value: 'cat', name: "Categorical"}
	]

	// Function to add a new product row
	function addFeature() {
		features = [...features, { id: features.length + 1, name: '', featureType: '', subType: '' }];
	}

	// Function to remove a feature row by its index
	function removeFeature(index: number) {
		features = features.filter((_, i) => i !== index);
	}
</script>

<Section name="tableheader" sectionClass="bg-gray-50 dark:bg-gray-900 h-80 flex pt-8">
	<TableHeader headerType="search">
		<Search slot="search" size="md" />
		<Button on:click={addFeature}>
			<svg class="h-3.5 w-3.5 mr-2" fill="currentColor" viewbox="0 0 20 20" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
				<path clip-rule="evenodd" fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" />
			</svg>
			Add feature
		</Button>
		<Button color="light">
			Actions<ChevronDownOutline />
		</Button>
	</TableHeader>

	<!-- Product Input Rows -->
	<div class="w-full p-4">
		{#each features as product, index}
			<div class="flex gap-4 mb-4 items-center">
				<!-- Delete button with minus icon -->
				<Button on:click={() => removeFeature(index)} color="red" class="p-2">
					<CircleMinusSolid class="h-5 w-5" />
				</Button>
				<input
						type="text"
						class="w-1/2 p-2 border rounded"
						placeholder="Feature Name"
						value={product.name}
				/>
				<Select
						bind:value={features[index].featureType}
						class="w-1/2 p-2 border rounded"
				>
					{#each types as t}
						<option value={t.value}>{t.name}</option>
					{/each}
				</Select>
				<Select
						bind:value={features[index].subType}
						class="w-1/2 p-2 border rounded"
				>
					{#each subTypes as t}
						<option value={t.value}>{t.name}</option>
					{/each}
				</Select>
			</div>
		{/each}
	</div>
</Section>
