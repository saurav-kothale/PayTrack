from numpy import size
from pydantic import BaseModel
from enum import Enum

class ProductSchema(BaseModel):
    EPC_code : str
    product_name: str
    category : str
    bike_category : list[str]
    quantity : int
    size : str
    color : str
    city : str  
    HSN_code : str
    GST : int
    unit : str
    amount : float

class ProductUpdateSchema(BaseModel):
    EPC_code : str
    quantity : int
    city : str  
    amount : float

class ProductUseSchema(BaseModel):
    EPC_code : str
    city : str
    quantity : int
    comment : str
    bike_number : str

class ProductCountResponse(BaseModel):
    total_in_products: int

    




