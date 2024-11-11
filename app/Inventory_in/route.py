from ast import List
from datetime import datetime
from enum import unique
from itertools import product
from typing import Optional
from urllib import response
from DateTime import Timezones
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    status,
    Query
)
from sqlalchemy import desc, false, func, true
from app.Inventory_in.category_new.model import NewCategoryDb
from app.Inventory_in.view import get_month_abbreviation
from app.product.model.model import InvoiceProductsDB, ProductDB
from app.utils.util import get_current_user
from database.database import get_db
from sqlalchemy.orm import Session
from app.Inventory_in.schema import InventoryResponseV2, Invetory, InvetoryResponse, InvetoryUpdate
from app.Inventory_in.model import InventoryDB, InvoiceDetailsDB
import uuid
from app.file_system.config import s3_client
from app import setting
from zoneinfo import ZoneInfo
from sqlalchemy import extract, distinct, case
import calendar
from datetime import date
from fastapi.responses import JSONResponse


inventory_router = APIRouter()
inventory = setting.INVENTORY

@inventory_router.post("/inventories/upload/image")
async def upload_inventory_image(file : UploadFile = None):
    if file is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="image not found"
        )
    
    file_extention = (file.filename).split(".")[1]

    if file_extention not in ["jpg", "jpeg"]:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail= "Please Upload valid file JPG or JPEG"
        )
    
    file_id = uuid.uuid4()
    file_key = f"{file_id}/{file.filename}"

    try:

        s3_client.upload_fileobj(file.file, inventory, file_key)


    except Exception as e:
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload image : {e}"
        )
    
    
    return {
        "status" : status.HTTP_202_ACCEPTED,
        "message" : "File uploaded successfully",
        "image_url" : f"https://{inventory}.s3.amazonaws.com/{file_key}",
        "file_name" : file.filename
    }
        

@inventory_router.post("/inventories")
def create_inventory(
    inventory: Invetory,
    db: Session = Depends(get_db),
    current_user : str = Depends(get_current_user)
):
    
    # if inventory.invoice_date < datetime.now().date():
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Invoice date cannot be in the past"
    #     )

    db_invoice = db.query(InvoiceDetailsDB).filter(
        InvoiceDetailsDB.invoice_number == inventory.invoice_number,
        InvoiceDetailsDB.vendor == inventory.vendor
    ).first()

    if db_invoice:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="invoice already exist"
        )
    
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    record = InvoiceDetailsDB(
        invoice_id=str(uuid.uuid4()),
        invoice_number=inventory.invoice_number,
        invoice_amount=inventory.invoice_amount,
        invoice_date=inventory.invoice_date,
        inventory_paydate=inventory.inventory_paydate,
        vendor=inventory.vendor,
        invoice_image_id=inventory.invoice_image_id,
        user=current_user,
        created_at = formatted_datetime,
        updated_at = formatted_datetime
    )

    db.add(record)

    db.commit()

    return {
        "status": status.HTTP_201_CREATED,
        "message": "Inventory created successfully",
        "invoice": {
            "invoice_id": str(record.invoice_id),  # Convert uuid to string for JSON response
            "invoice_number": record.invoice_number,
            "invoice_amount": record.invoice_amount,
            "invoice_date": record.invoice_date,
            "inventory_paydate": record.inventory_paydate,
            "vendor": record.vendor,
            "created_at" : record.created_at,
            "updated_at" : record.updated_at,
            "invoice_image_id": record.invoice_image_id,
            "user" : record.user,
        }
    }


@inventory_router.get("/inventories/{invoice_id}")
def get_inventory(invoice_id: str, db: Session = Depends(get_db)):

    db_inventory = (
        db.query(InvoiceDetailsDB)
        .filter(InvoiceDetailsDB.invoice_id == invoice_id)
        .first()
    )

    if db_inventory is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory not found please check inventory number",
        )
    

    return {
        "data": db_inventory,
        "status": status.HTTP_200_OK,
        "message": "Inventory Fetched Successfully",
    }


@inventory_router.get("/inventories")
def get_inventories(db: Session = Depends(get_db)):

    db_inventory = (
        db.query(
            InvoiceDetailsDB,
            func.count(InvoiceProductsDB.id).filter(InvoiceProductsDB.is_deleted == False).label("product_count")
        )
        .outerjoin(InvoiceProductsDB, InvoiceDetailsDB.invoice_id == InvoiceProductsDB.invoice_id)
        .group_by(InvoiceDetailsDB.invoice_id)
        .order_by(desc(InvoiceDetailsDB.created_at))
        .all()
    )

    if not db_inventory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Inventories Not Found"
        )

    # Create response
    inventory_responses = [
        InventoryResponseV2(
            invoice_id=inventory.InvoiceDetailsDB.invoice_id,
            invoice_number=inventory.InvoiceDetailsDB.invoice_number,
            invoice_amount=inventory.InvoiceDetailsDB.invoice_amount,
            invoice_date=inventory.InvoiceDetailsDB.invoice_date,
            inventory_paydate=inventory.InvoiceDetailsDB.inventory_paydate,
            vendor=inventory.InvoiceDetailsDB.vendor,
            invoice_image_id=inventory.InvoiceDetailsDB.invoice_image_id,
            product_count=inventory.product_count,
            user=inventory.InvoiceDetailsDB.user,
            updated_at = inventory.InvoiceDetailsDB.updated_at,
            created_at = inventory.InvoiceDetailsDB.created_at,

        )
        for inventory in db_inventory
    ]

    return inventory_responses



@inventory_router.patch("/inventories/{invoice_id}")
def update_inventory(
    invoice_id: str, 
    inventory: InvetoryUpdate, 
    db: Session = Depends(get_db),
    current_user : str = Depends(get_current_user)

):

    db_inventory = (
        db.query(InvoiceDetailsDB)
        .filter(InvoiceDetailsDB.invoice_id == invoice_id)
        .first()
    )

    if db_inventory is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory not found to update",
        )
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")


    db_inventory.invoice_number = inventory.invoice_number
    db_inventory.invoice_amount = inventory.invoice_amount
    db_inventory.invoice_date = inventory.invoice_date
    db_inventory.inventory_paydate = inventory.inventory_paydate
    db_inventory.vendor = inventory.vendor
    db_inventory.invoice_image_id = inventory.invoice_image_id
    db_inventory.updated_at = formatted_datetime

    db.commit()

    

    return {
        "message": "Inventory Updated Sucessfully",
        "status": status.HTTP_200_OK,
        "inventory" : {
            "invoice_number" : db_inventory.invoice_number,
            "invoice_amount" : db_inventory.invoice_amount,
            "invoice_date" : db_inventory.invoice_date,
            "inventory_paydate" : db_inventory.inventory_paydate,
            "vendor" : db_inventory.vendor,
            "image_id" : db_inventory.invoice_image_id,
            "create_at" : db_inventory.created_at,
            "updated_at" : db_inventory.updated_at,
            "user" : current_user
        }
    }


@inventory_router.delete("/inventories/{invoice_id}")
def delete_inventory(invoice_id: str, db: Session = Depends(get_db)):

    inventory_delete = db.query(InvoiceDetailsDB).filter(
        InvoiceDetailsDB.invoice_id == invoice_id
    ).first()

    if inventory_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory not found to delete",
        )
    
    products = db.query(ProductDB).filter(ProductDB.invoice_id == invoice_id).all()


    for product in products:
        db.delete(product)

    db.delete(inventory_delete)
    db.commit()

    return {
        "status": status.HTTP_202_ACCEPTED,
        "message": "Inventory deleted sucessfully",
    }


# @inventory_router.get("/inventories/vendors/billing")
# def get_vendor_by_billing(
#     db : Session = Depends(get_db)
# ):
    
#     db_vendors=db.query(
#         InvoiceDetailsDB.vendor,
#         func.sum(InvoiceDetailsDB.invoice_amount).label('total_billing'),
#     ).group_by(InvoiceDetailsDB.vendor)

#     return{
#         "billing" : db_vendors
#     }


@inventory_router.get("/inventories/vendors/billing")
def get_vendor_by_billing(
    db: Session = Depends(get_db)
):
    # Query to get total billing by vendor
    db_vendors = db.query(
        InvoiceDetailsDB.vendor,
        func.sum(InvoiceDetailsDB.invoice_amount).label('total_billing')
    ).group_by(InvoiceDetailsDB.vendor).all()

    # Convert query results to a list of dictionaries
    billing_list = [{'vendor_name': vendor, 'amount': total_billing} for vendor, total_billing in db_vendors]

    # Calculate the total amount across all vendors
    total_amount = sum(total_billing for _, total_billing in db_vendors)

    return {
        "billing": billing_list,
        "total_amount": total_amount
    }


@inventory_router.get("/v2/inventories/vendors/billing")
def get_vendor_by_billing_v2(
    start_date: date = Query(default="2024-01-01"),
    end_date: date = Query(default=date.today()),
    db: Session = Depends(get_db)
):
    # Query to get total billing by vendor within the date range
    db_vendors = (
        db.query(
            InvoiceDetailsDB.vendor,
            func.sum(InvoiceDetailsDB.invoice_amount).label('total_billing')
        )
        .filter(InvoiceDetailsDB.invoice_date >= start_date, InvoiceDetailsDB.invoice_date <= end_date)
        .group_by(InvoiceDetailsDB.vendor)
        .all()
    )

    # Convert query results to a list of dictionaries
    billing_list = [{'vendor_name': vendor, 'amount': total_billing} for vendor, total_billing in db_vendors]

    # Calculate the total amount across all vendors
    total_amount = sum(total_billing for _, total_billing in db_vendors)

    return {
        "billing": billing_list,
        "total_amount": total_amount
    }


@inventory_router.get("/inventory/count")
def count_inventory(db : Session = Depends(get_db)):
    
    db_count = db.query(InvoiceDetailsDB).filter(InvoiceDetailsDB.is_deleted == False).count()

    db_category_count = db.query(NewCategoryDb).filter(NewCategoryDb.is_deleted == False).count()


    return {
        "total_inventory" : db_count,
        "total_category" : db_category_count
    }


@inventory_router.get("/v2/inventories/years/{year}")
def get_monthly_product_quantities(
    year: int,
    db: Session = Depends(get_db)
):
    try:
        # Validate year
        current_year = datetime.now().year
        if year < 1900 or year > current_year:
            raise ValueError(f"Invalid year. Please provide a year between 1900 and {current_year}.")

        # Query to get monthly invoice amount and vendor count for the given year
        monthly_data_query = db.query(
            extract('month', InvoiceDetailsDB.inventory_paydate).label('month'),
            func.sum(InvoiceDetailsDB.invoice_amount).label('total_amount'),
            func.count(distinct(InvoiceDetailsDB.vendor)).label('vendor_count')
        ).filter(
            extract('year', InvoiceDetailsDB.inventory_paydate) == year,
            InvoiceDetailsDB.is_deleted == False,
        ).group_by(
            extract('month', InvoiceDetailsDB.inventory_paydate)
        ).all()

        # Prepare data for the response
        monthly_data = {}
        for month, total_amount, vendor_count in monthly_data_query:
            month_abbr = get_month_abbreviation(int(month))
            monthly_data[month_abbr] = {
                "total_amount": float(total_amount),
                "vendor_count": int(vendor_count)
            }

        # Convert the dictionary to a sorted list by month
        result = [
            {"month": month, **data}
            for month, data in sorted(monthly_data.items(), key=lambda x: list(calendar.month_abbr).index(x[0]))
        ]

        return {"year": year, "monthly_quantities": result}

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    

@inventory_router.get("/invoice-stats")
def get_invoice_stats(
    start_date: Optional[date] = date(2024,1,1),
    end_date: Optional[date] = date.today(), 
    db: Session = Depends(get_db)
):

    total_amounts = (
        db.query(
            func.to_char(InvoiceDetailsDB.invoice_date, 'YYYY-MM').label("month"),
            func.sum(InvoiceDetailsDB.invoice_amount).label("total_amount")
        )
        .filter(InvoiceDetailsDB.invoice_date >= start_date, InvoiceDetailsDB.invoice_date <= end_date)
        .filter(InvoiceDetailsDB.is_deleted == False)
        .group_by(func.to_char(InvoiceDetailsDB.invoice_date, 'YYYY-MM'))
        .subquery()
    )

    # Calculate total distinct products and sum of quantities by month
    product_stats = (
        db.query(
            func.to_char(InvoiceDetailsDB.invoice_date, 'YYYY-MM').label("month"),
            func.count(distinct(InvoiceProductsDB.EPC_code)).label("total_distinct_product_count"),
            func.sum(InvoiceProductsDB.quantity).label("total_quantity")
        )
        .join(InvoiceDetailsDB, InvoiceProductsDB.invoice_id == InvoiceDetailsDB.invoice_id)
        .filter(InvoiceDetailsDB.invoice_date >= start_date, InvoiceDetailsDB.invoice_date <= end_date)
        .filter(InvoiceDetailsDB.is_deleted == False, InvoiceProductsDB.is_deleted == False)
        .group_by(func.to_char(InvoiceDetailsDB.invoice_date, 'YYYY-MM'))
        .subquery()
    )

    # Combine results from both subqueries
    results = (
        db.query(
            total_amounts.c.month,
            total_amounts.c.total_amount,
            product_stats.c.total_distinct_product_count,
            product_stats.c.total_quantity
        )
        .outerjoin(product_stats, total_amounts.c.month == product_stats.c.month)
        .order_by(total_amounts.c.month)
        .all()
    )

    # Month mapping
    month_map = {
        "01": "jan",
        "02": "feb",
        "03": "mar",
        "04": "apr",
        "05": "may",
        "06": "jun",
        "07": "jul",
        "08": "aug",
        "09": "sep",
        "10": "oct",
        "11": "nov",
        "12": "dec"
    }

    # Convert result to a list of dictionaries
    return [
        {
            "month": month_map[month.split('-')[1]],
            "total_amount": total_amount,
            "total_distinct_product_count": total_distinct_product_count or 0,
            "total_quantity": total_quantity or 0
        }
        for month, total_amount, total_distinct_product_count, total_quantity in results
    ]