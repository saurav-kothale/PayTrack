from database.database import Base
from sqlalchemy import INTEGER, Column, DateTime, Float, Integer, String, Boolean
from sqlalchemy.orm import relationship

class GST(Base):
    __tablename__ = "GST"
    gst_id = Column(String, primary_key=True)
    gst_percentage = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    is_deleted = Column(Boolean)

    master_products = relationship("MasterProductDB", back_populates="gst_relation")