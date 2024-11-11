from datetime import datetime
from pydantic import BaseModel

class CategorySchema(BaseModel):
    category_name : str

class CategoryUpdateSchema(BaseModel):
    category_name : str
