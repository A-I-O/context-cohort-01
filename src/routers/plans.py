from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..schemas import plan as plan_schemas
from ..models import plan as plan_models

router = APIRouter()

@router.get("/", response_model=List[plan_schemas.PlanResponse])
def get_plans(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    plans = db.query(plan_models.Plan).offset(skip).limit(limit).all()
    return plans

