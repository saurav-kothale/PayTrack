from database.database import Base
from sqlalchemy import JSON, TEXT, Column, ForeignKey, Integer, String, DateTime, Boolean, true
from datetime import datetime
from sqlalchemy.orm import relationship, Relationship
# from app.Inventory_in.transfer_product.model import TransferProductDB

class ProductCategoryDB(Base):
    __tablename__ = "products"
    product_id = Column(String, primary_key= True)
    EPC_code = Column(String, unique=True)
    product_name = Column(String)
    HSN_code = Column(String)
    category = Column(String)
    bike_category = Column(JSON)
    size = Column(String)
    color = Column(String)
    unit = Column(String)
    gst = Column(Integer)
    created_at = Column(DateTime, default= datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    updated_at = Column(DateTime, default = datetime.now().strftime('%Y-%m-%d %H:%M:%S'), onupdate = datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    is_deleted = Column(Boolean, default=False)
    user = Column(JSON)


class MasterProductDB(Base):
    __tablename__ = "master products"
    # product_id = Column(String, primary_key= True)
    EPC_code = Column(String, unique=True, primary_key=True)
    product_name = Column(String)
    HSN_code = Column(String)
    category = Column(String, ForeignKey("new_category.category_id"))
    bike_category = Column(JSON)
    size = Column(String, ForeignKey("size.size_id"))
    color = Column(String, ForeignKey("colors.color_id"))
    unit = Column(String, ForeignKey("unit.unit_id"))
    gst = Column(String, ForeignKey("GST.gst_id"))
    created_at = Column(DateTime, default= datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    updated_at = Column(DateTime, default = datetime.now().strftime('%Y-%m-%d %H:%M:%S'), onupdate = datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    is_deleted = Column(Boolean, default=False)
    user = Column(JSON)

    category_relation = relationship("NewCategoryDb", back_populates="master_products")
    size_relation = relationship("Size", back_populates="master_products")
    color_relation = relationship("ColorDb", back_populates="master_products")
    size_relation = relationship("SizeDb", back_populates="master_products")
    gst_relation = relationship("GST", back_populates="master_products")
    unit_relation = relationship("Unit", back_populates="master_products")
    # bike_relationship = relationship("BikeDb", secondary="bike_product_association", back_populates="master_products")
    invoice_products = relationship("InvoiceProductsDB", back_populates="master_products")
    # instock_relation = relationship("InStockProducts", back_populates="master_relation")
    stock_relation = relationship("InStockProducts", back_populates="master_product_relation", foreign_keys="[InStockProducts.EPC_code]")
    transfer_products = relationship("TransferProductDB", back_populates="master_products")
    used_products_relation = relationship("UsedProduct", back_populates="master_products")


class CounterDB(Base):
    __tablename__ = "counter"
    code_id = Column(String, primary_key=True)
    code_name = Column(String)
    value = Column(Integer)
    