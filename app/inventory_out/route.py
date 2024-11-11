from math import prod
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import Integer, desc, func, Date
from app.Inventory_in.bike_category.model import BikeDb
from app.Inventory_in.master_product.model import MasterProductDB
from app.inventory_out.schema import InventoryBulkOut, InventoryOut, ProductTopListResponse, ProductTopResponse, TransferSchema
from app.product.model.model import ProductDB, UsedProduct
from app.inventory_out.model import ProductOutDb
from app.utils.util import get_current_user
from database.database import get_db
from datetime import datetime, date
import uuid
from sqlalchemy.sql.expression import cast

inventory_out_router = APIRouter()

@inventory_out_router.post("/inventory/use")
def create_product(
    product : InventoryOut,
    db : Session = Depends(get_db),
    current_user : str = Depends(get_current_user)

):    
    # Create a new product
    new_product = ProductOutDb(
        product_out_id=str(uuid.uuid4()),
        product_name=product.product_name,
        HSN_code = product.HSN_code,
        category=product.category,
        bike_category=product.bike_category,
        quntity=product.quantity,
        name = product.name,
        size=product.size,
        city=product.city,
        color=product.color,
        created_at = datetime.now(),
        updated_at = datetime.now(),
        is_deleted = False,
        user = current_user
    )

    # Add the product to the database
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    used_quantity = db.query(func.sum(ProductOutDb.quntity)).filter(
        ProductOutDb.category == product.category,
        ProductOutDb.bike_category == product.bike_category,
        ProductOutDb.product_name == product.product_name,
        ProductOutDb.color == product.color,
        ProductOutDb.size == product.size,
        ProductOutDb.city == product.city
    ).scalar() or 0

    total_quantity = db.query(func.sum(ProductDB.quantity)).filter(
        ProductDB.category == product.category,
        ProductDB.bike_category == product.bike_category,
        ProductDB.product_name == product.product_name,
        ProductDB.color == product.color,
        ProductDB.size == product.size,
        ProductDB.city == product.city
    ).scalar() or 0

    remaining_quantity = total_quantity - used_quantity

    return {
        "category": product.category,
        "bike_category": product.bike_category,
        "product_name": product.product_name,
        "color" : product.color,
        "size" : product.size,
        "city" : product.city,
        "name" : product.name,
        "user" : current_user,
        "remaining_quantity": remaining_quantity
    }


@inventory_out_router.get("/get/inventory/used")
def get_used_inventory(db : Session = Depends(get_db)):

    db_products = db.query(ProductOutDb).order_by(desc(ProductOutDb.created_at)).all()

    if not db_products:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No product found"
        )
    
    return{
        "status" : status.HTTP_202_ACCEPTED,
        "message" : "Product fetched successfully",
        "products" : db_products
    }


@inventory_out_router.post("/inventory/bulk/use")
def create_products(
    schema : InventoryBulkOut,
    db : Session = Depends(get_db),
    current_user : str = Depends(get_current_user)

):  
    product_data = []

    for product in schema.products:
    # Create a new product
        new_product = ProductOutDb(
            product_out_id=str(uuid.uuid4()),
            product_name=product.product_name,
            HSN_code = product.HSN_code,
            category=product.category,
            bike_category=product.bike_category,
            quntity=product.quantity,
            name = product.name,
            size=product.size,
            city=product.city,
            color=product.color,
            created_at = datetime.now(),
            updated_at = datetime.now(),
            is_deleted = False,
            user = current_user
        )

        # Add the product to the database
        db.add(new_product)

    db.commit()
    db.refresh(new_product)

    for product in schema.products:
        used_quantity = db.query(func.sum(ProductOutDb.quntity)).filter(
            ProductOutDb.category == product.category,
            ProductOutDb.bike_category == product.bike_category,
            ProductOutDb.product_name == product.product_name,
            ProductOutDb.color == product.color,
            ProductOutDb.size == product.size,
            ProductOutDb.city == product.city
        ).scalar() or 0

        total_quantity = db.query(func.sum(ProductDB.quantity)).filter(
            ProductDB.category == product.category,
            ProductDB.bike_category == product.bike_category,
            ProductDB.product_name == product.product_name,
            ProductDB.color == product.color,
            ProductDB.size == product.size,
            ProductDB.city == product.city
        ).scalar() or 0

        remaining_quantity = total_quantity - used_quantity

        product_data.append({
            "category": product.category,
            "bike_category": product.bike_category,
            "product_name": product.product_name,
            "color" : product.color,
            "size" : product.size,
            "city" : product.city,
            "name" : product.name,
            "user" : current_user,
            "remaining_quantity": remaining_quantity
        })

    return product_data


# @inventory_out_router.post('/inventory/transfer')
# def trasfer_inventory(
#     schema : TransferSchema,
#     db : Session = Depends(get_db),
#     current_user : str = Depends(get_current_user)
# ):
    
#     new_product = TransferDb(
#         trasfer_id=str(uuid.uuid4()),
#         product_name=schema.product_name,
#         HSN_code = schema.HSN_code,
#         category=schema.category,
#         bike_category=schema.bike_category,
#         quntity=schema.quantity,
#         size=schema.size,
#         city=schema.city,
#         color=schema.color,
#         created_at = datetime.now(),
#         updated_at = datetime.now(),
#         is_deleted = False,
#         user = current_user
#     )

#     db.add(new_product)

#     db.commit()
#     db.refresh(new_product)

#     used_quantity = db.query(func.sum(ProductOutDb.quntity)).filter(
#         ProductOutDb.category == schema.category,
#         ProductOutDb.bike_category == schema.bike_category,
#         ProductOutDb.product_name == schema.product_name,
#         ProductOutDb.color == schema.color,
#         ProductOutDb.size == schema.size,
#         ProductOutDb.city == schema.city
#     ).scalar() or 0

#     total_quantity = db.query(func.sum(ProductDB.quantity)).filter(
#         TransferDb.category == schema.category,
#         TransferDb.bike_category == schema.bike_category,
#         TransferDb.product_name == schema.product_name,
#         TransferDb.color == schema.color,
#         TransferDb.size == schema.size,
#         TransferDb.city == schema.city
#     ).scalar() or 0

#     remaining_quantity = total_quantity - used_quantity

#     return {
#         "category": schema.category,
#         "bike_category": schema.bike_category,
#         "product_name": schema.product_name,
#         "color" : schema.color,
#         "size" : schema.size,
#         "city" : schema.city,
#         "user" : current_user,
#         "remaining_quantity": remaining_quantity
#     }


# @inventory_out_router.post('v2/inventory/transfer')
# def trasfer_inventory(
#     schema : TransferSchema,
#     db : Session = Depends(get_db),
#     current_user : str = Depends(get_current_user)
# ):
    
#     new_product = TransferDb(
#         trasfer_id=str(uuid.uuid4()),
#         product_name=schema.product_name,
#         HSN_code = schema.HSN_code,
#         category=schema.category,
#         bike_category=schema.bike_category,
#         quntity=schema.quantity,
#         size=schema.size,
#         city=schema.city,
#         color=schema.color,
#         created_at = datetime.now(),
#         updated_at = datetime.now(),
#         is_deleted = False,
#         user = current_user
#     )

#     db.add(new_product)

#     db.commit()
#     db.refresh(new_product)

#     used_quantity = db.query(func.sum(ProductOutDb.quntity)).filter(
#         ProductOutDb.category == schema.category,
#         ProductOutDb.bike_category == schema.bike_category,
#         ProductOutDb.product_name == schema.product_name,
#         ProductOutDb.color == schema.color,
#         ProductOutDb.size == schema.size,
#         ProductOutDb.city == schema.city
#     ).scalar() or 0

#     total_quantity = db.query(func.sum(ProductDB.quantity)).filter(
#         TransferDb.category == schema.category,
#         TransferDb.bike_category == schema.bike_category,
#         TransferDb.product_name == schema.product_name,
#         TransferDb.color == schema.color,
#         TransferDb.size == schema.size,
#         TransferDb.city == schema.city
#     ).scalar() or 0

#     remaining_quantity = total_quantity - used_quantity

#     return {
#         "category": schema.category,
#         "bike_category": schema.bike_category,
#         "product_name": schema.product_name,
#         "color" : schema.color,
#         "size" : schema.size,
#         "city" : schema.city,
#         "user" : current_user,
#         "remaining_quantity": remaining_quantity
#     }


@inventory_out_router.get("/v2/get/inventory/used")
def get_used_inventory_v2(db : Session = Depends(get_db)):

    db_products = db.query(UsedProduct).all()

    if not db_products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Used product not found"
        )
    
    product_list = []
    for product in db_products:
        print(product)

        bikes = db.query(BikeDb).filter(BikeDb.bike_id.in_(product.master_products.bike_category)).all()
        final_product = {
        "EPC_code" : product.EPC_code,
        "product_name" : product.master_products.product_name,
        "category" : product.master_products.category_relation.category_name,
        "category_id" : product.master_products.category,
        "HSN_code" : product.master_products.HSN_code,
        "bike_category" : [bike.bike_name for bike in bikes],
        "bike_id" : product.master_products.bike_category,
        "size" : product.master_products.size_relation.size_name,
        "size_id" : product.master_products.size,
        "color" : product.master_products.color_relation.color_name,
        "color_id" : product.master_products.color,
        "unit" : product.master_products.unit_relation.unit_name,
        "unit_id" : product.master_products.unit,
        "gst" : product.master_products.gst_relation.gst_percentage,
        "gst_id" : product.master_products.gst,
        "created_at" : product.created_at,
        "updated_at" : product.updated_at,
        "quantity" : product.quantity,
        "user" : product.user,
        "comment" : product.comment,
        "city" : product.city_relation.city_name,
        "bike_number" : product.bike_number
        }

        product_list.append(final_product)

    return{
        "status" : status.HTTP_200_OK,
        "message" : "product categories fetched successfully",
        "products" : product_list
    }


@inventory_out_router.get("/v2/get/top/products", response_model=ProductTopListResponse)
def get_top_products(db: Session = Depends(get_db)):
    top_products = (
        db.query(
            UsedProduct.EPC_code,
            MasterProductDB.product_name,
            func.sum(cast(UsedProduct.quantity, Integer)).label('total_quantity')
        )
        .join(UsedProduct.master_products)
        .group_by(UsedProduct.EPC_code, MasterProductDB.product_name)
        .order_by(func.sum(cast(UsedProduct.quantity, Integer)).desc())
        .limit(10)
        .all()
    )

    return ProductTopListResponse(
        top_products=[
            ProductTopResponse(
                EPC_code=epc_code,
                product_name=product_name,
                total_quantity=total_quantity
            ) for epc_code, product_name, total_quantity in top_products
        ]
    )


@inventory_out_router.get("/v3/get/top/products", response_model=ProductTopListResponse)
def get_top_products_v3(
    start_date: date = Query(default="2024-01-01"),
    end_date: date = Query(default=date.today()),
    db: Session = Depends(get_db)
):
    top_products = (
        db.query(
            UsedProduct.EPC_code,
            MasterProductDB.product_name,
            func.sum(cast(UsedProduct.quantity, Integer)).label('total_quantity')
        )
        .join(UsedProduct.master_products)
        .filter(cast(UsedProduct.created_at, Date) >= start_date, cast(UsedProduct.created_at, Date) <= end_date)
        .group_by(UsedProduct.EPC_code, MasterProductDB.product_name)
        .order_by(func.sum(cast(UsedProduct.quantity, Integer)).desc())
        .limit(10)
        .all()
    )


    return ProductTopListResponse(
        top_products=[
            ProductTopResponse(
                EPC_code=epc_code,
                product_name=product_name,
                total_quantity=total_quantity
            ) for epc_code, product_name, total_quantity in top_products
        ]
    )