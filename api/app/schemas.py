from pydantic import BaseModel
from datetime import date
from typing import Optional

class MetricOut(BaseModel):
    account_id: int
    campaign_id: int
    cost_micros: Optional[float]
    clicks: float
    conversions: float
    impressions: float
    interactions: float
    date: date

    class Config:
        orm_mode = True

class UserOut(BaseModel):
    username: str
    role: str
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class UserLogin(BaseModel):
    username: str
    password: str
