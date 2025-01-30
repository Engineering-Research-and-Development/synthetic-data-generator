import peewee
from fastapi import APIRouter, Path
from starlette.responses import JSONResponse

from database.schema import Rule, FunctionParameter
from database.validation.schema import RuleOut as PydanticRule

router = APIRouter(prefix="/rules")


@router.get("/",
            name="Get all rules",
            summary="Get all the available rules",
            )
async def get_all_rules() -> list[PydanticRule]:
    results = [PydanticRule(**rule) for rule in Rule.select(Rule,
                                            FunctionParameter.name.alias('parameter_name'),
                                            )
                                            .join(FunctionParameter)
                                            .dicts()]

    return results


@router.get("/{rule_id}",
            name="Get a single rule",
            summary="Select a single rule",
            response_model= PydanticRule,
            responses={404: {"model": str}}
            )
async def get_single_rule(rule_id: int = Path(description="The id of the rule you want to get", example=1)):
    try:
        result = (Rule.select(Rule, FunctionParameter.name.alias('parameter_name'))
                  .join(FunctionParameter)
                  .where(Rule.id == rule_id)
                  .dicts()
                  .get()
                  )
    except peewee.DoesNotExist:
        return JSONResponse(status_code=404, content={"message": "Item not found"})

    return PydanticRule(**result)
