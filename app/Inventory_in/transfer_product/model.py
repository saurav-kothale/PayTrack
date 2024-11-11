from database.database import Base
from sqlalchemy import Column, ForeignKey, String, Integer, DateTime
from sqlalchemy.orm import relationship
# from app.Inventory_in.master_product.model import MasterProductDB


class TransferProductDB(Base):
    __tablename__ = "product_transfer"
    transfer_id = Column(String, primary_key=True)
    EPC_code = Column(String, ForeignKey("master products.EPC_code"))
    from_city = Column(String, ForeignKey("cities.city_id"))
    to_city = Column(String, ForeignKey("cities.city_id"))
    quantity = Column(Integer)
    transfer_at = Column(DateTime)
    transfer_by = Column(String)

    master_products = relationship("MasterProductDB", back_populates= "transfer_products")
    # city_relation = relationship("CityDb", back_populates= "transfer_products")

    from_city_relation = relationship("CityDb", foreign_keys=[from_city], back_populates="transfer_products_from")
    to_city_relation = relationship("CityDb", foreign_keys=[to_city], back_populates="transfer_products_to")
