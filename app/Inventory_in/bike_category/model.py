


from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from database.database import Base
from sqlalchemy.orm import relationship
import uuid

class BikeDb(Base):
    __tablename__ = "bikes"
    bike_id = Column(String, primary_key=True)
    bike_name = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    is_deleted = Column(Boolean)
