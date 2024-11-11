from pydantic import Json
from sqlalchemy import ARRAY, Boolean, Column, Float, ForeignKey, Integer, String, DateTime, JSON, UniqueConstraint
from sqlalchemy.orm import Relationship
from app.Inventory_in.master_product.model import MasterProductDB
from app.Inventory_in.model import InvoiceDetailsDB
from database.database import Base
import uuid
from sqlalchemy.orm import relationship

class ProductDB(Base):
    __tablename__ = "product"
    product_id = Column(String, primary_key=True, default=(uuid.uuid4()))
    product_name = Column(String)
    category = Column(String)
    bike_category = Column(String)
    quantity = Column(Integer)
    size = Column(String)
    city = Column(String)
    color = Column(String)
    user = Column(JSON)
    HSN_code = Column(String)
    GST = Column(String)
    unit = Column(String)
    amount = Column(Float)
    total_amount = Column(Float)
    amount_with_gst = Column(Float)
    invoice_id = Column(String, ForeignKey("inventory.invoice_id"))
    invoice = Relationship("InventoryDB", back_populates="products")
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    is_deleted = Column(Boolean)


class InvoiceProductsDB(Base):
    __tablename__ = "invoice_products"
    id = Column(String, primary_key=True, default=(uuid.uuid4()))
    EPC_code = Column(String, ForeignKey("master products.EPC_code"))
    # category = Column(String)
    # bike_category = Column(String)
    quantity = Column(Integer)
    # size = Column(String)
    city = Column(String, ForeignKey("cities.city_id"))
    # color = Column(String)
    user = Column(JSON)
    # HSN_code = Column(String)
    # GST = Column(Integer)  
    # unit = Column(String)
    amount = Column(Float)
    total_amount = Column(Float)
    amount_with_gst = Column(Float)
    invoice_id = Column(String, ForeignKey("invoice details.invoice_id"))
    # invoice = Relationship("InvoiceDetailsDB", back_populates="master products")
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    is_deleted = Column(Boolean)
    # __table_args__ = (UniqueConstraint('EPC_code', 'invoice_id', name='_epc_invoice_uc'),)
    invoice_relation = relationship("InvoiceDetailsDB", back_populates="products")

    # Relationship with MasterProductDB
    master_products = relationship("MasterProductDB", back_populates="invoice_products")

    city_relation = relationship("CityDb", back_populates="invoice_products")

    # invoice_instock_relation = relationship("InStockProducts", back_populates="invoice_product_relation")
    
   

class AuditUpdateDB(Base):
    __tablename__ = "product update audit"
    id = Column(String, primary_key=True, default=(uuid.uuid4()))
    invoice_id = Column(String)
    EPC_code = Column(String)
    field_changed = Column(String)
    old_value = Column(String)
    new_value = Column(String)
    changed_at = Column(DateTime)
    changed_by = Column(String)

class AuditTransferDB(Base):
    __tablename__ = "product transfer audit"
    id = Column(String, primary_key=True, default=(uuid.uuid4()))
    invoice_id = Column(String)
    product_id = Column(String)
    product_name = Column(String)
    from_city = Column(String)
    to_city = Column(String)
    total_product = Column(Integer)
    transfer_quantity = Column(Integer)
    transfer_at = Column(DateTime)
    transfer_by = Column(String)


class InStockProducts(Base):
    __tablename__ = "product_stock"
    id = Column(String, primary_key=True)
    EPC_code = Column(String, ForeignKey("master products.EPC_code"))
    city = Column(String, ForeignKey("cities.city_id"))
    available_quantity = Column(Integer)

    # invoice_product_relation = relationship("InvoiceProductsDB", back_populates="invoice_instock_relation")

    # master_relation = relationship("MasterProductDB", back_populates="instock_relation")
    master_product_relation = relationship("MasterProductDB", back_populates="stock_relation")
    city_relation = relationship("CityDb", back_populates="instock_products")


class UsedProduct(Base):
    __tablename__ = "used products"
    id = Column(String, primary_key=True)
    EPC_code = Column(String, ForeignKey("master products.EPC_code"))
    city = Column(String, ForeignKey("cities.city_id"))
    quantity = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    comment = Column(String, nullable=True)
    bike_number = Column(String)
    user = Column(JSON)

    master_products = relationship("MasterProductDB", back_populates="used_products_relation")

    city_relation = relationship("CityDb", back_populates= "used_product_relation")





