from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging
from . import models, database
from .config.cors import setup_cors
from .routers import auth, metrics, users

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    models.Base.metadata.create_all(bind=database.engine)
    yield
    database.engine.dispose()

app = FastAPI(title="Case API", lifespan=lifespan)

setup_cors(app)
app.include_router(auth.router)
app.include_router(metrics.router)
app.include_router(users.router)

@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}
