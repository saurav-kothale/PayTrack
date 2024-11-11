from  datetime import datetime
from pydantic import BaseModel


class UnitSchema(BaseModel):
    unit_name : str

class UnitUpdateSchema(BaseModel):
    unit_name : str