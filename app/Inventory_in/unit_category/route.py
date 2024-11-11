from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.Inventory_in.unit_category.model import Unit
from app.Inventory_in.unit_category.schema import UnitSchema, UnitUpdateSchema
from database.database import get_db
import uuid
from datetime import datetime
from app.Inventory_in.master_product.view import EPCCodeGenerator

unit_router = APIRouter()

@unit_router.get('/units')
def get_units(db : Session = Depends(get_db)):
    
    db_units = db.query(Unit).filter(Unit.is_deleted == False).all()

    if not db_units:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="Units not found"
        )
    
    return {
        "status" : status.HTTP_200_OK,
        "message" : "Units fetched successfully",
        "units" : db_units
    }


@unit_router.get("/units/{unit_id}")
def get_unit(
    unit_id : str,
    db : Session = Depends(get_db)
):
    db_unit = db.query(Unit).filter(Unit.unit_id == unit_id, Unit.is_deleted == False).first()

    if not db_unit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="unit not found"
        )
    
    return {
        "status" : status.HTTP_200_OK,
        "message" : "unit fetched successfully",
        "unit" : db_unit
    }


@unit_router.post("/units")
def create_unit(
    schema : UnitSchema,
    db : Session = Depends(get_db)
):
    
    db_unit = db.query(Unit).filter(Unit.unit_name == schema.unit_name, Unit.is_deleted == False).first()

    if db_unit:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unit name already exist"
        )
    
    code_generator = EPCCodeGenerator("unit category", db=db)
    
    new_unit = Unit(
        unit_id = code_generator.generate_code("UC", 3),
        unit_name = schema.unit_name,
        created_at = datetime.now(),
        updated_at = datetime.now(),
        is_deleted = False
    )

    db.add(new_unit)

    db.commit()

    unit = {
        "unit_id" : new_unit.unit_id,
        "unit_name" : new_unit.unit_name,
        "created_at" : new_unit.created_at,
        "updated_at" : new_unit.updated_at
    }

    return{
        "status" : status.HTTP_201_CREATED,
        "message" : "Unit created successfully",
        "unit" : unit
    }


@unit_router.patch("/units/{unit_id}")
def update_unit(
    unit_id : str,
    schema : UnitUpdateSchema,
    db : Session = Depends(get_db)
):
    
    db_unit = db.query(Unit).filter(Unit.unit_id == unit_id).first()

    if not db_unit:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "Unit not found to update"
        )
    
    db_unit.unit_name = schema.unit_name
    db_unit.updated_at = datetime.now()

    db.commit()

    unit = {
        "unit_id" : db_unit.unit_id,
        "unit_name" : db_unit.unit_name,
        "created_at" : db_unit.created_at,
        "updated_at" : db_unit.updated_at
    }

    return{
        "status" : status.HTTP_200_OK,
        "message" : "unit updated succesfully",
        "unit" : unit
    }


@unit_router.delete("/unit/{unit_id}")
def delete_unit(
    unit_id : str,
    db : Session = Depends(get_db)
):
    db_unit = db.query(Unit).filter(Unit.unit_id == unit_id).first()

    if not db_unit:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unit not found to delete"
        )
    
    db_unit.is_deleted = True

    db.commit()

    return{
        "status" : status.HTTP_200_OK,
        "message" : "Unit deleted successfully",
        "unit" : db_unit.unit_id
    }