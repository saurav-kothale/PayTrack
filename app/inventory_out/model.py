from sqlalchemy import JSON, Boolean, Column, DateTime, Integer, String
from database.database import Base


class ProductOutDb(Base):
    __tablename__ = "product_usage"
    product_out_id =  Column(String , primary_key=True)
    HSN_code  = Column(String)
    product_name = (Column(String))
    category = Column(String)
    bike_category = Column(String)
    size = Column(String)
    quntity = Column(Integer)
    name = Column(String)
    color = Column(String)
    city = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    is_deleted = Column(Boolean, default=False)
    user = Column(JSON)


# class TransferDb(Base):
#     __tablename__ = "product_trasfer"
#     transfer_id =  Column(String , primary_key=True)
#     from_city = Column(String)
#     to_city = Column(String)
#     quantity = Column(Integer)
#     created_at = Column(DateTime)
#     updated_at = Column(DateTime)
#     is_deleted = Column(Boolean, default=False)
#     user = Column(JSON)