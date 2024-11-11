from sqlalchemy import Boolean, Column, DateTime, String
from database.database import Base

class SalaryClientModel(Base):
    __tablename__ = "client_salary_structure"
    client_id = Column(String, primary_key = True)
    client_name = Column(String)
    grid_slab = Column(Boolean)
    rejection = Column(Boolean)
    bad_order = Column(Boolean)
    perform_to = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    is_deleted = Column(Boolean)