from pydantic import BaseModel
from datetime import date
from typing import Optional
from fastapi import Query

class MetricOut(BaseModel):
    account_id: int
    campaign_id: int
    cost_micros: Optional[float] = None
    clicks: float
    conversions: float
    impressions: float
    interactions: float
    date: date

    model_config = {"from_attributes": True}


class MetricsFilter(BaseModel):
    skip: int = Query(0, ge=0, description="Número de registros a pular")
    limit: int = Query(100, gt=0, le=500, description="Número máximo de registros a retornar")
    start_date: Optional[date] = Query(None, description="Data inicial do filtro")
    end_date: Optional[date] = Query(None, description="Data final do filtro")
    order_by: str = Query("date", description="Coluna para ordenação")
    desc: bool = Query(True, description="Ordenação decrescente se True")

class UserOut(BaseModel):
    username: str
    email: str
    role: str

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None