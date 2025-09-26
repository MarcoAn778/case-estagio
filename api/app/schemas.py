from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

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