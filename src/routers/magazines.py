from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..schemas import magazine as magazine_schemas
from ..models import magazine as magazine_models
from ..models import user as user_models
from ..auth.utils import get_current_user

router = APIRouter()

@router.get("/", response_model=List[magazine_schemas.MagazineResponse])
def get_magazines(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    magazines = db.query(magazine_models.Magazine).offset(skip).limit(limit).all()
    return magazines

# @router.post("/", response_model=magazine_schemas.MagazineResponse)
# def create_magazine(
#     magazine: magazine_schemas.MagazineCreate,
#     db: Session = Depends(get_db),
#     current_user: user_models.User = Depends(get_current_user)
# ):
#     db_magazine = magazine_models.Magazine(**magazine.dict())
#     db.add(db_magazine)
#     db.commit()
#     db.refresh(db_magazine)
#     return db_magazine
# src/routers/magazines.py

@router.post("/", response_model=magazine_schemas.MagazineResponse)
def create_magazine(
    magazine: magazine_schemas.MagazineCreate,
    db: Session = Depends(get_db),
    current_user: user_models.User = Depends(get_current_user)
):
    db_magazine = magazine_models.Magazine(
        name=magazine.name, description=magazine.description, base_price=magazine.base_price
    )
    db.add(db_magazine)
    db.commit()
    db.refresh(db_magazine)
    return db_magazine

# @router.post("/", response_model=magazine_schemas.MagazineResponse)
# def create_magazine(
#     magazine: magazine_schemas.MagazineCreate,
#     db: Session = Depends(get_db),
#     current_user: user_models.User = Depends(get_current_user)
# ):
#     # Explicitly create the magazine with all provided data
#     db_magazine = magazine_models.Magazine(
#         name=magazine.name, 
#         description=magazine.description, 
#         base_price=magazine.base_price
#     )
#     db.add(db_magazine)
#     db.commit()
#     db.refresh(db_magazine)
#     return db_magazine