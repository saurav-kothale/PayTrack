from datetime import datetime
from pydantic import BaseModel

class CityCategorySchema(BaseModel):
    city_name : str

class CityUpdateSchema(BaseModel):
    city_name : str
