from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.vendor.model import Vendor
from database.database import get_db
from app.Inventory_in.vendor_category.model import VendorCategoryModel
from app.Inventory_in.vendor_category.schema import VendorCategory, VendorCategoryUpdate
import uuid
from datetime import datetime
from app.Inventory_in.master_product.view import EPCCodeGenerator


vendor_category_router = APIRouter()


@vendor_category_router.get("/vendors")
def get_vendors(
    db : Session = Depends(get_db)
):
    
    db_vendor = db.query(VendorCategoryModel).filter(VendorCategoryModel.is_deleted == False).all()

    if not db_vendor:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="Vendors not found"
        )
    
    return{
        "status" : status.HTTP_200_OK,
        "message" : "Record fetched successfully",
        "venders" : db_vendor
    }


@vendor_category_router.get("/vendors/{vendor_id}")
def get_vendor(
    vendor_id : str,
    db : Session = Depends(get_db)
):
    
    db_vendor = db.query(VendorCategoryModel).filter(VendorCategoryModel.Vendor_id == vendor_id, VendorCategoryModel.is_deleted == False).first()

    if not db_vendor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="vendor not found"
        )
    
    return{
        "status" : status.HTTP_200_OK,
        "message" : "vendor fetched successfully",
        "vendor" : db_vendor
    }

 
@vendor_category_router.post("/vendor")
def create_vendor(
    schema : VendorCategory,
    db : Session = Depends(get_db)
):
    db_vendor = db.query(VendorCategoryModel).filter(VendorCategoryModel.Vendor_name == schema.vendor_name, VendorCategoryModel.is_deleted == False).first()

    if db_vendor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "Vendor already present"
        )
    
    code_generator = EPCCodeGenerator("vendor category", db=db)

    new_vendor = VendorCategoryModel(
        Vendor_id = code_generator.generate_code("VC", 3),
        Vendor_name = schema.vendor_name,
        Contact_number = schema.contact_number,
        Address = schema.address,
        Email_id = schema.email_id,
        City = schema.city,
        Payment_term = schema.payment_terms,
        GST_Number = schema.gst_number,
        created_at = datetime.now(),
        updated_at = datetime.now(),
        is_deleted = False
    )


    db.add(new_vendor)

    db.commit()

    vendor = {
        "Vendor_id" : new_vendor.Vendor_id,
        "Vendor_name" : new_vendor.Vendor_name,
        "Contact_number" : new_vendor.Contact_number,
        "Address" : new_vendor.Address,
        "Email_id" : new_vendor.Email_id,
        "City" : new_vendor.City,
        "Payment_term" : new_vendor.Payment_term,
        "GST_Number" : new_vendor.GST_Number,
        "created_at" : new_vendor.created_at,
        "updated_at" : new_vendor.updated_at
    }

    return{
        "status" : status.HTTP_201_CREATED,
        "message" : "Vendor Created Successfully",
        "vendor" : vendor
    }
    

@vendor_category_router.patch("/vendors/{vendor_id}")
def update_vendor(
    vendor_id : str,
    schema : VendorCategoryUpdate,
    db : Session = Depends(get_db)
):
    
    db_vendor = db.query(VendorCategoryModel).filter(VendorCategoryModel.Vendor_id == vendor_id).first()

    if not db_vendor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "Vendor not found to update"
        )
    
    db_vendor.Vendor_name = schema.vendor_name
    db_vendor.Contact_number = schema.contact_number
    db_vendor.Address = schema.address
    db_vendor.Email_id = schema.email_id
    db_vendor.City = schema.city
    db_vendor.Payment_term = schema.payment_terms
    db_vendor.GST_Number = schema.gst_number
    db_vendor.updated_at = datetime.now()

    db.commit()

    vendor = {
        "vendor_id" : db_vendor.Vendor_id,
        "vendor_name" : db_vendor.Vendor_name,
        "Contact_number" : db_vendor.Contact_number,
        "Address" : db_vendor.Address,
        "Email_id" : db_vendor.Email_id,
        "City" : db_vendor.City,
        "Payment_term" : db_vendor.Payment_term,
        "GST_Number" : db_vendor.GST_Number,
        "created_at" : db_vendor.created_at,
        "updated_at" : db_vendor.updated_at
    }

    return{
        "status" : status.HTTP_200_OK,
        "message" : "vendor updated succesfully",
        "vendor" : vendor
    }


@vendor_category_router.delete("/vendor/{vendor_id}")
def delete_vendor(
    vendor_id : str,
    db : Session = Depends(get_db)
):
    db_vendor = db.query(VendorCategoryModel).filter(VendorCategoryModel.Vendor_id == vendor_id).first()

    if not db_vendor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vendor not found to delete"
        )
    
    db_vendor.is_deleted = True

    db.commit()

    return{
        "status" : status.HTTP_200_OK,
        "message" : "Vendor deleted successfully",
        "vendor" : db_vendor.Vendor_id
    }


@vendor_category_router.get("/vendor/count")
def vendor_count(db : Session = Depends(get_db)):

    db_vendors = db.query(VendorCategoryModel).filter(VendorCategoryModel.is_deleted == False).count()    
    

    return {
        "total_vendors" : db_vendors
    }