from fastapi import APIRouter, Depends
import logging

from .. import schemas, models, dependencies

router = APIRouter(prefix="/users", tags=["Users"])
logger = logging.getLogger("uvicorn")


@router.get("/me", response_model=schemas.UserOut)
def read_users_me(current_user: models.User = Depends(dependencies.get_current_user)):
    logger.info(f"Consulta em /users/me para {current_user.username}")
    return current_user
