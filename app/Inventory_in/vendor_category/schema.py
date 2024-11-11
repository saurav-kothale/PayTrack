from pydantic import BaseModel
from datetime import datetime

class VendorCategory(BaseModel):
    vendor_name : str
    contact_number : str
    address : str
    email_id : str
    city : str
    payment_terms : str
    gst_number : str

class VendorCategoryUpdate(BaseModel):
    vendor_name : str
    contact_number : str
    address : str
    email_id : str
    city : str
    payment_terms : str
    gst_number : str

