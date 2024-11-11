from sqlalchemy import Boolean, Column, DateTime, String
from database.database import Base
from sqlalchemy.orm import relationship
import uuid

class CityDb(Base):
    __tablename__ = "cities"
    city_id = Column(String, primary_key=True)
    city_name = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    is_deleted = Column(Boolean)

    invoice_products = relationship("InvoiceProductsDB", back_populates="city_relation")

    instock_products = relationship("InStockProducts", back_populates="city_relation")

    # transfer_products = relationship("TransferProductDB", back_populates="city_relation")

    transfer_products_from = relationship("TransferProductDB", foreign_keys="[TransferProductDB.from_city]", back_populates="from_city_relation")
    transfer_products_to = relationship("TransferProductDB", foreign_keys="[TransferProductDB.to_city]", back_populates="to_city_relation")

    used_product_relation = relationship("UsedProduct", back_populates="city_relation")