from sqlalchemy import Column, Integer, String, Float
from ..database import Base

class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    renewal_period = Column(Integer)
    tier = Column(Integer)
    discount = Column(Float)