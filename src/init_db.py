# src/init_db.py
from sqlalchemy.orm import Session
from database import SessionLocal
from models.plan import Plan

def init_plans(db: Session):
    plans = [
        {
            "title": "Silver Plan",
            "description": "Basic plan which renews monthly",
            "renewal_period": 1,
            "tier": 1,
            "discount": 0.0
        },
        {
            "title": "Gold Plan",
            "description": "Standard plan which renews every 3 months",
            "renewal_period": 3,
            "tier": 2,
            "discount": 0.05
        },
        {
            "title": "Platinum Plan",
            "description": "Premium plan which renews every 6 months",
            "renewal_period": 6,
            "tier": 3,
            "discount": 0.10
        },
        {
            "title": "Diamond Plan",
            "description": "Exclusive plan which renews annually",
            "renewal_period": 12,
            "tier": 4,
            "discount": 0.25
        }
    ]

    for plan_data in plans:
        plan = db.query(Plan).filter(Plan.title == plan_data["title"]).first()
        if not plan:
            plan = Plan(**plan_data)
            db.add(plan)
    
    db.commit()

if __name__ == "__main__":
    db = SessionLocal()
    init_plans(db)
    db.close()