from sqlalchemy import Column, Integer, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    magazine_id = Column(Integer, ForeignKey("magazines.id"))
    plan_id = Column(Integer, ForeignKey("plans.id"))
    price = Column(Float)
    renewal_date = Column(DateTime)
    is_active = Column(Boolean, default=True)

    user = relationship("User", back_populates="subscriptions")
    magazine = relationship("Magazine")
    plan = relationship("Plan")