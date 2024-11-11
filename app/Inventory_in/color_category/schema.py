from datetime import datetime
from pydantic import BaseModel

class ColorCategorySchema(BaseModel):
    color_name : str

class ColorUpdateSchema(BaseModel):
    color_name : str
