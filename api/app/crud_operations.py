from sqlalchemy.orm import Session
from . import models, auth
import logging
from typing import Optional

logger = logging.getLogger("uvicorn")


def get_metrics(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Metric)
        .order_by(models.Metric.date.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def count_metrics(db: Session) -> int:
    return db.query(models.Metric).count()


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()


def authenticate_user(db: Session, email: str, password: str) -> Optional[models.User]:
    user = get_user_by_email(db, email)
    if not user:
        logger.warning(f"Tentativa de login falhou: email={email} (não encontrado)")
        return None
    if not auth.verify_password(password, user.password):
        logger.warning(f"Tentativa de login falhou: email={email} (senha incorreta)")
        return None
    logger.info(f"Login bem-sucedido para email={email}")
    return user
