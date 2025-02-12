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
    let selectedModel: string = "";
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


    onMount(async () => {
        userFile = JSON.parse(sessionStorage.getItem("userFile") || "{}");
        additionalRows = Number(sessionStorage.getItem("additionalRows")) || 0;
        functionData = JSON.parse(sessionStorage.getItem("functionData") || "{}");
        newModel = JSON.parse(sessionStorage.getItem("newModel") || "false");
        selectedModel = sessionStorage.getItem("selectedModel") || "";
        selectedVersion = Number(sessionStorage.getItem("selectedVersion")) || 0;
        featuresCreated = JSON.parse(sessionStorage.getItem("featuresCreated") || "[]");

        console.log(generateOutFunctions(functionData))
    });

    async function sendData() {
        let postData = {
            featuresCreated,
            userFile,
            additionalRows,
            functionData,
            newModel,
            selectedVersion,
            selectedModel,
        };

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