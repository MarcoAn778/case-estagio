from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from contextlib import asynccontextmanager
from api.app import schemas
from . import db, crud, models

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

@app.get("/metrics", response_model=List[schemas.MetricOut])
def read_metrics(
    skip: int = 0,
    limit: int = Query(100, le=1000),
    db: Session = Depends(db.get_db),
):
    items = crud.get_metrics(db, skip=skip, limit=limit)
    return items

@app.get("/metrics/count")
def metrics_count(db: Session = Depends(db.get_db)):
    return {"count": crud.count_metrics(db)}
