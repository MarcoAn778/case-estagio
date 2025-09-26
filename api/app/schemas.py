from pydantic import BaseModel
from datetime import date

class MetricOut(BaseModel):
    account_id: int
    campaign_id: int
    cost_micros: float
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
