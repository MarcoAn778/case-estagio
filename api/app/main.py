from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
from datetime import timedelta
from typing import List
from .schemas import MetricsFilter
import logging
from .config.cors import setup_cors
from . import crud_operations, database, dependencies, schemas, models, auth, config

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    models.Base.metadata.create_all(bind=database.engine)
    yield
    database.engine.dispose()


app = FastAPI(title="Case api", lifespan=lifespan)

setup_cors(app)


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
    filters: MetricsFilter = Depends(),
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(dependencies.get_current_user)
):
    if not hasattr(models.Metric, filters.order_by):
        raise HTTPException(
            status_code=422,
            detail=f"Coluna inválida para ordenação: {filters.order_by}"
        )

    query = db.query(models.Metric)

    if filters.start_date:
        query = query.filter(models.Metric.date >= filters.start_date)
    if filters.end_date:
        query = query.filter(models.Metric.date <= filters.end_date)

    column = getattr(models.Metric, filters.order_by)
    query = query.order_by(column.desc() if filters.desc else column.asc())

    items = query.offset(filters.skip).limit(filters.limit).all()

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
