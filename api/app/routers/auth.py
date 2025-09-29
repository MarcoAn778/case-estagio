from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
import logging

from .. import crud_operations, database, schemas, security, config

router = APIRouter(tags=["Auth"])
logger = logging.getLogger("uvicorn")


@router.post("/login", response_model=schemas.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db)
):
    user = crud_operations.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        logger.warning(f"Falha de login para email: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "AUTH_FAILED", "message": "Email ou senha incorretos"},
        )

    access_token_expires = timedelta(minutes=config.settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email, "role": user.role},
        expires_delta=access_token_expires
    )
    logger.info(f"Login bem-sucedido para email: {user.email} (username={user.username})")
    return {"access_token": access_token, "token_type": "bearer"}
