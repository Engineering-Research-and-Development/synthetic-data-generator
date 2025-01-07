<script lang="ts">
	import { Section, TableHeader } from "flowbite-svelte-blocks";
	import { Button, Search, Dropdown, DropdownItem, DropdownDivider, Checkbox } from "flowbite-svelte";
	import { ChevronDownOutline } from "flowbite-svelte-icons";

	// Array to store product data
	let products: Array<{ id: number, name: string, price: number }> = [];

	// Function to add a new product row
	function addProduct() {
		products = [...products, { id: products.length + 1, name: '', price: 0 }];
	}

	// Function to handle input changes
	function handleInputChange(event: Event, index: number, field: 'name' | 'price') {
		const target = event.target as HTMLInputElement;
		products[index][field] = field === 'price' ? parseFloat(target.value) : target.value;
		products = products; // Trigger reactivity
	}
</script>

<Section name="tableheader" sectionClass="bg-gray-50 dark:bg-gray-900 h-80 flex pt-8">
	<TableHeader headerType="search">
		<Search slot="search" size="md" />
		<Button on:click={addProduct}>
			<svg class="h-3.5 w-3.5 mr-2" fill="currentColor" viewbox="0 0 20 20" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
				<path clip-rule="evenodd" fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" />
			</svg>
			Add product
		</Button>
		<Button color="light">
			Actions<ChevronDownOutline />
		</Button>
		<Dropdown>
			<DropdownItem>Mass Edit</DropdownItem>
			<DropdownDivider />
			<DropdownItem>Delete all</DropdownItem>
		</Dropdown>
		<Button color="light">
			<svg xmlns="http://www.w3.org/2000/svg" aria-hidden="true" class="w-4 h-4 mr-2 text-gray-400" viewbox="0 0 20 20" fill="currentColor">
				<path fill-rule="evenodd" d="M3 3a1 1 0 011-1h12a1 1 0 011 1v3a1 1 0 01-.293.707L12 11.414V15a1 1 0 01-.293.707l-2 2A1 1 0 018 17v-5.586L3.293 6.707A1 1 0 013 6V3z" clip-rule="evenodd" />
			</svg>
			Filter<ChevronDownOutline />
		</Button>
		<Dropdown class="w-48 p-2 text-sm">
			<h6 class="mb-3 ml-1 text-sm font-medium text-gray-900 dark:text-white">Category</h6>
			<li class="rounded p-1 hover:bg-gray-100 dark:hover:bg-gray-600">
				<Checkbox>Apple (56)</Checkbox>
			</li>
			<li class="rounded p-1 hover:bg-gray-100 dark:hover:bg-gray-600">
				<Checkbox>Fitbit (56)</Checkbox>
			</li>
			<li class="rounded p-1 hover:bg-gray-100 dark:hover:bg-gray-600">
				<Checkbox checked>Dell (56)</Checkbox>
			</li>
			<li class="rounded p-1 hover:bg-gray-100 dark:hover:bg-gray-600">
				<Checkbox>Asus (97)</Checkbox>
			</li>
		</Dropdown>
	</TableHeader>

	<!-- Product Input Rows -->
	<div class="w-full p-4">
		{#each products as product, index}
			<div class="flex gap-4 mb-4">
				<input
						type="text"
						class="w-1/2 p-2 border rounded"
						placeholder="Product Name"
						value={product.name}
						on:input={(event) => handleInputChange(event, index, 'name')}
				/>
				<input
						type="number"
						class="w-1/2 p-2 border rounded"
						placeholder="Price"
						value={product.price}
						on:input={(event) => handleInputChange(event, index, 'price')}
				/>
			</div>
		{/each}
	</div>
</Section>