from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import NoResultFound
from sqlmodel import select
from model_registry.database.schema import ModelVersion
from ..dependencies import SessionDep

router = APIRouter(prefix="/versions")


@router.get("/", status_code=200)
async def get_all_model_versions(session: SessionDep):
    statement = select(ModelVersion)
    results = session.exec(statement)
    return results.all()

@router.get("/{version_id}", status_code=200)
async def get_version_by_id(version_id: int , session: SessionDep):
    try:
        statement = select(ModelVersion).where(ModelVersion.id == version_id)
        version = session.exec(statement).one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="No version with id: " + str(version_id) + " has been found")
    return version