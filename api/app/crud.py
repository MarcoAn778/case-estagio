from sqlalchemy.orm import Session
from . import models

def get_metrics(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Metric).order_by(models.Metric.date.desc()).offset(skip).limit(limit).all()

def count_metrics(db: Session):
    return db.query(models.Metric).count()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()
