from fastapi import APIRouter, Depends, HTTPException,status
from numpy import size
from sqlalchemy.orm import Session
from datetime import datetime
from app.Inventory_in.size_category.model import SizeDb
from app.Inventory_in.size_category.schema import SizeCategorySchema, SizeUpdateSchema
from app.utils.util import get_current_user
from database.database import get_db
import uuid
from sqlalchemy.sql.expression import func
from app.Inventory_in.master_product.view import EPCCodeGenerator


size_router = APIRouter()


@size_router.get("/sizes")
def get_sizes(db : Session = Depends(get_db)):
    
    db_size = db.query(SizeDb).filter(SizeDb.is_deleted == False).all()

    if not db_size:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="content not found"
        )
    
    return{
        "status" : status.HTTP_200_OK,
        "message" : "Records Fetched Sucessfully",
        "size" : db_size
    }


@size_router.get("/v3/sizes")
def get_sizes_v3(db : Session = Depends(get_db), current_user = Depends(get_current_user)):
    
    if current_user["inventory_privileges"]["read"] == False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "You don't have enoght permission to read sizes"
        )

    db_size = db.query(SizeDb).filter(SizeDb.is_deleted == False).all()

    if not db_size:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="content not found"
        )
    
    return{
        "status" : status.HTTP_200_OK,
        "message" : "Records Fetched Sucessfully",
        "size" : db_size
    }

 
@size_router.get("/sizes/{size_id}")
def get_size(size_id : str, db : Session = Depends(get_db)):
    
    db_size = db.query(SizeDb).filter(SizeDb.size_id == size_id, SizeDb.is_deleted == False).first()

    if db_size is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="record not found"
        )
    
    return{
        "status" : status.HTTP_200_OK,
        "message" : "Record Fetched Sucessfully",
        "colors" : db_size
    }


@size_router.post("/sizes")
def create_size(
    schema : SizeCategorySchema,
    db : Session = Depends(get_db)
):
    db_size = db.query(SizeDb).filter(func.lower(SizeDb.size_name) == func.lower(schema.size_name), SizeDb.is_deleted == False).first()

    if db_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="size name already exist"
        )
    
    code_generator = EPCCodeGenerator("size category", db=db)

    new_size = SizeDb(
        size_id = code_generator.generate_code("SC", 3),
        size_name = schema.size_name,
        created_at = datetime.now(),
        updated_at = datetime.now(),
        is_deleted = False
    )

    db.add(new_size)

    db.commit()

    size = {
       "size_id" : new_size.size_id,
       "size_name" : new_size.size_name,
       "created_at" : new_size.created_at,
       "updated_at" : new_size.updated_at
    }

    return{
        "status" : status.HTTP_201_CREATED,
        "message" : "size created sucessfully",
        "size" : size
    }


@size_router.post("/v3/sizes")
def create_size_v3(
    schema : SizeCategorySchema,
    db : Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if current_user["inventory_privileges"]["edit"] == False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "You don't have enoght permission to create size"
        )

    db_size = db.query(SizeDb).filter(func.lower(SizeDb.size_name) == func.lower(schema.size_name), SizeDb.is_deleted == False).first()

    if db_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="size name already exist"
        )
    
    code_generator = EPCCodeGenerator("size category", db=db)

    new_size = SizeDb(
        size_id = code_generator.generate_code("SC", 3),
        size_name = schema.size_name,
        created_at = datetime.now(),
        updated_at = datetime.now(),
        is_deleted = False
    )

    db.add(new_size)

    db.commit()

    size = {
       "size_id" : new_size.size_id,
       "size_name" : new_size.size_name,
       "created_at" : new_size.created_at,
       "updated_at" : new_size.updated_at
    }

    return{
        "status" : status.HTTP_201_CREATED,
        "message" : "size created sucessfully",
        "size" : size
    }

@size_router.patch("/sizes/{size_id}")
def update_size(
    size_id : str,
    schema : SizeUpdateSchema,
    db : Session = Depends(get_db)
):
    db_size = db.query(SizeDb).filter(SizeDb.size_id == size_id).first()

    if db_size is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Size not found to update"
        )
    
    existing_size = db.query(SizeDb).filter(
        func.lower(SizeDb.size_name) == func.lower(schema.size_name),
        SizeDb.size_id != size_id
    ).first()
    
    if existing_size:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Size is already exist"
        )
    
    db_size.size_name = schema.size_name
    db_size.updated_at = datetime.now()
    
    db.commit()

    updated_size = {
        "size_id" : db_size.size_id,
        "size_name" : db_size.size_name,
        "created_at" : db_size.created_at,
        "updated_at" : db_size.updated_at
    }

    return{
        "status" : status.HTTP_200_OK,
        "message" : "record Updated Successfully",
        "size" : updated_size
    }


@size_router.patch("/v3/sizes/{size_id}")
def update_size_v3(
    size_id : str,
    schema : SizeUpdateSchema,
    db : Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if current_user["inventory_privileges"]["edit"] == False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "You don't have enoght permission to update size"
        )

    db_size = db.query(SizeDb).filter(SizeDb.size_id == size_id).first()

    if db_size is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Size not found to update"
        )
    
    existing_size = db.query(SizeDb).filter(
        func.lower(SizeDb.size_name) == func.lower(schema.size_name),
        SizeDb.size_id != size_id
    ).first()
    
    if existing_size:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Size is already exist"
        )
    
    db_size.size_name = schema.size_name
    db_size.updated_at = datetime.now()
    
    db.commit()

    updated_size = {
        "size_id" : db_size.size_id,
        "size_name" : db_size.size_name,
        "created_at" : db_size.created_at,
        "updated_at" : db_size.updated_at
    }

    return{
        "status" : status.HTTP_200_OK,
        "message" : "record Updated Successfully",
        "size" : updated_size
    }

@size_router.delete("/sizes/{size_id}")
def delete_size(
    size_id : str,
    db : Session = Depends(get_db) 
):
    db_size = db.query(SizeDb).filter(SizeDb.size_id == size_id).first()

    if db_size is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Size not found to delete"
        )

    db_size.is_deleted = True

    db.commit()

    return{
        "status" : status.HTTP_200_OK,
        "message" : "Record deleted sucessfully",
        "size_id" : db_size.size_id
    }


@size_router.delete("/v3/sizes/{size_id}")
def delete_size_v3(
    size_id : str,
    db : Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    
    if current_user["inventory_privileges"]["edit"] == False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "You don't have enoght permission to delete size"
        )

    db_size = db.query(SizeDb).filter(SizeDb.size_id == size_id).first()

    if db_size is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Size not found to delete"
        )

    db_size.is_deleted = True

    db.commit()

    return{
        "status" : status.HTTP_200_OK,
        "message" : "Record deleted sucessfully",
        "size_id" : db_size.size_id
    }