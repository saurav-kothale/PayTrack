from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from datetime import datetime
from app.Inventory_in.city_category.model import CityDb
from app.Inventory_in.city_category.schema import CityCategorySchema, CityUpdateSchema
from app.utils.util import get_current_user
from database.database import get_db
import uuid
from sqlalchemy.sql.expression import func
from app.Inventory_in.master_product.view import EPCCodeGenerator

city_router = APIRouter()


@city_router.get("/cities")
def get_cities(db : Session = Depends(get_db)):
    
    db_city = db.query(CityDb).filter(CityDb.is_deleted == False).all()

    if not db_city:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="content not found"
        )
    
    return{
        "status" : status.HTTP_200_OK,
        "message" : "Records Fetched Sucessfully",
        "cities" : db_city
    }

@city_router.get("/v3/cities")
def get_cities_v3(
    db : Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    
    if current_user["inventory_privileges"]["read"] == False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "You don't have enoght permission to see cities"
        )

    db_city = db.query(CityDb).filter(CityDb.is_deleted == False).all()

    if not db_city:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="content not found"
        )
    
    return{
        "status" : status.HTTP_200_OK,
        "message" : "Records Fetched Sucessfully",
        "cities" : db_city
    }


@city_router.get("/cities/{city_id}")
def get_city(city_id : str, db : Session = Depends(get_db)):
    
    db_city = db.query(CityDb).filter(CityDb.city_id == city_id, CityDb.is_deleted == False).first()

    if db_city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="record not found"
        )
    
    return{
        "status" : status.HTTP_200_OK,
        "message" : "Record Fetched Sucessfully",
        "cities" : db_city
    }


@city_router.post("/cities")
def create_city(
    schema : CityCategorySchema,
    db : Session = Depends(get_db)
):
    db_city = db.query(CityDb).filter(func.lower(CityDb.city_name) == func.lower(schema.city_name), CityDb.is_deleted == False).first()

    if db_city:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="City name already exist"
        )
    
    code_generator = EPCCodeGenerator("city category", db=db)    
    
    new_city = CityDb(
        city_id = code_generator.generate_code("CT", 3),
        city_name = schema.city_name,
        created_at = datetime.now(),
        updated_at = datetime.now(),
        is_deleted = False
    )

    db.add(new_city)

    db.commit()

    return{
        "status" : status.HTTP_201_CREATED,
        "message" : "City created sucessfully",
        "city" : {
            "city_id" : new_city.city_id,
            "city_name" : new_city.city_name,
            "created_at" : new_city.created_at,
            "updated_at" : new_city.updated_at,
            "is_deleted" : new_city.is_deleted
        }
    }


@city_router.post("/v3/cities")
def create_city_v3(
    schema : CityCategorySchema,
    db : Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    
    if current_user["inventory_privileges"]["edit"] == False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "You don't have enoght permission to create cities"
        )

    db_city = db.query(CityDb).filter(func.lower(CityDb.city_name) == func.lower(schema.city_name), CityDb.is_deleted == False).first()

    if db_city:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="City name already exist"
        )
    
    code_generator = EPCCodeGenerator("city category", db=db)    
    
    new_city = CityDb(
        city_id = code_generator.generate_code("CT", 3),
        city_name = schema.city_name,
        created_at = datetime.now(),
        updated_at = datetime.now(),
        is_deleted = False
    )

    db.add(new_city)

    db.commit()

    return{
        "status" : status.HTTP_201_CREATED,
        "message" : "City created sucessfully",
        "city" : {
            "city_id" : new_city.city_id,
            "city_name" : new_city.city_name,
            "created_at" : new_city.created_at,
            "updated_at" : new_city.updated_at,
            "is_deleted" : new_city.is_deleted
        }
    }


@city_router.patch("/cities/{city_id}")
def update_city(
    city_id : str,
    schema : CityUpdateSchema,
    db : Session = Depends(get_db)
):
    db_city = db.query(CityDb).filter(CityDb.city_id == city_id).first()

    if db_city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found to update"
        )
    
    existing_city = db.query(CityDb).filter(
        func.lower(CityDb.city_name) == func.lower(schema.city_name),
        CityDb.city_id != city_id
    ).first()

    if existing_city:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="City already exists"
        )
    
    
    db_city.city_name = schema.city_name
    db_city.updated_at = datetime.now()
    
    db.commit()

    return{
        "status" : status.HTTP_200_OK,
        "message" : "record Updated Successfully",
        "city" : {
            "city_id" : db_city.city_id,
            "city_name" : db_city.city_name,
            "updated_at" : db_city.updated_at,
            "created_at" : db_city.created_at
        }
    }


@city_router.patch("/v3/cities/{city_id}")
def update_city_v3(
    city_id : str,
    schema : CityUpdateSchema,
    db : Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    
    if current_user["inventory_privileges"]["edit"] == False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "You don't have enoght permission to update city"
        )

    db_city = db.query(CityDb).filter(CityDb.city_id == city_id).first()

    if db_city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found to update"
        )
    
    existing_city = db.query(CityDb).filter(
        func.lower(CityDb.city_name) == func.lower(schema.city_name),
        CityDb.city_id != city_id
    ).first()

    if existing_city:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="City already exists"
        )
    
    
    db_city.city_name = schema.city_name
    db_city.updated_at = datetime.now()
    
    db.commit()

    return{
        "status" : status.HTTP_200_OK,
        "message" : "record Updated Successfully",
        "city" : {
            "city_id" : db_city.city_id,
            "city_name" : db_city.city_name,
            "updated_at" : db_city.updated_at,
            "created_at" : db_city.created_at
        }
    }


@city_router.delete("/cities/{city_id}")
def delete_city(
    city_id : str,
    db : Session = Depends(get_db) 
):
    db_city = db.query(CityDb).filter(CityDb.city_id == city_id).first()

    if db_city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found to delete"
        )

    db_city.is_deleted = True

    db.commit()

    return{
        "status" : status.HTTP_200_OK,
        "message" : "Record deleted sucessfully",
        "city_id" : db_city.city_id
    }


@city_router.delete("/v3/cities/{city_id}")
def delete_city_v3(
    city_id : str,
    db : Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    
    if current_user["inventory_privileges"]["edit"] == False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "You don't have enoght permission to delete city"
        )

    db_city = db.query(CityDb).filter(CityDb.city_id == city_id).first()

    if db_city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found to delete"
        )

    db_city.is_deleted = True

    db.commit()

    return{
        "status" : status.HTTP_200_OK,
        "message" : "Record deleted sucessfully",
        "city_id" : db_city.city_id
    }