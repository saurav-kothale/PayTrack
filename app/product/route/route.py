from datetime import date, datetime
from doctest import master
from itertools import product
from math import prod
from nis import cat
from operator import and_
from typing import Optional
from unicodedata import category
from xml.sax import default_parser_list
from fastapi import APIRouter, Depends, HTTPException, status
from numpy import empty, integer
from pydantic import HttpUrl
from app.Inventory_in.bike_category.model import BikeDb
from app.Inventory_in.category_new.model import NewCategoryDb
from app.Inventory_in.color_category.model import ColorDb
from app.Inventory_in.gst_category.model import GST
from app.Inventory_in.master_product.model import MasterProductDB
from app.Inventory_in.size_category.model import SizeDb
from app.Inventory_in.unit_category.model import Unit
from app.product.schema.schema import ProductCountResponse, ProductSchema, ProductUpdateSchema, ProductUseSchema
from sqlalchemy.orm import Session
from app.product.model.model import ProductDB, AuditUpdateDB, AuditTransferDB, InvoiceProductsDB, InStockProducts, UsedProduct
from app.inventory_out.model import ProductOutDb
from app.Inventory_in.model import InventoryDB, InvoiceDetailsDB
from app.utils.util import get_current_user
from app.vendor.model import Vendor
from database.database import SessionLocal, get_db
import uuid
from sqlalchemy import Subquery, distinct, func, and_, case
from app.product.view.view import add_gst, get_month_abbreviation, new_add_gst
from sqlalchemy import desc
from sqlalchemy.orm import aliased
from sqlalchemy import extract
from datetime import datetime
from sqlalchemy import Integer
import calendar


product_router = APIRouter()


@product_router.post("/product/{invoice_id}")
def create_product(
    invoice_id: str,
    product : ProductSchema,
    current_user : str = Depends(get_current_user),
    db : Session = Depends(get_db),

):
    invoice = db.query(InvoiceDetailsDB).filter(InvoiceDetailsDB.invoice_id == invoice_id, InvoiceDetailsDB.is_deleted == False).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice ID not found")

    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    # Create a new product

    quntity_amount = product.quantity * product.amount

    gst_amount = new_add_gst(product.GST, quntity_amount)


    new_product = InvoiceProductsDB(
        id=str(uuid.uuid4()),
        EPC_code = product.EPC_code,
        category=product.category,
        bike_category=product.bike_category,
        quantity=product.quantity,
        size=product.size,
        city=product.city,
        color=product.color,
        user = current_user,
        invoice_id=invoice_id,
        HSN_code = product.HSN_code,
        GST = product.GST,
        unit = product.unit,
        amount = product.amount,
        total_amount = quntity_amount,
        amount_with_gst = gst_amount,
        created_at = formatted_datetime,
        updated_at = formatted_datetime,
        is_deleted = False
    )

    # Add the product to the database
    db.add(new_product)

    # available_product = db.query(InStockProducts).filter(InStockProducts.EPC_code == product.EPC_code, InStockProducts.city == product.city).first()

    # if available_product:
        
    #     available_product.available_quantity += product.quantity

    # else :

    #     add_product = InStockProducts(
    #         id = str(uuid.uuid4()),
    #         EPC_code = product.EPC_code,
    #         city = product.city,
    #         available_quantity = product.quantity
    #     )

    #     db.add(add_product)

    # master_product = db.query(MasterProductDB).filter(MasterProductDB.EPC_code == product.EPC_code).first()

    # category_name = db.query(NewCategoryDb).filter(NewCategoryDb.category_id == master_product.category).first()

    # bike = db.query(BikeDb).filter(BikeDb.bike_id == master_product.bike_category).first()

    # color = db.query(ColorDb).filter(ColorDb.color_id == master_product.color).first()

    #     # gst = db.query(GST).filter(GST.gst_id == master_product.gst).first()

    # size = db.query(SizeDb).filter(SizeDb.size_id == master_product.size).first()

        # unit = db.query(Unit).filter(Unit.unit_id == master_product.unit).first()

        # vendor = db.query(Vendor).filter(Vendor.vendor_id == master_product.vendor).first()

        
    # final_product = {
    #         "product_name" : master_product.product_name,
    #         "hsn_code" : master_product.HSN_code,
    #         "category": category_name.category_name,
    #         "bike_category": bike.bike_name,
    #         "color": color.color_name,
    #         "size": size.size_name,
    #         "city": product.city,
    #         "product_name": master_product.product_name,
    #         "EPC_code" : master_product.EPC_code,
    #         "quantity" : product.quantity,
    #         "total_amount" : quntity_amount
    #     }

    db.commit()
    db.refresh(new_product)


    return{
        "status" : status.HTTP_201_CREATED,
        "message" : "product created successfully",
        "product" : new_product
    }

@product_router.post("/v2/product/{invoice_id}")
def create_product_v2(
    invoice_id: str,
    product : ProductSchema,
    current_user : str = Depends(get_current_user),
    db : Session = Depends(get_db),

):
    invoice = db.query(InvoiceDetailsDB).filter(InvoiceDetailsDB.invoice_id == invoice_id, InvoiceDetailsDB.is_deleted == False).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice ID not found")

    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    # Create a new product

    quntity_amount = product.quantity * product.amount

    gst_amount = new_add_gst(product.GST, quntity_amount)


    new_product = InvoiceProductsDB(
        id=str(uuid.uuid4()),
        EPC_code = product.EPC_code,
        # category=product.category,
        # bike_category=product.bike_category,
        quantity=product.quantity,
        # size=product.size,
        city=product.city,
        # color=product.color,
        user = current_user,
        invoice_id=invoice_id,
        # HSN_code = product.HSN_code,
        # GST = product.GST,
        # unit = product.unit,
        amount = product.amount,
        total_amount = quntity_amount,
        amount_with_gst = gst_amount,
        created_at = formatted_datetime,
        updated_at = formatted_datetime,
        is_deleted = False
    )

    # Add the product to the database
    db.add(new_product)

    available_product = db.query(InStockProducts).filter(InStockProducts.EPC_code == product.EPC_code, InStockProducts.city == product.city).first()

    if available_product:
        
        available_product.available_quantity += product.quantity

    else :

        add_product = InStockProducts(
            id = str(uuid.uuid4()),
            EPC_code = product.EPC_code,
            city = product.city,
            available_quantity = product.quantity
        )

        db.add(add_product)

    # master_product = db.query(MasterProductDB).filter(MasterProductDB.EPC_code == product.EPC_code).first()

    # category_name = db.query(NewCategoryDb).filter(NewCategoryDb.category_id == master_product.category).first()

    # bike = db.query(BikeDb).filter(BikeDb.bike_id == master_product.bike_category).first()

    # color = db.query(ColorDb).filter(ColorDb.color_id == master_product.color).first()

    # gst = db.query(GST).filter(GST.gst_id == master_product.gst).first()

    # size = db.query(SizeDb).filter(SizeDb.size_id == master_product.size).first()

    # unit = db.query(Unit).filter(Unit.unit_id == master_product.unit).first()
    db.commit()
    db.refresh(new_product)

    # bikes = db.query(BikeDb).filter(BikeDb.bike_id.in_(new_product.master_products.bike_category), BikeDb.is_deleted == False).all()

    # breakpoint()

    final_product = {
        "id" : new_product.id,
        "product_name" : new_product.master_products.product_name,
        "EPC_code" : product.EPC_code,
        "category" : new_product.master_products.category_relation.category_name,
        "bike_category" : product.bike_category,
        "quantity" : product.quantity,
        "size" : new_product.master_products.size_relation.size_name,
        "city" : new_product.city_relation.city_name,
        "color" : new_product.master_products.color_relation.color_name,
        "user" : current_user,
        "invoice_id" : invoice_id,
        "HSN_code" : product.HSN_code,
        "GST" : new_product.master_products.gst_relation.gst_percentage,
        "unit" : new_product.master_products.unit_relation.unit_name,
        "amount" : product.amount,
        "total_amount" : quntity_amount,
        "amount_with_gst" : gst_amount,
        "created_at" : formatted_datetime,
        "updated_at" : formatted_datetime,
        }



    return{
        "status" : status.HTTP_201_CREATED,
        "message" : "product created successfully",
        "product" : final_product
    }


@product_router.get("/products/{id}")
def get_product(id : str, db : Session = Depends(get_db)):
    db_product = db.query(InvoiceProductsDB).filter(InvoiceProductsDB.id == id, InvoiceProductsDB.is_deleted == False).first()

    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    if db_product.invoice.is_deleted:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Inventory is Deleted of this product"
        )

    return{
        "status" : status.HTTP_200_OK,
        "product" : db_product
    }


@product_router.get("/products")
def get_products(db : Session = Depends(get_db)):

    db_products = db.query(ProductDB).filter(ProductDB.is_deleted == False).all()

    if not db_products:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="Product not found"
        )

    return {
        "status" : status.HTTP_200_OK,
        "message" : "Products Fetched Successfully",
        "products" : db_products
    }


@product_router.patch("/products/{product_id}")
def update_product(
    product_id : str, 
    data : ProductSchema, 
    db : Session = Depends(get_db),
    current_user : str = Depends(get_current_user)
):  
    db_product = db.query(InvoiceProductsDB).filter(InvoiceProductsDB.id == product_id, InvoiceProductsDB.is_deleted == False).first()

    if db_product is None:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= "Product is not found to update"
        )
    
    changes = []
    
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    quntity_amount = data.quantity * data.amount

    gst_amount = new_add_gst(data.GST, quntity_amount)

       
    if data.quantity != db_product.quantity:
        changes.append({
            "changed_field" : "EPC_code",
            "old_value" : str(db_product.EPC_code),
            "new_value" : str(data.EPC_code)
        })

    if data.quantity != db_product.quantity:
        changes.append({
            "changed_field" : "Quantity",
            "old_value" : str(db_product.quantity),
            "new_value" : str(data.quantity)
        })

    if data.city != db_product.city:
        changes.append({
            "changed_field" : "City",
            "old_value" : str(db_product.city),
            "new_value" : str(data.city)
        })
    

    if data.amount != db_product.amount:
        changes.append({
            "changed_field" : "Amount",
            "old_value" : str(db_product.amount),
            "new_value" : str(data.amount)
        })

    db_product.EPC_code = data.EPC_code
    db_product.quantity = data.quantity
    db_product.updated_at = formatted_datetime
    db_product.amount = data.amount
    db_product.city = data.city
    db_product.total_amount = quntity_amount
    db_product.amount_with_gst = gst_amount


    db.commit()

    for change in changes:
        audit_entry = AuditUpdateDB(
            id = str(uuid.uuid4()),
            invoice_id = db_product.invoice_id,
            EPC_code=data.EPC_code,
            field_changed=change["changed_field"],
            old_value=(change["old_value"]),
            new_value=(change["new_value"]),
            changed_by = current_user["user_name"],
            changed_at = datetime.now()
        )
        db.add(audit_entry)
    
    db.commit()

    return {
        "message": "Product Updated Sucessfully",
        "status": status.HTTP_200_OK,
        "product" : {
            "EPC_code" : db_product.EPC_code,
            "city" : db_product.city,
            "product_quantity" : db_product.quantity,
            "product_updated_at" : db_product.updated_at,
            "product_amount" : db_product.amount,
            "product_total_amount" : db_product.total_amount,
            "product_with_gst" : db_product.amount_with_gst
        }
    }


@product_router.patch("/v2/products/{product_id}")
def update_product_v2(
    product_id : str, 
    data : ProductSchema, 
    db : Session = Depends(get_db),
    current_user : str = Depends(get_current_user)
):  
    db_product = db.query(InvoiceProductsDB).filter(InvoiceProductsDB.id == product_id, InvoiceProductsDB.is_deleted == False).first()


    if db_product is None:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= "Product is not found to update"
        )
    
    changes = []
    
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    quntity_amount = data.quantity * data.amount

    gst_amount = new_add_gst(data.GST, quntity_amount)

       
    if data.quantity != db_product.quantity:
        changes.append({
            "changed_field" : "EPC_code",
            "old_value" : str(db_product.EPC_code),
            "new_value" : str(data.EPC_code)
        })

    if data.quantity != db_product.quantity:
        changes.append({
            "changed_field" : "Quantity",
            "old_value" : str(db_product.quantity),
            "new_value" : str(data.quantity)
        })

    if data.city != db_product.city:
        changes.append({
            "changed_field" : "City",
            "old_value" : str(db_product.city),
            "new_value" : str(data.city)
        })
    

    if data.amount != db_product.amount:
        changes.append({
            "changed_field" : "Amount",
            "old_value" : str(db_product.amount),
            "new_value" : str(data.amount)
        })



    old_product = db.query(InStockProducts).filter(InStockProducts.EPC_code == db_product.EPC_code, InStockProducts.city == db_product.city).first()

    old_product.available_quantity -= db_product.quantity

    new_product = db.query(InStockProducts).filter(InStockProducts.EPC_code == data.EPC_code, InStockProducts.city == data.city).first()
    if not new_product:
        db_new_stock = InStockProducts(
            id = str(uuid.uuid4()),
            EPC_code = data.EPC_code,
            city = data.city,
            available_quantity = data.quantity
        )

        db.add(db_new_stock)
    
    else:
        new_product.available_quantity += data.quantity

    db_product.EPC_code = data.EPC_code
    db_product.quantity = data.quantity
    db_product.updated_at = formatted_datetime
    db_product.amount = data.amount
    db_product.city = data.city
    db_product.total_amount = quntity_amount
    db_product.amount_with_gst = gst_amount

    db.commit()

    for change in changes:
        audit_entry = AuditUpdateDB(
            id = str(uuid.uuid4()),
            invoice_id = db_product.invoice_id,
            EPC_code=data.EPC_code,
            field_changed=change["changed_field"],
            old_value=(change["old_value"]),
            new_value=(change["new_value"]),
            changed_by = current_user["user_name"],
            changed_at = datetime.now()
        )
        db.add(audit_entry)
    
    db.commit()

    return {
        "message": "Product Updated Sucessfully",
        "status": status.HTTP_200_OK,
        "product" : {
            "id" : db_product.id,
            "EPC_code" : db_product.EPC_code,
            "product_name" : db_product.master_products.product_name,
            "category" : db_product.master_products.category_relation.category_name,
            "bike_category" : data.bike_category,
            "size" : db_product.master_products.size_relation.size_name,
            "color" : db_product.master_products.color_relation.color_name,
            "GST" : db_product.master_products.gst_relation.gst_percentage,
            "unit" : db_product.master_products.unit_relation.unit_name,
            "HSN_code" : db_product.master_products.HSN_code,
            "city" : db_product.city_relation.city_name,
            "quantity" : db_product.quantity,
            "updated_at" : db_product.updated_at,
            "amount" : db_product.amount,
            "total_amount" : db_product.total_amount,
            "product_with_gst" : db_product.amount_with_gst,
            
        }
    }


@product_router.delete("/products/{product_id}")
def delete_product(
    product_id : str,
    db : Session = Depends(get_db)
):
    db_product = db.query(InvoiceProductsDB).filter(InvoiceProductsDB.id == product_id, InvoiceProductsDB.is_deleted == False).first()

    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product Not Found to Delete"
        )
    
    stock_product = db.query(InStockProducts).filter(InStockProducts.EPC_code == db_product.EPC_code, InStockProducts.city == db_product.city).first()
    
    if stock_product.available_quantity < db_product.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Can't delete the product because product quantity is {db_product.quantity} and available quantity is {stock_product.available_quantity}"
        )
    
    stock_product.available_quantity -= db_product.quantity

    db_product.is_deleted = True

    db.commit()

    return{
        "status" : status.HTTP_200_OK,
        "message" : "Product deleted sucessfully"
    }

@product_router.get("/products/invoice/{invoice_id}")
def get_inventory_products(
    invoice_id : str,
    db : Session = Depends(get_db) 
):
    
    db_products = db.query(InvoiceProductsDB).filter(InvoiceProductsDB.invoice_id == invoice_id, InvoiceProductsDB.is_deleted == False).all()

    if not db_products:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="Products Not Found for given invoice id"
        )

    product_list = []

    for product in db_products:

        master_product = db.query(MasterProductDB).filter(MasterProductDB.EPC_code == product.EPC_code).first()

        product = {
            "product_name" : master_product.product_name,
            "category" : master_product.category,
            "bike_category" : master_product.bike_category,
            "size" : master_product.size,
            "color" : master_product.color,
            "unit" : master_product.unit,
            "gst" : master_product.gst,
            "city" : product.city,
            "total_amount" : product.total_amount,
            "quantity" : product.quantity,
            "HSN_code" : master_product.HSN_code,
            "user" : master_product.user
        }
    
        product_list.append(product)
    
    return {
        "status" : status.HTTP_200_OK,
        "message" : "Product Fetched successfully",
        "product" : product_list
    }

@product_router.get("/v2/products/invoice/{invoice_id}")
def get_inventory_products_v2(
    invoice_id : str,
    db : Session = Depends(get_db) 
):
    
    db_products = db.query(InvoiceProductsDB).filter(InvoiceProductsDB.invoice_id == invoice_id, InvoiceProductsDB.is_deleted == False).all()

    if not db_products:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="Products Not Found for given invoice id"
        )
    
    product_list = []

    for product in db_products:

        bikes = db.query(BikeDb).filter(BikeDb.bike_id.in_(product.master_products.bike_category)).all()
        
        final_product = {
            "product_id" : product.id,
            "product_name" : product.master_products.product_name,
            "HSN_code" : product.master_products.HSN_code,
            "category": product.master_products.category_relation.category_name,
            "bike_category": [bike.bike_name for bike in bikes],
            "color": product.master_products.color_relation.color_name,
            "size": product.master_products.size_relation.size_name,
            "city": product.city_relation.city_name,
            "city_id" : product.city,
            "unit" : product.master_products.unit_relation.unit_name,
            "EPC_code" : product.EPC_code,
            "quantity" : product.quantity,
            "amount" : product.amount,
            "total_amount" : product.total_amount,
            "amount_with_gst" : product.amount_with_gst,
            "user" : product.master_products.user
        }

        product_list.append(final_product)
    
    return {
        "status" : status.HTTP_200_OK,
        "message" : "Product Fetched successfully",
        "product" : product_list
    }


@product_router.get("/product/category/deprecated")
def retrieve_products_by_category123_deprecated(db: Session = Depends(get_db)):
    # Subquery to calculate the total used quantity
    used_quantity_subquery = db.query(
        ProductOutDb.HSN_code,
        ProductOutDb.product_name,
        ProductOutDb.category,
        ProductOutDb.bike_category,
        ProductOutDb.color,
        ProductOutDb.size,
        ProductOutDb.city,
        func.sum(ProductOutDb.quntity).label("total_used_quantity")
    ).group_by(
        ProductOutDb.HSN_code, 
        ProductOutDb.product_name,
        ProductOutDb.category,
        ProductOutDb.bike_category,
        ProductOutDb.color,
        ProductOutDb.size,
        ProductOutDb.city
    ).subquery()

    # Subquery to calculate the total quantity for each product
    total_quantity_subquery = db.query(
        InvoiceProductsDB.HSN_code,
        InvoiceProductsDB.category,
        InvoiceProductsDB.bike_category,
        InvoiceProductsDB.color,
        InvoiceProductsDB.size,
        InvoiceProductsDB.city,
        InvoiceProductsDB.product_name,
        func.sum(InvoiceProductsDB.quantity).label("total_quantity")
    ).group_by(
        InvoiceProductsDB.HSN_code,
        InvoiceProductsDB.category,
        InvoiceProductsDB.bike_category,
        InvoiceProductsDB.color,
        InvoiceProductsDB.size,
        InvoiceProductsDB.city,
        InvoiceProductsDB.product_name
    ).subquery()

    # Main query to retrieve distinct products and calculate remaining quantity
    db_distinct = db.query(
        total_quantity_subquery.c.HSN_code,
        total_quantity_subquery.c.category,
        total_quantity_subquery.c.bike_category,
        total_quantity_subquery.c.color,
        total_quantity_subquery.c.size,
        total_quantity_subquery.c.city,
        total_quantity_subquery.c.product_name,
        func.coalesce(total_quantity_subquery.c.total_quantity - used_quantity_subquery.c.total_used_quantity, total_quantity_subquery.c.total_quantity).label('remaining_quantity')
    ).outerjoin(
        used_quantity_subquery,
        and_(
            total_quantity_subquery.c.HSN_code == used_quantity_subquery.c.HSN_code,
            total_quantity_subquery.c.product_name == used_quantity_subquery.c.product_name,
            total_quantity_subquery.c.category == used_quantity_subquery.c.category,
            total_quantity_subquery.c.bike_category == used_quantity_subquery.c.bike_category,
            total_quantity_subquery.c.color == used_quantity_subquery.c.color,
            total_quantity_subquery.c.size == used_quantity_subquery.c.size,
            total_quantity_subquery.c.city == used_quantity_subquery.c.city
        )
    ).all()

    # Format the result
    result = [
        {
            "hsn_code" : row.HSN_code,
            "category": row.category,
            "bike_category": row.bike_category,
            "color": row.color,
            "size": row.size,
            "city": row.city,
            "product_name": row.product_name,
            "remaining_quantity": row.remaining_quantity
        } 
        for row in db_distinct
    ]
    
    return {
        "distinct_values": result
    }


@product_router.get("/product/category")
def retrieve_products_by_category123(db: Session = Depends(get_db)):
    # Subquery to calculate the total used quantity
    used_quantity_subquery = db.query(
        ProductOutDb.HSN_code,
        ProductOutDb.product_name,
        ProductOutDb.category,
        ProductOutDb.bike_category,
        ProductOutDb.color,
        ProductOutDb.size,
        ProductOutDb.city,
        func.sum(ProductOutDb.quntity).label("total_used_quantity")
    ).group_by(
        ProductOutDb.HSN_code, 
        ProductOutDb.product_name,
        ProductOutDb.category,
        ProductOutDb.bike_category,
        ProductOutDb.color,
        ProductOutDb.size,
        ProductOutDb.city
    ).subquery()

    # Subquery to calculate the total quantity for each product
    total_quantity_subquery = db.query(
        ProductDB.HSN_code,
        ProductDB.category,
        ProductDB.bike_category,
        ProductDB.color,
        ProductDB.size,
        ProductDB.city,
        ProductDB.product_name,
        ProductDB.created_at,  # Include created_at in the subquery
        func.sum(ProductDB.quantity).label("total_quantity")
    ).group_by(
        ProductDB.HSN_code,
        ProductDB.category,
        ProductDB.bike_category,
        ProductDB.color,
        ProductDB.size,
        ProductDB.city,
        ProductDB.product_name,
        # InvoiceProductsDB.created_at  # Group by created_at as well
    ).subquery()

    # Main query to retrieve distinct products and calculate remaining quantity
    db_distinct = db.query(
        total_quantity_subquery.c.HSN_code,
        total_quantity_subquery.c.category,
        total_quantity_subquery.c.bike_category,
        total_quantity_subquery.c.color,
        total_quantity_subquery.c.size,
        total_quantity_subquery.c.city,
        total_quantity_subquery.c.product_name,
        func.coalesce(total_quantity_subquery.c.total_quantity - used_quantity_subquery.c.total_used_quantity, total_quantity_subquery.c.total_quantity).label('remaining_quantity')
    ).outerjoin(
        used_quantity_subquery,
        and_(
            total_quantity_subquery.c.HSN_code == used_quantity_subquery.c.HSN_code,
            total_quantity_subquery.c.product_name == used_quantity_subquery.c.product_name,
            total_quantity_subquery.c.category == used_quantity_subquery.c.category,
            total_quantity_subquery.c.bike_category == used_quantity_subquery.c.bike_category,
            total_quantity_subquery.c.color == used_quantity_subquery.c.color,
            total_quantity_subquery.c.size == used_quantity_subquery.c.size,
            total_quantity_subquery.c.city == used_quantity_subquery.c.city
        )
    ).order_by(desc(total_quantity_subquery.c.created_at))  # Order by created_at in descending order

    # Format the result
    result = [
        {
            "hsn_code" : row.HSN_code,
            "category": row.category,
            "bike_category": row.bike_category,
            "color": row.color,
            "size": row.size,
            "city": row.city,
            "product_name": row.product_name,
            "remaining_quantity": row.remaining_quantity
        } 
        for row in db_distinct
    ]
    
    return {
        "distinct_values": result
    }


@product_router.get("/products/amount/sum/{invoice_id}")
def match_sum(
    invoice_id : str ,
    db: Session = Depends(get_db)
):
    total_sum = db.query(func.sum(InvoiceProductsDB.amount_with_gst)).filter(InvoiceProductsDB.invoice_id == invoice_id).scalar()

    invoice = db.query(InvoiceDetailsDB).filter(InvoiceDetailsDB.invoice_id == invoice_id).first()

    price_diffrence = invoice.invoice_amount - total_sum

    return {
        "status" : status.HTTP_200_OK,
        "Price Difference" : price_diffrence
    }


@product_router.get("/product/category/v2")
def retrieve_products_by_category_v2(db: Session = Depends(get_db)):
    # Subquery to calculate the total used quantity
    used_quantity_subquery = db.query(
        ProductOutDb.HSN_code,
        ProductOutDb.product_name,
        ProductOutDb.category,
        ProductOutDb.bike_category,
        ProductOutDb.color,
        ProductOutDb.size,
        ProductOutDb.city,
        func.sum(ProductOutDb.quntity).label("total_used_quantity")
    ).group_by(
        ProductOutDb.HSN_code, 
        ProductOutDb.product_name,
        ProductOutDb.category,
        ProductOutDb.bike_category,
        ProductOutDb.color,
        ProductOutDb.size,
        ProductOutDb.city
    ).subquery()

    # Subquery to calculate the total quantity for each product
    total_quantity_subquery = db.query(
        ProductDB.HSN_code,
        ProductDB.category,
        ProductDB.bike_category,
        ProductDB.color,
        ProductDB.size,
        ProductDB.city,
        ProductDB.product_name,
        # ProductDB.created_at,  # Include created_at in the subquery
        func.sum(ProductDB.quantity).label("total_quantity")
    ).group_by(
        ProductDB.HSN_code,
        ProductDB.category,
        ProductDB.bike_category,
        ProductDB.color,
        ProductDB.size,
        ProductDB.city,
        ProductDB.product_name,
        # InvoiceProductsDB.created_at  # Group by created_at as well
    ).subquery()

    # Main query to retrieve distinct products and calculate remaining quantity
    ProductDBAlias = aliased(ProductDB)

# Main query to retrieve distinct products and calculate remaining quantity
    db_distinct = db.query(
        total_quantity_subquery.c.HSN_code,
        total_quantity_subquery.c.category,
        total_quantity_subquery.c.bike_category,
        total_quantity_subquery.c.color,
        total_quantity_subquery.c.size,
        total_quantity_subquery.c.city,
        total_quantity_subquery.c.product_name,
        func.coalesce(
            total_quantity_subquery.c.total_quantity - used_quantity_subquery.c.total_used_quantity, 
            total_quantity_subquery.c.total_quantity
        ).label('remaining_quantity'),
        ProductDBAlias.created_at,  # Include created_at for ordering
        func.row_number().over(
            partition_by=[
                total_quantity_subquery.c.HSN_code,
                total_quantity_subquery.c.category,
                total_quantity_subquery.c.bike_category,
                total_quantity_subquery.c.color,
                total_quantity_subquery.c.size,
                total_quantity_subquery.c.city,
                total_quantity_subquery.c.product_name
            ],
            order_by=desc(ProductDBAlias.created_at)
        ).label('row_number')
    ).outerjoin(
        used_quantity_subquery,
        and_(
            total_quantity_subquery.c.HSN_code == used_quantity_subquery.c.HSN_code,
            total_quantity_subquery.c.product_name == used_quantity_subquery.c.product_name,
            total_quantity_subquery.c.category == used_quantity_subquery.c.category,
            total_quantity_subquery.c.bike_category == used_quantity_subquery.c.bike_category,
            total_quantity_subquery.c.color == used_quantity_subquery.c.color,
            total_quantity_subquery.c.size == used_quantity_subquery.c.size,
            total_quantity_subquery.c.city == used_quantity_subquery.c.city
        )
    ).join(
        ProductDBAlias,  # Join with the alias to fetch created_at
        and_(
            total_quantity_subquery.c.HSN_code == ProductDBAlias.HSN_code,
            total_quantity_subquery.c.product_name == ProductDBAlias.product_name,
            total_quantity_subquery.c.category == ProductDBAlias.category,
            total_quantity_subquery.c.bike_category == ProductDBAlias.bike_category,
            total_quantity_subquery.c.color == ProductDBAlias.color,
            total_quantity_subquery.c.size == ProductDBAlias.size,
            total_quantity_subquery.c.city == ProductDBAlias.city
        )
    ).subquery()

    # Query to filter only the latest entries
    final_query = db.query(
        db_distinct.c.HSN_code,
        db_distinct.c.category,
        db_distinct.c.bike_category,
        db_distinct.c.color,
        db_distinct.c.size,
        db_distinct.c.city,
        db_distinct.c.product_name,
        db_distinct.c.remaining_quantity
    ).filter(
        db_distinct.c.row_number == 1
    ).order_by(
        desc(db_distinct.c.created_at)
    )

    # Format the result
    result = [
        {
            "hsn_code": row.HSN_code,
            "category": row.category,
            "bike_category": row.bike_category,
            "color": row.color,
            "size": row.size,
            "city": row.city,
            "product_name": row.product_name,
            "remaining_quantity": row.remaining_quantity
        }
        for row in final_query
    ]

    return {
        "distinct_values": result
    }


@product_router.get("/product/category/v3")
def retrieve_products_by_category_v3(db: Session = Depends(get_db)):
    # Subquery to calculate the total used quantity
    used_quantity_subquery = db.query(
        ProductOutDb.HSN_code,
        ProductOutDb.product_name,
        ProductOutDb.category,
        ProductOutDb.bike_category,
        ProductOutDb.color,
        ProductOutDb.size,
        ProductOutDb.city,
        func.sum(ProductOutDb.quantity).label("total_used_quantity")
    ).group_by(
        ProductOutDb.HSN_code, 
        ProductOutDb.product_name,
        ProductOutDb.category,
        ProductOutDb.bike_category,
        ProductOutDb.color,
        ProductOutDb.size,
        ProductOutDb.city
    ).subquery()

    # Subquery to calculate the total quantity for each product
    total_quantity_subquery = db.query(
        InvoiceProductsDB.HSN_code,
        InvoiceProductsDB.category,
        InvoiceProductsDB.bike_category,
        InvoiceProductsDB.color,
        InvoiceProductsDB.size,
        InvoiceProductsDB.city,
        InvoiceProductsDB.product_name,
        func.sum(InvoiceProductsDB.quantity).label("total_quantity")
    ).group_by(
        InvoiceProductsDB.HSN_code,
        InvoiceProductsDB.category,
        InvoiceProductsDB.bike_category,
        InvoiceProductsDB.color,
        InvoiceProductsDB.size,
        InvoiceProductsDB.city,
        InvoiceProductsDB.product_name
    ).subquery()

    # Subquery to calculate the transferred quantity
    transfer_quantity_subquery = db.query(
        TransferDb.HSN_code,
        TransferDb.category,
        TransferDb.bike_category,
        TransferDb.color,
        TransferDb.size,
        TransferDb.product_name,
        func.sum(TransferDb.quantity).label("transfer_quantity")
    ).group_by(
        TransferDb.HSN_code, 
        TransferDb.product_name,
        TransferDb.category,
        TransferDb.bike_category,
        TransferDb.color,
        TransferDb.size
    ).subquery()

    # Main query to retrieve distinct products and calculate remaining quantity
    ProductDBAlias = aliased(InvoiceProductsDB)
    db_distinct = db.query(
        total_quantity_subquery.c.HSN_code,
        total_quantity_subquery.c.category,
        total_quantity_subquery.c.bike_category,
        total_quantity_subquery.c.color,
        total_quantity_subquery.c.size,
        total_quantity_subquery.c.city,
        total_quantity_subquery.c.product_name,
        func.coalesce(
            total_quantity_subquery.c.total_quantity - used_quantity_subquery.c.total_used_quantity - transfer_quantity_subquery.c.transfer_quantity, 
            total_quantity_subquery.c.total_quantity
        ).label('remaining_quantity'),
        ProductDBAlias.created_at,  # Include created_at for ordering
        func.row_number().over(
            partition_by=[
                total_quantity_subquery.c.HSN_code,
                total_quantity_subquery.c.category,
                total_quantity_subquery.c.bike_category,
                total_quantity_subquery.c.color,
                total_quantity_subquery.c.size,
                total_quantity_subquery.c.city,
                total_quantity_subquery.c.product_name
            ],
            order_by=desc(ProductDBAlias.created_at)
        ).label('row_number')
    ).outerjoin(
        used_quantity_subquery,
        and_(
            total_quantity_subquery.c.HSN_code == used_quantity_subquery.c.HSN_code,
            total_quantity_subquery.c.product_name == used_quantity_subquery.c.product_name,
            total_quantity_subquery.c.category == used_quantity_subquery.c.category,
            total_quantity_subquery.c.bike_category == used_quantity_subquery.c.bike_category,
            total_quantity_subquery.c.color == used_quantity_subquery.c.color,
            total_quantity_subquery.c.size == used_quantity_subquery.c.size,
            total_quantity_subquery.c.city == used_quantity_subquery.subquery.c.city
        )
    ).join(
        ProductDBAlias,
        and_(
            total_quantity_subquery.c.HSN_code == ProductDBAlias.HSN_code,
            total_quantity_subquery.c.product_name == ProductDBAlias.product_name,
            total_quantity_subquery.c.category == ProductDBAlias.category,
            total_quantity_subquery.c.bike_category == ProductDBAlias.bike_category,
            total_quantity_subquery.c.color == ProductDBAlias.color,
            total_quantity_subquery.c.size == ProductDBAlias.size,
            total_quantity_subquery.c.city == ProductDBAlias.city
        )
    ).subquery()

    # Query to filter only the latest entries
    final_query = db.query(
        db_distinct.c.HSN_code,
        db_distinct.c.category,
        db_distinct.c.bike_category,
        db_distinct.c.color,
        db_distinct.c.size,
        db_distinct.c.city,
        db_distinct.c.product_name,
        db_distinct.c.remaining_quantity
    ).filter(
        db_distinct.c.row_number == 1
    ).order_by(
        desc(db_distinct.c.created_at)
    )

    # Format the result
    result = [
        {
            "hsn_code": row.HSN_code,
            "category": row.category,
            "bike_category": row.bike_category,
            "color": row.color,
            "size": row.size,
            "city": row.city,
            "product_name": row.product_name,
            "remaining_quantity": row.remaining_quantity
        }
        for row in final_query
    ]

    return {
        "distinct_values": result
    }

@product_router.post('/products/transfer/{invoice_id}/{product_id}')
def transfer_product(
    invoice_id : str,
    product_id : str,
    product : ProductSchema,
    current_user : str = Depends(get_current_user),
    db : Session = Depends(get_db),
):
    
    # invoice = db.query(InvoiceDetailsDB).filter(InvoiceDetailsDB.invoice_id == invoice_id).first()
    # if not invoice:
    #     raise HTTPException(status_code=404, detail="Invoice ID not found")
    

    db_product = db.query(InvoiceProductsDB).filter(InvoiceProductsDB.product_id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= "Prodcut not found"
        )
    
    if db_product.quantity < product.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please select valide quantity"
        )    
    
    transfer_audit = AuditTransferDB(
        id = str(uuid.uuid4()),
        invoice_id = invoice_id,
        product_id = product_id,
        product_name = db_product.product_name,
        from_city = db_product.city,
        to_city = product.city,
        total_product = db_product.quantity,
        transfer_quantity = product.quantity,
        transfer_at = datetime.now(),
        transfer_by = current_user["user_name"]

    )
    db.add(transfer_audit) 

    db.commit()

    db_transfer_product = db.query(InvoiceProductsDB).filter(
        InvoiceProductsDB.HSN_code == product.HSN_code,
        InvoiceProductsDB.product_name == product.product_name,
        InvoiceProductsDB.category == product.category,
        InvoiceProductsDB.bike_category == product.bike_category,
        InvoiceProductsDB.city == product.city,
        InvoiceProductsDB.size == product.size,
        InvoiceProductsDB.color == product.color
    ).first()


    if db_transfer_product:

        new_quantity = db_transfer_product.quantity + product.quantity
        quntity_amount = new_quantity * product.amount
        gst_amount = add_gst(product.GST.value, quntity_amount)
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

        db_transfer_product.quantity = new_quantity
        db_transfer_product.total_amount = quntity_amount
        db_transfer_product.amount_with_gst = gst_amount
        db_transfer_product.updated_at = formatted_datetime


        current_quntity = db_product.quantity
        remaining_quntity = current_quntity - product.quantity
        updated_quntity_amount = remaining_quntity * db_product.amount
        updated_gst_amount = add_gst(db_product.GST, updated_quntity_amount)

        db_product.quantity = remaining_quntity
        db_product.total_amount = updated_quntity_amount
        db_product.amount_with_gst = updated_gst_amount
        db_product.updated_at = formatted_datetime

        db.commit()

        return {
            "status" : status.HTTP_200_OK,
            "message" : "Recored Transfer successfully",
            "transfer_product_id" : product_id,
            "transfered_product_id" : db_transfer_product.product_id
        }
    
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    # Create a new product

    quntity_amount = product.quantity * product.amount

    gst_amount = add_gst(product.GST.value, quntity_amount)


    
    new_product = InvoiceProductsDB(
        product_id=str(uuid.uuid4()),
        product_name=product.product_name,
        category=product.category,
        bike_category=product.bike_category,
        quantity=product.quantity,
        size=product.size,
        city=product.city,
        color=product.color,
        user = current_user,
        invoice_id=invoice_id,
        HSN_code = product.HSN_code,
        GST = product.GST,
        unit = product.unit,
        amount = product.amount,
        total_amount = quntity_amount,
        amount_with_gst = gst_amount,
        created_at = formatted_datetime,
        updated_at = formatted_datetime,
        is_deleted = False
    )

    current_quntity = db_product.quantity
    remaining_quntity = current_quntity - product.quantity
    updated_quntity_amount = remaining_quntity * db_product.amount
    updated_gst_amount = add_gst(db_product.GST, updated_quntity_amount)

    db_product.quantity = remaining_quntity
    db_product.total_amount = updated_quntity_amount
    db_product.amount_with_gst = updated_gst_amount
    db_product.updated_at = formatted_datetime

    

    db.add(new_product)       

    db.commit()

    return{
        "status" : status.HTTP_200_OK,
        "message" : "Recored Transfer successfully",
        "transfer_product_id" : product_id,
        "transfered_product_id" : new_product.product_id
    }


@product_router.get('/v2/available/quantity')
def available_quantity(db : Session = Depends(get_db)):

    available_products = db.query(InStockProducts).all()

    if not available_products:

        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="Available quantity is Empty"
        )

    product_list = []

    for product in available_products:

        # bikes = db.query(BikeDb).filter(BikeDb)product.invoice_product_relation

        bikes = db.query(BikeDb).filter(BikeDb.bike_id.in_(product.master_product_relation.bike_category)).all()

        final_product = {
            "product_name" : product.master_product_relation.product_name,
            "hsn_code" : product.master_product_relation.HSN_code,
            "category": product.master_product_relation.category_relation.category_name,
            "bike_category" : [bike.bike_name for bike in bikes],
            "color": product.master_product_relation.color_relation.color_name,
            "size": product.master_product_relation.size_relation.size_name,
            "city": product.city_relation.city_name,
            "EPC_code" : product.EPC_code,
            "quantity" : product.available_quantity,
            "city_id" : product.city
            
        }

        product_list.append(final_product)


    return{
        "status" : status.HTTP_200_OK,
        "message" : "available quantity fetched successfully",
        "available_quantity" : product_list
    }


@product_router.post("/v2/use/product")
def product_use(
    schema : ProductUseSchema,
    db : Session = Depends(get_db),
    current_user : str = Depends(get_current_user)
    
):

    db_product = db.query(InStockProducts).filter(InStockProducts.EPC_code == schema.EPC_code, InStockProducts.city == schema.city).first()

    if not db_product:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="product not found"
        )
    
    if db_product.available_quantity <= schema.quantity:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This much quantity is not available"
        )
    
    db_product.available_quantity -= schema.quantity
    
    
    new_product = UsedProduct(
        id = str(uuid.uuid4()),
        EPC_code = schema.EPC_code,
        city = schema.city,
        quantity = schema.quantity,
        comment = schema.comment,
        user = current_user,
        created_at = datetime.now(),
        updated_at = datetime.now()
    )

    db.add(new_product)

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
            "city": db_product.city_relation.city_name,
            "EPC_code" : db_product.EPC_code,
            "user" : current_user,
            "comment" : new_product.comment,
            "created_at" : new_product.created_at,
            "updated_at" : new_product.updated_at, 
            "quantity" : db_product.available_quantity,
            
        } 
    }


# @product_router.get("/v2/products/year/{year}")
# def get_monthly_product_quantities(
#     year: int,
#     db: Session = Depends(get_db)
# ):
#     try:
#         # Validate year
#         current_year = datetime.now().year
#         if year < 1900 or year > current_year:
#             raise ValueError(f"Invalid year. Please provide a year between 1900 and {current_year}.")

#         # Query to get monthly quantities
#         monthly_quantities = db.query(
#             extract('month', InvoiceDetailsDB.inventory_paydate).label('month'),
#             func.sum(InvoiceProductsDB.quantity).label('total_quantity')
#         ).join(
#             InvoiceProductsDB,
#             InvoiceDetailsDB.invoice_id == InvoiceProductsDB.invoice_id
#         ).filter(
#             extract('year', InvoiceDetailsDB.inventory_paydate) == year,
#             InvoiceDetailsDB.is_deleted == False,
#             InvoiceProductsDB.is_deleted == False
#         ).group_by(
#             extract('month', InvoiceDetailsDB.inventory_paydate)
#         ).order_by(
#             extract('month', InvoiceDetailsDB.inventory_paydate)
#         ).all()

#         # Convert results to a list of dictionaries with month abbreviations
#         result = [
#             {
#                 "month": get_month_abbreviation(int(month)),
#                 "total_quantity": int(total_quantity)  # Convert to int for JSON serialization
#             }
#             for month, total_quantity in monthly_quantities
#         ]

#         return {"year": year, "monthly_quantities": result}

#     except ValueError as ve:
#         raise HTTPException(status_code=400, detail=str(ve))
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    

@product_router.get("/v2/products/year/{year}")
def get_monthly_product_quantities(
    year: int,
    db: Session = Depends(get_db)
):
    try:
        # Validate year
        current_year = datetime.now().year
        if year < 1900 or year > current_year:
            raise ValueError(f"Invalid year. Please provide a year between 1900 and {current_year}.")

        # Query to get monthly quantities for new products
        new_product_quantities = db.query(
            extract('month', InvoiceDetailsDB.inventory_paydate).label('month'),
            func.sum(InvoiceProductsDB.quantity).label('total_quantity')
        ).join(
            InvoiceProductsDB,
            InvoiceDetailsDB.invoice_id == InvoiceProductsDB.invoice_id
        ).filter(
            extract('year', InvoiceDetailsDB.inventory_paydate) == year,
            InvoiceDetailsDB.is_deleted == False,
            InvoiceProductsDB.is_deleted == False
        ).group_by(
            extract('month', InvoiceDetailsDB.inventory_paydate)
        ).all()

        # Query to get monthly quantities for used products
        used_product_quantities = db.query(
            extract('month', UsedProduct.created_at).label('month'),
            func.sum(func.cast(UsedProduct.quantity, Integer)).label('used_quantity')
        ).filter(
            extract('year', UsedProduct.created_at) == year
        ).group_by(
            extract('month', UsedProduct.created_at)
        ).all()

        # Combine new and used product data
        monthly_data = {}
        for month, total_quantity in new_product_quantities:
            month_abbr = get_month_abbreviation(int(month))
            monthly_data[month_abbr] = {"total_quantity": int(total_quantity), "used_quantity": 0}

        for month, used_quantity in used_product_quantities:
            month_abbr = get_month_abbreviation(int(month))
            if month_abbr in monthly_data:
                monthly_data[month_abbr]["used_quantity"] = int(used_quantity)
            else:
                monthly_data[month_abbr] = {"total_quantity": 0, "used_quantity": int(used_quantity)}

        # Convert to list and sort by month
        result = [
            {"month": month, **data}
            for month, data in sorted(monthly_data.items(), key=lambda x: list(calendar.month_abbr).index(x[0]))
        ]

        return {"year": year, "monthly_quantities": result}

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    

@product_router.get("/v3/products/range/")
def get_monthly_product_quantities_v3(
    start_date: date = datetime(2024, 1, 1).date(),
    end_date: date = datetime.now().date(),
    db: Session = Depends(get_db)
):
    try:
        # Validate date range
        if start_date > end_date:
            raise ValueError("Start date must be before or equal to end date.")

        # Query to get monthly quantities for new products
        new_product_quantities = db.query(
            extract('month', InvoiceDetailsDB.inventory_paydate).label('month'),
            func.sum(InvoiceProductsDB.quantity).label('total_quantity')
        ).join(
            InvoiceProductsDB,
            InvoiceDetailsDB.invoice_id == InvoiceProductsDB.invoice_id
        ).filter(
            InvoiceDetailsDB.inventory_paydate.between(start_date, end_date),
            InvoiceDetailsDB.is_deleted == False,
            InvoiceProductsDB.is_deleted == False
        ).group_by(
            extract('month', InvoiceDetailsDB.inventory_paydate)
        ).all()

        # Query to get monthly quantities for used products
        used_product_quantities = db.query(
            extract('month', UsedProduct.created_at).label('month'),
            func.sum(func.cast(UsedProduct.quantity, Integer)).label('used_quantity')
        ).filter(
            UsedProduct.created_at.between(start_date, end_date)
        ).group_by(
            extract('month', UsedProduct.created_at)
        ).all()

        print(used_product_quantities)


        # Combine new and used product data
        monthly_data = {}
        for month, total_quantity in new_product_quantities:
            month_abbr = get_month_abbreviation(int(month))
            monthly_data[month_abbr] = {"total_quantity": int(total_quantity), "used_quantity": 0}

        for month, used_quantity in used_product_quantities:
            print(month)
            print(used_quantity)
            month_abbr = get_month_abbreviation(int(month))
            if month_abbr in monthly_data:
                monthly_data[month_abbr]["used_quantity"] = int(used_quantity)
            else:
                monthly_data[month_abbr] = {"total_quantity": 0, "used_quantity": int(used_quantity)}

        # Convert to list and sort by month
        result = [
            {"month": month, **data}
            for month, data in sorted(monthly_data.items(), key=lambda x: list(calendar.month_abbr).index(x[0]))
        ]

        return {"start_date": start_date, "end_date": end_date, "monthly_quantities": result}

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
