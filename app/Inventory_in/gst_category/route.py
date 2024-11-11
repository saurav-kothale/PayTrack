from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.Inventory_in.gst_category.model import GST
from app.Inventory_in.gst_category.schema import GSTSchema, GSTUpdateSchema
from app.utils.util import get_current_user
from database.database import get_db
import uuid
from datetime import datetime
from app.Inventory_in.master_product.view import EPCCodeGenerator

gst_router = APIRouter()

@gst_router.get('/gsts')
def get_gsts(db : Session = Depends(get_db)):
    
    db_gst = db.query(GST).filter(GST.is_deleted == False).all()

    if not db_gst:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="GSTs not found"
        )
    
    return {
        "status" : status.HTTP_200_OK,
        "message" : "GSTs fetched successfully",
        "gsts" : db_gst
    }

@gst_router.get('/v3/gsts')
def get_gsts(db : Session = Depends(get_db), current_user = Depends(get_current_user)):
    
    if current_user["inventory_privileges"]["read"] == False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "You don't have enoght permission to read GSTs"
        )

    db_gst = db.query(GST).filter(GST.is_deleted == False).all()

    if not db_gst:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="GSTs not found"
        )
    
    return {
        "status" : status.HTTP_200_OK,
        "message" : "GSTs fetched successfully",
        "gsts" : db_gst
    }


@gst_router.get("/gsts/{gst_id}")
def get_gst(
    gst_id : str,
    db : Session = Depends(get_db)
):
    db_gst = db.query(GST).filter(GST.gst_id == gst_id, GST.is_deleted == False).first()

    if not db_gst:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="gst not found"
        )
    
    return {
        "status" : status.HTTP_200_OK,
        "message" : "gst fetched successfully",
        "gst" : db_gst
    }


@gst_router.post("/gsts")
def create_gst(
    schema : GSTSchema,
    db : Session = Depends(get_db)
):
    
    db_gst = db.query(GST).filter(GST.gst_percentage == schema.gst_perentage, GST.is_deleted == False).first()

    if db_gst:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="gst percentage already exist"
        )
        
    code_generator = EPCCodeGenerator("gst category", db=db)

    new_gst = GST(
        gst_id = code_generator.generate_code("GC", 3),
        gst_percentage = schema.gst_perentage,
        created_at = datetime.now(),
        updated_at = datetime.now(),
        is_deleted = False
    )

    db.add(new_gst)

    db.commit()

    gst = {
        "gst_id" : new_gst.gst_id,
        "gst_percentage" : new_gst.gst_percentage,
        "created_at" : new_gst.created_at,
        "updated_at" : new_gst.updated_at
    }

    return{
        "status" : status.HTTP_201_CREATED,
        "message" : "gst created successfully",
        "gst" : gst
    }

@gst_router.post("/v3/gsts")
def create_gst_v3(
    schema : GSTSchema,
    db : Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if current_user["inventory_privileges"]["edit"] == False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "You don't have enoght permission to create GST"
        )

    db_gst = db.query(GST).filter(GST.gst_percentage == schema.gst_perentage, GST.is_deleted == False).first()

    if db_gst:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="gst percentage already exist"
        )
        
    code_generator = EPCCodeGenerator("gst category", db=db)

    new_gst = GST(
        gst_id = code_generator.generate_code("GC", 3),
        gst_percentage = schema.gst_perentage,
        created_at = datetime.now(),
        updated_at = datetime.now(),
        is_deleted = False
    )

    db.add(new_gst)

    db.commit()

    gst = {
        "gst_id" : new_gst.gst_id,
        "gst_percentage" : new_gst.gst_percentage,
        "created_at" : new_gst.created_at,
        "updated_at" : new_gst.updated_at
    }

    return{
        "status" : status.HTTP_201_CREATED,
        "message" : "gst created successfully",
        "gst" : gst
    }


@gst_router.patch("/gst/{gst_id}")
def update_gst(
    gst_id : str,
    schema : GSTUpdateSchema,
    db : Session = Depends(get_db)
):
    
    db_gst = db.query(GST).filter(GST.gst_id == gst_id).first()

    if not db_gst:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "GST not found to update"
        )
    
    db_gst.gst_percentage = schema.gst_percentage
    db_gst.updated_at = datetime.now()

    db.commit()

    gst = {
        "gst_id" : db_gst.gst_id,
        "gst_percentage" : db_gst.gst_percentage,
        "created_at" : db_gst.created_at,
        "updated_at" : db_gst.updated_at
    }

    return{
        "status" : status.HTTP_200_OK,
        "message" : "gst updated succesfully",
        "gst" : gst
    }


@gst_router.patch("/v3/gst/{gst_id}")
def update_gst_v3(
    gst_id : str,
    schema : GSTUpdateSchema,
    db : Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if current_user["inventory_privileges"]["edit"] == False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "You don't have enoght permission to update GST"
        )

    db_gst = db.query(GST).filter(GST.gst_id == gst_id).first()

    if not db_gst:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "GST not found to update"
        )
    
    db_gst.gst_percentage = schema.gst_percentage
    db_gst.updated_at = datetime.now()

    db.commit()

    gst = {
        "gst_id" : db_gst.gst_id,
        "gst_percentage" : db_gst.gst_percentage,
        "created_at" : db_gst.created_at,
        "updated_at" : db_gst.updated_at
    }

    return{
        "status" : status.HTTP_200_OK,
        "message" : "gst updated succesfully",
        "gst" : gst
    }


@gst_router.delete("/gst/{gst_id}")
def delete_gst(
    gst_id : str,
    db : Session = Depends(get_db)
):
    db_gst = db.query(GST).filter(GST.gst_id == gst_id).first()

    if not db_gst:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="GST not found to delete"
        )
    
    db_gst.is_deleted = True

    db.commit()

    return{
        "status" : status.HTTP_200_OK,
        "message" : "GST deleted successfully",
        "gst" : db_gst.gst_id
    }


@gst_router.delete("/v3/gst/{gst_id}")
def delete_gst_v3(
    gst_id : str,
    db : Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if current_user["inventory_privileges"]["edit"] == False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "You don't have enoght permission to delete GST"
        )

    db_gst = db.query(GST).filter(GST.gst_id == gst_id).first()

    if not db_gst:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="GST not found to delete"
        )
    
    db_gst.is_deleted = True

    db.commit()

    return{
        "status" : status.HTTP_200_OK,
        "message" : "GST deleted successfully",
        "gst" : db_gst.gst_id
    }