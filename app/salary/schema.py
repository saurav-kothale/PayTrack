from pydantic import BaseModel

class SalaryClient(BaseModel):
    client_name : str
    grid_slab : bool
    rejection : bool
    bad_order : bool
    perform_to : str


class SalaryClientUpdate(BaseModel):
    client_name : str
    grid_slab : bool
    rejection : bool
    bad_order : bool
    perform_to : str
    