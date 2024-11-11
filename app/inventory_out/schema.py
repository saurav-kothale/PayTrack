from pydantic import BaseModel
from typing import List

class InventoryOut(BaseModel):
    product_name : str
    name : str
    category : str
    HSN_code : str
    bike_category : str
    color : str
    size : str
    city : str
    quantity : int

class InventoryBulkOut(BaseModel):
    products : list[InventoryOut]


class TransferSchema(BaseModel):
    product_name : str
    category : str
    bike_category : str
    quantity : int
    size : str
    color : str
    city : str
    HSN_code : str


class TransferSchemaV2(BaseModel):
    product_name : str
    category : str
    bike_category : str
    quantity : int
    size : str
    color : str
    city : str
    HSN_code : str


class ProductTopResponse(BaseModel):
    EPC_code: str
    product_name: str
    total_quantity: int

class ProductTopListResponse(BaseModel):
    top_products: List[ProductTopResponse]