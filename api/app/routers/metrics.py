from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import database, models, schemas, dependencies

router = APIRouter(prefix="/metrics", tags=["Metrics"])


@router.get("/", tags=["Metrics"])
def read_metrics(
    filters: schemas.MetricsFilter = Depends(),
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
        metric_dict = metric.model_dump(exclude={"cost_micros"} if current_user.role != "admin" else None)
        result.append(metric_dict)

    return result
