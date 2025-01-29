from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import NoResultFound
from ..dependencies import SessionDep
from model_registry.database.handlers import mv_handler as db_handler

router = APIRouter(prefix="/versions")


@router.get("/", status_code=200)
async def get_all_model_versions(session: SessionDep):
    return db_handler.get_all(session)

@router.get("/{version_id}", status_code=200)
async def get_version_by_id(version_id: int , session: SessionDep):
    try:
        version = db_handler.get_by_id(version_id,session)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="No version with id: " + str(version_id) + " has been found")
    return version