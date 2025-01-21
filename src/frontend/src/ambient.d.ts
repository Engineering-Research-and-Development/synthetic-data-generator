type FunctionParameter = {
    name: string;
    type: string;
    value: number;
};

type Behaviour = {
    id: number;
    name: string;
    description: string;
    function_reference: string;
    function_parameters: FunctionParameter[];
};

type FeatureBehaviour = {
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