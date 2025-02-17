<script lang="ts">
    import {BACKEND_URL} from "../../stores/shared";
    import {onMount} from "svelte";

    type RowData = { [key: string]: any };

    let userFile: RowData[] = [];
    let additionalRows: number = 0;
    let functionData: Record<string, Array<{
        functionId: number;
        functionName: string;
        parameters: Array<Parameter>
    }>> = {};
    let newModel: boolean = false;
    let selectedModel: SelectedModel;
    let selectedVersion: number = 0;
    let featuresCreated: FeaturesCreated[] = [];

    function generateOutFunctions(featureFunctions: Record<string, { functionName: string; functionId: number,parameters: Parameter[] }[]>): OutFunction[] {
        let outFunctions: OutFunction[] = [];

        for (const [feature, functions] of Object.entries(featureFunctions)) {
            functions.forEach((func) => {
                const parameters: OutParameter[] = func.parameters.map(param => ({
                    param_id: param.id,
                    value: parseFloat(param.value)
                }));

                outFunctions.push({
                    feature: feature,
                    function_id: func.functionId,
                    parameters: parameters
                });
            });
        }

        return outFunctions;
    }

    function generateAiModel(newModel: boolean, selectedVersion: number, newModelName: string, selectedModelId: number): AIModel{
        return {
            selected_model_id: selectedModelId,
            model_version: selectedVersion.toString(),
            new_model: newModel,
            new_model_name: newModelName
        }
    }

    onMount(async () => {
        additionalRows = Number(sessionStorage.getItem("additionalRows")) || 0;
        functionData = JSON.parse(sessionStorage.getItem("functionData") || "{}");
        newModel = JSON.parse(sessionStorage.getItem("newModel") || "false");
        selectedModel = JSON.parse(sessionStorage.getItem("selectedModel") || "");
        selectedVersion = Number(sessionStorage.getItem("selectedVersion")) || 0;
        userFile = JSON.parse(sessionStorage.getItem("userFile") || "{}");
        featuresCreated = JSON.parse(sessionStorage.getItem("featuresCreated") || "[]");
        await sendData()
    });

    async function sendData() {
        let postData: SdgOut = {
            additional_rows: additionalRows,
            functions: generateOutFunctions(functionData),
            ai_model: generateAiModel(newModel, selectedVersion, "test_name", selectedModel.id),
        };

        if (userFile.length>0) {
            postData["user_file"]= userFile
        }
        if (featuresCreated.length>0) {
            postData["features_created"] = featuresCreated
        }

        console.log(JSON.stringify(postData));
        try {
            const response = await fetch(`${BACKEND_URL}/sdg_input`, {
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