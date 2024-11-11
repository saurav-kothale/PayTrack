from sqlalchemy import Boolean, Column, DateTime, String
from database.database import Base
import uuid
from sqlalchemy.orm import relationship

class SizeDb(Base):
    __tablename__ = "size"
    size_id = Column(String, primary_key=True)
    size_name = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    is_deleted = Column(Boolean)

    master_products = relationship("MasterProductDB", back_populates="size_relation")