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
    feature: string,
    type: string,
    category: string
};

type AllowedData  = {
    datatype: string
    is_categorical: boolean
}

type NewAlgorithm = {
    id: number;
    name: string;
    description: string;
    default_loss_function: string;
    allowed_data: AllowedData[]
};

type TrainingInfo = {
    loss_function: string;
    train_loss: number;
    val_loss: number;
    train_samples: number;
    val_samples: number;
}
type FeatureSchema = {
    feature_name: string;
    feature_position: number;
    is_categorical: boolean;
    datatype: string;
}

type PreTrainedModel = {
    id: number;
    name: string;
    dataset_name: string;
    input_shape: string;
    algorithm_id: string;
    size: string;
    version_ids: number[];
};

type SelectedModel = {
    id: number;
    name: string;
}

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
    selected_model_id: number;
    new_model: boolean;
    new_model_name: string;
    model_version: string;
}

type SdgOut = {
    additional_rows: number;
    functions: OutFunction[];
    ai_model: AIModel;
    user_file?: object[];
    features_created?: FeaturesCreated[];
}
