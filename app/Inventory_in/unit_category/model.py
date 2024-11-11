from database.database import Base
from sqlalchemy import Column, DateTime, String, Boolean
from sqlalchemy.orm import relationship

class Unit(Base):
    __tablename__ = "unit"
    unit_id = Column(String, primary_key=True)
    unit_name = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    is_deleted = Column(Boolean)

    master_products = relationship("MasterProductDB", back_populates="unit_relation")