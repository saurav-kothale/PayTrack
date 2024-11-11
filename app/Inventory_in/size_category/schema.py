from datetime import datetime
from pydantic import BaseModel

class SizeCategorySchema(BaseModel):
    size_name : str

class SizeUpdateSchema(BaseModel):
    size_name : str
