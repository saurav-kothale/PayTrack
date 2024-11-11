from database.database import Base
from sqlalchemy import Boolean, Column, Integer, String, DateTime


class VendorCategoryModel(Base):
    __tablename__ = "vendor_category"
    Vendor_id = Column(String, unique=True, primary_key=True)
    Vendor_name = Column(String)
    Contact_number = Column(String)
    Address = Column(String)
    Email_id = Column(String)
    City = Column(String)
    Payment_term = Column(String)
    GST_Number = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    is_deleted = Column(Boolean)
    