from pydantic import BaseModel, Field
from typing import Optional

class PlanBase(BaseModel):
    title: str
    description: str
    renewal_period: int = Field(gt=0)
    tier: int
    discount: float = Field(ge=0, le=1)

class PlanCreate(PlanBase):
    pass

class PlanResponse(PlanBase):
    id: int
    
    class Config:
        from_attributes = True