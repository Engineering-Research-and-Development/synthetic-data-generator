from peewee import fn, JOIN

from database.schema import (
    TrainedModel,
    TrainingInfo,
    ModelVersion,
    TrainModelDatatype,
    DataType,
    Algorithm,
)
from database.validation_schema import (
    TrainedModelAndVersionIds,
    TrainedModelAndVersions as PydanticTrainedModelAndVersions,
    ModelVersionAndTrainInfo,
    ModelVersion as PydanticModelVersion,
    TrainingInfo as PydanticTrainingInfo,
)


def get_trained_model_versions(
    model_id, version_id=None, include_training_info: bool = False
) -> PydanticTrainedModelAndVersions:
    if version_id is None:
        query = ModelVersion.select().where(ModelVersion.trained_model_id == model_id)
    else:
        query = (
            ModelVersion.select()
            .where(ModelVersion.trained_model_id == model_id)
            .where(ModelVersion.id == version_id)
        )

    versions = [PydanticModelVersion(**row) for row in query.dicts()]

    # Now we get the features
    train_and_features = (
        (
            TrainedModel.select(
                TrainedModel,
                fn.JSON_AGG(
                    fn.JSON_BUILD_OBJECT(
                        "feature_name",
                        TrainModelDatatype.feature_name,
                        "feature_position",
                        TrainModelDatatype.feature_position,
                        "is_categorical",
                        DataType.is_categorical,
                        "datatype",
                        DataType.type,
                    )
                ).alias("feature_schema"),
                Algorithm.name.alias("algorithm_name"),
            )
            .join(Algorithm, on=TrainedModel.algorithm_id == Algorithm.id)
            .switch(TrainedModel)
            .join(TrainModelDatatype)
            .join(DataType)
            .where(TrainedModel.id == model_id)
            .group_by(TrainedModel.id, Algorithm.name)
        )
        .dicts()
        .get()
    )

    if include_training_info:
        query = (
            TrainingInfo.select(TrainingInfo)
            .join(ModelVersion)
            .where(ModelVersion.trained_model_id == model_id)
        )
        training_infos = [PydanticTrainingInfo(**row) for row in query.dicts()]
        versions_and_train_info = [
            ModelVersionAndTrainInfo(version=elem[0], training_info=elem[1])
            for elem in zip(versions, training_infos)
        ]
        return PydanticTrainedModelAndVersions(
            **train_and_features, versions=versions_and_train_info
        )
    else:
        return PydanticTrainedModelAndVersions(**train_and_features, versions=versions)


def get_models_and_version_ids(
    index_by_id: bool = False,
) -> list[TrainedModelAndVersionIds]:
    query = (
        TrainedModel.select(
            TrainedModel,
            Algorithm.name.alias("algorithm_name"),
            fn.STRING_AGG(ModelVersion.id.cast("TEXT"), ", ").alias("version_ids"),
        )
        .join(ModelVersion, JOIN.LEFT_OUTER)
        .join(Algorithm, JOIN.LEFT_OUTER, on=TrainedModel.algorithm_id == Algorithm.id)
        .group_by(TrainedModel.id, Algorithm.name.alias("algorithm_name"))
    )
    if not index_by_id:
        payload = [TrainedModelAndVersionIds(**row) for row in query.dicts()]
    else:
        payload = {row["id"]: TrainedModelAndVersionIds(**row) for row in query.dicts()}
    return payload
