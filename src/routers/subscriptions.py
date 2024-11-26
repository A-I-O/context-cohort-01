from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from ..database import get_db
from ..schemas import subscription as subscription_schemas
from ..models import subscription as subscription_models
from ..models import magazine as magazine_models
from ..models import plan as plan_models
from ..models import user as user_models
from ..auth.utils import get_current_user

router = APIRouter()

@router.get("/", response_model=List[subscription_schemas.SubscriptionResponse])
def get_user_subscriptions(
    db: Session = Depends(get_db),
    current_user: user_models.User = Depends(get_current_user)
):
    subscriptions = db.query(subscription_models.Subscription).filter(
        subscription_models.Subscription.user_id == current_user.id,
        subscription_models.Subscription.is_active == True
    ).all()
    return subscriptions

@router.post("/", response_model=subscription_schemas.SubscriptionResponse)
def create_subscription(
    subscription: subscription_schemas.SubscriptionCreate,
    db: Session = Depends(get_db),
    current_user: user_models.User = Depends(get_current_user)
):
    # Check for existing active subscription
    existing_subscription = db.query(subscription_models.Subscription).filter(
        subscription_models.Subscription.user_id == current_user.id,
        subscription_models.Subscription.magazine_id == subscription.magazine_id,
        subscription_models.Subscription.is_active == True
    ).first()
    
    if existing_subscription:
        raise HTTPException(status_code=400, detail="Active subscription already exists for this magazine")
    
    # Get magazine and plan details
    magazine = db.query(magazine_models.Magazine).filter(magazine_models.Magazine.id == subscription.magazine_id).first()
    if not magazine:
        raise HTTPException(status_code=404, detail="Magazine not found")
    
    plan = db.query(plan_models.Plan).filter(plan_models.Plan.id == subscription.plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    
    # Calculate price and renewal date
    price = magazine.base_price * (1 - plan.discount)
    renewal_date = datetime.utcnow() + timedelta(days=30 * plan.renewal_period)
    
    # Create new subscription
    db_subscription = subscription_models.Subscription(
        user_id=current_user.id,
        magazine_id=subscription.magazine_id,
        plan_id=subscription.plan_id,
        price=price,
        renewal_date=renewal_date,
        is_active=True
    )
    
    db.add(db_subscription)
    db.commit()
    db.refresh(db_subscription)
    return db_subscription

@router.put("/{subscription_id}", response_model=subscription_schemas.SubscriptionResponse)
def update_subscription(
    subscription_id: int,
    subscription_update: subscription_schemas.SubscriptionUpdate,
    db: Session = Depends(get_db),
    current_user: user_models.User = Depends(get_current_user)
):
    # Get existing subscription
    db_subscription = db.query(subscription_models.Subscription).filter(
        subscription_models.Subscription.id == subscription_id,
        subscription_models.Subscription.user_id == current_user.id,
        subscription_models.Subscription.is_active == True
    ).first()
    
    if not db_subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    # Deactivate current subscription
    db_subscription.is_active = False
    
    # Create new subscription with updated plan
    magazine = db.query(magazine_models.Magazine).filter(
        magazine_models.Magazine.id == db_subscription.magazine_id
    ).first()
    
    new_plan = db.query(plan_models.Plan).filter(
        plan_models.Plan.id == subscription_update.plan_id
    ).first()
    
    if not new_plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    
    # Calculate new price and renewal date
    new_price = magazine.base_price * (1 - new_plan.discount)
    new_renewal_date = datetime.utcnow() + timedelta(days=30 * new_plan.renewal_period)
    
    # Create new subscription
    new_subscription = subscription_models.Subscription(
        user_id=current_user.id,
        magazine_id=db_subscription.magazine_id,
        plan_id=subscription_update.plan_id,
        price=new_price,
        renewal_date=new_renewal_date,
        is_active=True
    )
    
    db.add(new_subscription)
    db.commit()
    db.refresh(new_subscription)
    return new_subscription

@router.delete("/{subscription_id}")
def cancel_subscription(
    subscription_id: int,
    db: Session = Depends(get_db),
    current_user: user_models.User = Depends(get_current_user)
):
    subscription = db.query(subscription_models.Subscription).filter(
        subscription_models.Subscription.id == subscription_id,
        subscription_models.Subscription.user_id == current_user.id,
        subscription_models.Subscription.is_active == True
    ).first()
    
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    subscription.is_active = False
    db.commit()
    return {"message": "Subscription cancelled successfully"}