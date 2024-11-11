from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from datetime import datetime
from app.Inventory_in.color_category.model import ColorDb
from app.Inventory_in.color_category.schema import ColorCategorySchema, ColorUpdateSchema
from app.utils.util import get_current_user
from database.database import get_db
import uuid
from sqlalchemy.sql.expression import func
from app.Inventory_in.master_product.view import EPCCodeGenerator

color_router = APIRouter()

@color_router.get("/colors")
def get_color(db : Session = Depends(get_db)):
    
    db_color = db.query(ColorDb).filter(ColorDb.is_deleted == False).all()

    if not db_color:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="content not found"
        )
    
    return{
        "status" : status.HTTP_200_OK,
        "message" : "Records Fetched Sucessfully",
        "colors" : db_color
    }


@color_router.get("/v3/colors")
def get_color(
    db : Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if current_user["inventory_privileges"]["read"] == False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "You don't have enoght permission to read colors"
        )

    db_color = db.query(ColorDb).filter(ColorDb.is_deleted == False).all()

    if not db_color:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="content not found"
        )
    
    return{
        "status" : status.HTTP_200_OK,
        "message" : "Records Fetched Sucessfully",
        "colors" : db_color
    }


@color_router.get("/colors/{color_id}")
def get_colors(color_id : str, db : Session = Depends(get_db)):
    
    db_color = db.query(ColorDb).filter(ColorDb.color_id == color_id, ColorDb.is_deleted == False).first()

    if db_color is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="record not found"
        )
    
    return{
        "status" : status.HTTP_200_OK,
        "message" : "Record Fetched Sucessfully",
        "colors" : db_color
    }


@color_router.post("/colors")
def create_color(
    schema : ColorCategorySchema,
    db : Session = Depends(get_db)
):
    db_color = db.query(ColorDb).filter(func.lower(ColorDb.color_name) == func.lower(schema.color_name), ColorDb.is_deleted == False).first()

    if db_color:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="color name already exist"
        )
    
    code_generator = EPCCodeGenerator("color category", db=db)

    new_color = ColorDb(
        color_id = code_generator.generate_code("CC", 3),
        color_name = schema.color_name,
        created_at = datetime.now(),
        updated_at = datetime.now(),
        is_deleted = False
    )

    db.add(new_color)

    db.commit()

    color_dict = {
        "color_id" : new_color.color_id,
        "color_name" : new_color.color_name,
        "created_at" : new_color.created_at,
        "updated_at" : new_color.updated_at
    }

    return{
        "status" : status.HTTP_201_CREATED,
        "message" : "Color created sucessfully",
        "color" : color_dict
    }


@color_router.post("/v3/colors")
def create_color_v3(
    schema : ColorCategorySchema,
    db : Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    
    if current_user["inventory_privileges"]["edit"] == False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "You don't have enoght permission to create color"
        )
    
    db_color = db.query(ColorDb).filter(func.lower(ColorDb.color_name) == func.lower(schema.color_name), ColorDb.is_deleted == False).first()

    if db_color:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="color name already exist"
        )
    
    code_generator = EPCCodeGenerator("color category", db=db)

    new_color = ColorDb(
        color_id = code_generator.generate_code("CC", 3),
        color_name = schema.color_name,
        created_at = datetime.now(),
        updated_at = datetime.now(),
        is_deleted = False
    )

    db.add(new_color)

    db.commit()

    color_dict = {
        "color_id" : new_color.color_id,
        "color_name" : new_color.color_name,
        "created_at" : new_color.created_at,
        "updated_at" : new_color.updated_at
    }

    return{
        "status" : status.HTTP_201_CREATED,
        "message" : "Color created sucessfully",
        "color" : color_dict
    }


@color_router.patch("/colors/{color_id}")
def update_color(
    color_id : str,
    schema : ColorUpdateSchema,
    db : Session = Depends(get_db)
):
    db_color = db.query(ColorDb).filter(ColorDb.color_id == color_id).first()

    if db_color is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Color not found to update"
        )
    
    existing_city = db.query(ColorDb).filter(
        func.lower(ColorDb.color_name) == func.lower(schema.color_name),
        ColorDb.color_id != color_id
    ).first()

    if existing_city:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Color already exists"
        )
    
    db_color.color_name = schema.color_name
    db_color.updated_at = datetime.now()
    
    db.commit()

    return{
        "status" : status.HTTP_200_OK,
        "message" : "record Updated Successfully",
        "color" : {
            "color_id" : db_color.color_id,
            "color_name" : db_color.color_name,
            "updated_at" : db_color.updated_at,
            "created_at" : db_color.created_at
        }

    }


@color_router.patch("/v3/colors/{color_id}")
def update_color_v3(
    color_id : str,
    schema : ColorUpdateSchema,
    db : Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    
    if current_user["inventory_privileges"]["edit"] == False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "You don't have enoght permission to update color"
        )
    db_color = db.query(ColorDb).filter(ColorDb.color_id == color_id).first()

    if db_color is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Color not found to update"
        )
    
    existing_city = db.query(ColorDb).filter(
        func.lower(ColorDb.color_name) == func.lower(schema.color_name),
        ColorDb.color_id != color_id
    ).first()

    if existing_city:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Color already exists"
        )
    
    db_color.color_name = schema.color_name
    db_color.updated_at = datetime.now()
    
    db.commit()

    return{
        "status" : status.HTTP_200_OK,
        "message" : "record Updated Successfully",
        "color" : {
            "color_id" : db_color.color_id,
            "color_name" : db_color.color_name,
            "updated_at" : db_color.updated_at,
            "created_at" : db_color.created_at
        }

    }


@color_router.delete("/colors/{color_id}")
def delete_color(
    color_id : str,
    db : Session = Depends(get_db) 
):
    db_color = db.query(ColorDb).filter(ColorDb.color_id == color_id).first()

    if db_color is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Color not found to delete"
        )

    db_color.is_deleted = True

    db.commit()

    return{
        "status" : status.HTTP_200_OK,
        "message" : "Record deleted sucessfully",
        "color_id" : db_color.color_id
    }


@color_router.delete("v3/colors/{color_id}")
def delete_color_v3(
    color_id : str,
    db : Session = Depends(get_db),
    current_user = Depends(get_current_user) 
):
    
    if current_user["inventory_privileges"]["edit"] == False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "You don't have enoght permission to delete color"
        )

    db_color = db.query(ColorDb).filter(ColorDb.color_id == color_id).first()

    if db_color is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Color not found to delete"
        )

    db_color.is_deleted = True

    db.commit()

    return{
        "status" : status.HTTP_200_OK,
        "message" : "Record deleted sucessfully",
        "color_id" : db_color.color_id
    }