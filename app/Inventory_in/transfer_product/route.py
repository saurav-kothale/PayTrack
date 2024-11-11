from hmac import new
from fastapi import APIRouter, Depends, HTTPException, status
from app.Inventory_in.transfer_product.model import TransferProductDB
from app.Inventory_in.transfer_product.schema import TransferSchema
from app.product.model.model import InStockProducts
from app.product.route.route import available_quantity
from database.database import get_db
from sqlalchemy.orm import Session
import uuid
from datetime import datetime
from app.Inventory_in.bike_category.model import BikeDb


transfer_router = APIRouter()

@transfer_router.post("/v1/v2/product/transfer")
def product_transfer(
    schema : TransferSchema,
    db : Session = Depends(get_db)
):
    
    db_product = db.query(InStockProducts).filter(InStockProducts.EPC_code == schema.EPC_code, InStockProducts.city == schema.from_city).first()

    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "product not found to trasfer"
        )
    
    if db_product.available_quantity < schema.quantity:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="please select valid quantity"
        )
    
    if db_product.city == schema.to_city:
        raise HTTPException(
           status_code=status.HTTP_400_BAD_REQUEST,
            detail="Transfer in same city is not allowed" 
        )
    
    db_product.available_quantity -= schema.quantity


    new_transfer_product = TransferProductDB(
        transfer_id = str(uuid.uuid4()),
        EPC_code = schema.EPC_code,
        from_city = schema.from_city,
        to_city = schema.to_city,
        quantity = schema.quantity,
        transfer_at = datetime.now(),
        transfer_by = "not_implemented"
    )

    available_product = db.query(InStockProducts).filter(InStockProducts.EPC_code == schema.EPC_code, InStockProducts.city == schema.to_city).first()

    if not available_product:

        new_product = InStockProducts(
            id = str(uuid.uuid4()),
            EPC_code = schema.EPC_code,
            city = schema.to_city,
            available_quantity = schema.quantity
        )

        db.add(new_product)

    else :

        available_product.available_quantity += schema.quantity


    db.add(new_transfer_product)

    db.commit()

    bikes = db.query(BikeDb).filter(BikeDb.bike_id.in_(db_product.master_product_relation.bike_category)).all()

    return{
        "status" : status.HTTP_200_OK,
        "message" : "Product Export Successfully",
        "final_product" : {
            "product_name" : db_product.master_product_relation.product_name,
            "hsn_code" : db_product.master_product_relation.HSN_code,
            "category": db_product.master_product_relation.category_relation.category_name,
            "bike_category" : [bike.bike_name for bike in bikes],
            "color": db_product.master_product_relation.color_relation.color_name,
            "size": db_product.master_product_relation.size_relation.size_name,
            "from city": new_transfer_product.from_city_relation.city_name,
            "to city" : new_transfer_product.to_city_relation.city_name,
            "EPC_code" : db_product.EPC_code,
            "quantity" : db_product.available_quantity,
            
        } 
    }



    








    
