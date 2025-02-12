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

type NewAlgorithm = {
    id: number;
    name: string;
    description: string;
    default_loss_function: string;
};

type PreTrainedModel = {
    id: number;
    name: string;
    dataset_name: string;
    input_shape: string;
    algorithm_id: string;
    size: string;
    version_ids: number[];
};


type OutParameter = {
    param_id: number;
    value: number;
}

type OutFunction = {
    feature: string;
    function_id: number;
    parameters: OutParameter[];
}

type AIModel = {
    selected_model: number;
    new_model: boolean;
    new_model_name: string;
    model_version: string;
}

type SdgOut = {
    additional_rows: number;
    functions: OutFunction[];
    ai_model: AIModel;
    user_file?: object[];
    features_created?: string[];
}
