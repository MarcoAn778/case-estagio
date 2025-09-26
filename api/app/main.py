from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List

from . import db, crud, schemas, models, auth, deps, config

app = FastAPI(title="Case - API (Dia 3)")

@asynccontextmanager
async def lifespan(app: FastAPI):
    models.Base.metadata.create_all(bind=db.engine)
    yield
    db.engine.dispose()

app = FastAPI(
    title="Case - API (Dia 2)",
    lifespan=lifespan
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(db.get_db)):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Usuário ou senha incorretos")

    access_token_expires = timedelta(minutes=config.settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username, "role": user.role}, 
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/metrics", response_model=List[schemas.MetricOut])
def read_metrics(skip: int = 0, limit: int = 100, db: Session = Depends(db.get_db), current_user=Depends(deps.get_current_user)):
    items = crud.get_metrics(db, skip=skip, limit=limit)
    if current_user.role != "admin":
        for item in items:
            item.cost_micros = None
    return items
