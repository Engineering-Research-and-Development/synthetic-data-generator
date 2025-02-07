type AIFunction = {
    id: number;
    name: string;
    description: string;
    function_reference: string;
};

type Parameter = {
    id: number;
    name: string;
    value: string;
    parameter_type: "float" | "int";
};

type FunctionParameter = {
    function: AIFunction;
    parameter: Parameter[];
};


type FeatureFunction = {
    [feature: string]: string[]
};

type FeaturesCreated = {
    id: number,
    name: string,
    featureType: string,
    subType: string
};

type BuiltInModel = {
    id: number;
    name: string;
    description: string;
    loss_function: string;
    allowed_datatype: string[];
    is_categorical: boolean[];
};

type PreTrainedModel = {
    name: string;
    id: number;
    dataset_name: string;
    input_shape: string;
    algorithm_name: string;
    size: string;
    version_ids: number[];
};

type SelectedModel ={
    id: number;
    name: string;
    version: number;
}