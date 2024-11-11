import uuid
from app.Inventory_in.master_product.model import CounterDB
from sqlalchemy.orm import Session

def generate_epc_code():

    return f"EPC_{str(uuid.uuid4())[:6]}"


class EPCCodeGenerator:
    def __init__(self,counter_name, db : Session):
        self.db = db
        self.counter_name = counter_name

        counter = self.db.query(CounterDB).filter_by(code_name = self.counter_name).first()

        if not counter:
            counter = CounterDB(
                code_id = uuid.uuid4(),
                code_name = self.counter_name,
                value = 0

            )

            self.db.add(counter)
            self.db.commit()

    

    def generate_code(self, tag, zfill):
       
       self.tag = tag
       self.zfill = zfill
        
       counter = self.db.query(CounterDB).filter_by(code_name=self.counter_name).first()

       if counter:
           counter.value += 1

           self.db.commit()

           return f"{self.tag}{str(counter.value).zfill(self.zfill)}"
    

