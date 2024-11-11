from sqlalchemy import Boolean, Column, DateTime, String
from database.database import Base
from sqlalchemy.orm import relationship
import uuid

class NewCategoryDb(Base):
    __tablename__ = "new_category"
    category_id = Column(String, primary_key=True)
    category_name = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    is_deleted = Column(Boolean)

    master_products = relationship("MasterProductDB", back_populates="category_relation")