from sqlalchemy.orm import Session
from . import models, auth

def get_metrics(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Metric).order_by(models.Metric.date.desc()).offset(skip).limit(limit).all()

def count_metrics(db: Session):
    return db.query(models.Metric).count()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not auth.verify_password(password, user.password):
        return None
    return user
