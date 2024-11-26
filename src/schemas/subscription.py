from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class SubscriptionBase(BaseModel):
    magazine_id: int
    plan_id: int

class SubscriptionCreate(SubscriptionBase):
    pass

class SubscriptionUpdate(BaseModel):
    plan_id: int

class SubscriptionResponse(SubscriptionBase):
    id: int
    user_id: int
    price: float
    renewal_date: datetime
    is_active: bool
    
    class Config:
        from_attributes = True
