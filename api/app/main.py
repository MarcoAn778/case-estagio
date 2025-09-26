from fastapi import FastAPI, Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
from datetime import date, timedelta
from typing import List, Optional
import logging

from . import crud_operations, database, dependencies, schemas, models, auth, config

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    models.Base.metadata.create_all(bind=database.engine)
    yield
    database.engine.dispose()


app = FastAPI(title="Case - API (Dia 3)", lifespan=lifespan)


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}


@app.post("/login", response_model=schemas.Token, tags=["Auth"])
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
    access_token = auth.create_access_token(
        data={"sub": user.email, "role": user.role},
        expires_delta=access_token_expires
    )
    logger.info(f"Login bem-sucedido para email: {user.email} (username={user.username})")
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/metrics", tags=["Metrics"])
def read_metrics(
    skip: int = 0,
    limit: int = 100,
    start_date: Optional[date] = Query(None, description="Data inicial"),
    end_date: Optional[date] = Query(None, description="Data final"),
    order_by: str = Query("date", description="Coluna para ordenar"),
    desc: bool = Query(True, description="Ordenar de forma decrescente?"),
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(dependencies.get_current_user)
):
    query = db.query(models.Metric)

    if start_date:
        query = query.filter(models.Metric.date >= start_date)
    if end_date:
        query = query.filter(models.Metric.date <= end_date)

    if hasattr(models.Metric, order_by):
        column = getattr(models.Metric, order_by)
        query = query.order_by(column.desc() if desc else column.asc())
    else:
        raise HTTPException(status_code=400, detail=f"Coluna inválida para ordenação: {order_by}")

    items = query.offset(skip).limit(limit).all()

    result: List[dict] = []
    for item in items:
        metric = schemas.MetricOut.model_validate(item)
        metric_dict = metric.model_dump()

        if current_user.role != "admin":
            metric_dict.pop("cost_micros", None)

        result.append(metric_dict)

    return result


@app.get("/users/me", response_model=schemas.UserOut, tags=["Users"])
def read_users_me(current_user: models.User = Depends(dependencies.get_current_user)):
    logger.info(f"Consulta em /users/me para {current_user.username}")
    return current_user
