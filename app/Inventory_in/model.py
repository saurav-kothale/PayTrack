import DateTime
import uuid
from datetime import datetime, timezone
from database.database import Base
from sqlalchemy import JSON, Boolean, Column, Integer, Date, String,DateTime, Uuid, Float
from sqlalchemy.orm import Relationship, relationship

class InventoryDB(Base):
    __tablename__ = "inventory"
    invoice_id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    invoice_number = Column(String)
    invoice_amount = Column(Float)
    invoice_date = Column(Date)
    inventory_paydate = Column(Date)
    vendor = Column(String)
    invoice_image_id = Column(String)
    user = Column(JSON)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    is_deleted = Column(Boolean, default=False)
    products = Relationship("ProductDB", back_populates="invoice")


class InvoiceDetailsDB(Base):
    __tablename__ = "invoice details"
    invoice_id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    invoice_number = Column(String)
    invoice_amount = Column(Float)
    invoice_date = Column(Date)
    inventory_paydate = Column(Date)
    vendor = Column(String)
    invoice_image_id = Column(String)
    user = Column(JSON)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    is_deleted = Column(Boolean, default=False)
    products = relationship("InvoiceProductsDB", back_populates="invoice_relation")