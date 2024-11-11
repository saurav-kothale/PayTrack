from pydantic import BaseModel

class TransferSchema(BaseModel):
    EPC_code : str
    from_city : str
    to_city : str
    quantity : int
