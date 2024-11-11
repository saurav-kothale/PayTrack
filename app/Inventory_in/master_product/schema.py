from pydantic import BaseModel

class ProductCategorySchema(BaseModel):
    product_name : str
    hsn_code : str
    category : str
    bike_category : list[str]
    size : str
    color : str
    unit : str
    gst : str

class ProductCategorySchemaV2(BaseModel):
    product_name : str
    hsn_code : str
    category : str
    bike_category : list[str]
    size : str
    color : str
    unit : str
    gst : str
