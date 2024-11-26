from pydantic import BaseModel, Field
from typing import Optional

class MagazineBase(BaseModel):
    name: str
    description: str
    base_price: float = Field(gt=0)

class MagazineCreate(MagazineBase):
    pass

class MagazineResponse(MagazineBase):
    id: int
    
    class Config:
        from_attributes = True

