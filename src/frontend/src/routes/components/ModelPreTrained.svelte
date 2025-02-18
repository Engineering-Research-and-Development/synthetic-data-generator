<script lang="ts">
    import { Label, Select, Table, TableHead, TableBody, TableBodyCell, TableBodyRow, TableHeadCell } from 'flowbite-svelte';
    import { onMount } from 'svelte';
    import {BACKEND_URL} from "../../stores/shared";
    import Error from "./Error.svelte";

    export let trainedModels:PreTrainedModel[];
    export let selectedModel: SelectedModel;
    export let selectedVersion: number;

    let chosenModel: string;
    let fetchedPreTrainedModels: PreTrainedModel[] = [];

    let models: typeof fetchedPreTrainedModels[number] | null = null;
    let selectedVersionLabel: { value: number; name: string }[] = [];
    let newModels: { value: string; name: string }[] = [];

    let trainingInfo: TrainingInfo | null = null;
    let featureSchema: FeatureSchema[] = [];
    let errorMessage:string;

    onMount(async () => {
        try {
            newModels = trainedModels.map((model) => ({
                value: model.name,
                name: model.name
            }));
        } catch (error) {
            errorMessage='Error fetching trained models:' + error;
        }
    });

    $: {
        models = trainedModels.find((model) => model.name === chosenModel) || null;
        selectedVersionLabel = models ? models.version_ids.map((id) => ({value: id, name: `Version ${id}`})) : [];
        if (selectedVersion && models) {
            fetchTrainingInfoAndFeatureSchema();
            selectedModel ={id: models.id, name:models.name}
        }
    }

    async function fetchTrainingInfoAndFeatureSchema() {
        try {
            // Use the selected model's ID in the fetch URL
            const response = await fetch(BACKEND_URL +`/trained_models/${models?.id}?include_versions=true&${selectedVersion}`);
            const data = await response.json();

            if (data.training_info) {
                trainingInfo = data.training_info as TrainingInfo;
            }

            if (data.feature_schema) {
                featureSchema = data.feature_schema as FeatureSchema[];
            }
        } catch (error) {
            errorMessage='Error fetching training info and feature schema:'+ error;
        }
    }
</script>


{#if errorMessage}
    <Error message={errorMessage}/>
{/if}

<div class="w-full">
    <!-- Dropdown for model selection -->
    <div class="w-full">
        <Label>
            Select a model
            <Select class="mt-2" items={newModels} bind:value={chosenModel} />
        </Label>
    </div>

    <!-- Label list for selecting version_id -->
    <div class="w-full">
        <Label>
            Available Version IDs:
            <Select class="mt-2" items={selectedVersionLabel} bind:value={selectedVersion} />
        </Label>
    </div>

    <!-- Table to display selected model details -->
    <div class="w-full mt-8">
        {#if models}
            <Table>
                <TableHead>
                    <TableHeadCell class="font-bold">Property</TableHeadCell>
                    <TableHeadCell class="font-bold">Value</TableHeadCell>
                </TableHead>
                <TableBody>
                    <TableBodyRow>
                        <TableBodyCell>Name</TableBodyCell>
                        <TableBodyCell>{models.name}</TableBodyCell>
                    </TableBodyRow>
                    <TableBodyRow>
                        <TableBodyCell>Dataset Name</TableBodyCell>
                        <TableBodyCell>{models.dataset_name}</TableBodyCell>
                    </TableBodyRow>
                    <TableBodyRow>
                        <TableBodyCell>Input Shape</TableBodyCell>
                        <TableBodyCell>{models.input_shape}</TableBodyCell>
                    </TableBodyRow>
                    <TableBodyRow>
                        <TableBodyCell>Algorithm</TableBodyCell>
                        <TableBodyCell>{models.algorithm_id}</TableBodyCell>
                    </TableBodyRow>
                    <TableBodyRow>
                        <TableBodyCell>Size</TableBodyCell>
                        <TableBodyCell>{models.size}</TableBodyCell>
                    </TableBodyRow>

                    <!-- Display Training Info -->
                    {#if trainingInfo}
                        <TableBodyRow>
                            <TableBodyCell>Loss Function</TableBodyCell>
                            <TableBodyCell>{trainingInfo.loss_function}</TableBodyCell>
                        </TableBodyRow>
                        <TableBodyRow>
                            <TableBodyCell>Train Loss</TableBodyCell>
                            <TableBodyCell>{trainingInfo.train_loss}</TableBodyCell>
                        </TableBodyRow>
                        <TableBodyRow>
                            <TableBodyCell>Validation Loss</TableBodyCell>
                            <TableBodyCell>{trainingInfo.val_loss}</TableBodyCell>
                        </TableBodyRow>
                        <TableBodyRow>
                            <TableBodyCell>Train Samples</TableBodyCell>
                            <TableBodyCell>{trainingInfo.train_samples}</TableBodyCell>
                        </TableBodyRow>
                        <TableBodyRow>
                            <TableBodyCell>Validation Samples</TableBodyCell>
                            <TableBodyCell>{trainingInfo.val_samples}</TableBodyCell>
                        </TableBodyRow>
                    {/if}

                    <!-- Display Feature Schema -->
                    {#if featureSchema.length > 0}
                        {#each featureSchema as feature}
                            <TableBodyRow>
                                <TableBodyCell>Feature Name</TableBodyCell>
                                <TableBodyCell>{feature.feature_name}</TableBodyCell>
                            </TableBodyRow>
                            <TableBodyRow>
                                <TableBodyCell>Feature Position</TableBodyCell>
                                <TableBodyCell>{feature.feature_position}</TableBodyCell>
                            </TableBodyRow>
                            <TableBodyRow>
                                <TableBodyCell>Is Categorical</TableBodyCell>
                                <TableBodyCell>{feature.is_categorical ? 'Yes' : 'No'}</TableBodyCell>
                            </TableBodyRow>
                            <TableBodyRow>
                                <TableBodyCell>Data Type</TableBodyCell>
                                <TableBodyCell>{feature.datatype}</TableBodyCell>
                            </TableBodyRow>
                        {/each}
                    {/if}
                </TableBody>
            </Table>
        {:else}
            <p class="text-gray-500">Please select a model from the dropdown.</p>
        {/if}
    </div>
</div>