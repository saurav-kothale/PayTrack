from abc import update_abstractmethods
import json
from ssl import create_default_context
from pydantic import BaseModel, Field, validator
from datetime import date, datetime
from typing import Dict


class Invetory(BaseModel):
    invoice_number : str 
    invoice_amount : float 
    invoice_date : date  
    inventory_paydate : date
    vendor : str
    invoice_image_id : str


class InvetoryUpdate(BaseModel):
    invoice_number : str
    invoice_amount : float
    invoice_date : date 
    inventory_paydate : date
    vendor : str
    invoice_image_id : str

    class config:
        from_attributes = True

class InvetoryResponse(BaseModel):
    invoice_id : str
    invoice_number : str
    invoice_amount : int
    invoice_date : date
    inventory_paydate : date
    vendor : str
    invoice_image_id : str

    class config:
        from_attributes = True

class InventoryResponseV2(BaseModel):
    invoice_id: str
    invoice_number: str
    invoice_amount: float
    invoice_date: date
    inventory_paydate: date
    vendor: str
    invoice_image_id: str
    product_count: int
    user : Dict
    created_at : datetime
    updated_at : datetime