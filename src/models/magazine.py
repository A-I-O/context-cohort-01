from sqlalchemy import Column, Integer, String, Float
from ..database import Base

class Magazine(Base):
    __tablename__ = "magazines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    base_price = Column(Float)