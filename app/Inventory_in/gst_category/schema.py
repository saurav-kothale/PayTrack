from  datetime import datetime
from pydantic import BaseModel


class GSTSchema(BaseModel):
    gst_perentage : int


class GSTUpdateSchema(BaseModel):
    gst_percentage : int