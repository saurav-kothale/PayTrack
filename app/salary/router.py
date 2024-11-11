from re import S
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.exception_handlers import http_exception_handler
from sqlalchemy.orm import Session

from app.salary.model import SalaryClientModel
from app.salary.schema import SalaryClient, SalaryClientUpdate
from database.database import get_db
import uuid
from datetime import datetime

salary_client = APIRouter()

@salary_client.get("/")
def get_salary_clients(db : Session = Depends(get_db)):

    db_client = db.query(SalaryClientModel).filter(SalaryClientModel.is_deleted == False).all()

    if not db_client:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "No data found"
        )
    
    return{
        "status" : status.HTTP_200_OK,
        "message" : "record fetched successfully",
        "data" : db_client
    }

@salary_client.get("/client/{client_id}")
def get_salary_client(
    client_id : str,
    db : Session = Depends(get_db)
):
    
    db_client = db.query(SalaryClientModel).filter(SalaryClientModel.client_id == client_id).first()

    if not db_client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="client not found"
        )
    
    return{
        "status" : status.HTTP_200_OK,
        "message" : "record Fetched successfully",
        "data" : db_client
    }


@salary_client.post("/client")
def create_salary_client(
    schema : SalaryClient,
    db : Session = Depends(get_db)
):
    
    db_client = db.query(SalaryClientModel).filter(SalaryClientModel.client_name == schema.client_name, SalaryClientModel.is_deleted == False).first()

    if db_client:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="client is already exist"
        )
    
    new_client = SalaryClientModel(
        client_id = str(uuid.uuid4()),
        client_name = schema.client_name,
        grid_slab = schema.grid_slab,
        rejection = schema.rejection,
        bad_order = schema.bad_order,
        perform_to = schema.perform_to,
        created_at = datetime.now(),
        updated_at = datetime.now()
    )

    db.add(new_client)

    db.commit
    
    return{        
        "status" : status.HTTP_201_CREATED,
        "message" : "client created successfully",
        "data" : new_client
    }


@salary_client.patch("/client/{client_id}")
def udpate_salary_client(
    client_id : str,
    schema : SalaryClientUpdate,
    db : Session = Depends(get_db)
):
    db_client = db.query(SalaryClientModel).filter(SalaryClientModel.client_id == client_id, SalaryClientModel.is_deleted == False).first()

    if not db_client:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="client not found to udpate"
        )
    
    db_client.client_name = schema.client_name
    db_client.grid_slab = schema.grid_slab
    db_client.rejection = schema.rejection
    db_client.bad_order = schema.bad_order
    db_client.perform_to = schema.perform_to
    db_client.updated_at = datetime.now()

    db.commit()

    client = {
        "client_id" : db_client.client_id,
        "client_name" : db_client.client_name,
        "rejection" : db_client.rejection,
        "bad_order" : db_client.bad_order,
        "perform_to" : db_client.perform_to,
        "created_at" : db_client.created_at,
        "updated_at" : db_client.updated_at,
        "is_deleted" : db_client.is_deleted
    }

    return{
        "status" : status.HTTP_202_ACCEPTED,
        "message" : "Client Updated successfully",
        "data" : client
    }


@salary_client.delete("/client/{client_id}")
def delete_salary_client(
    client_id : str,
    db : Session = Depends(get_db)
):
    
    db_client = db.query(SalaryClientModel).filter(SalaryClientModel.client_id == client_id, SalaryClientModel.is_deleted == False).first()

    if not db_client:
        
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="client salary not found to delete"
        )
    
    db_client.is_deleted = True

    db.commit()

    client = {
        "client_id" : db_client.client_id,
        "client_name" : db_client.client_name,
        "rejection" : db_client.rejection,
        "bad_order" : db_client.bad_order,
        "perform_to" : db_client.perform_to,
        "created_at" : db_client.created_at,
        "updated_at" : db_client.updated_at,
        "is_deleted" : db_client.is_deleted
    }

    return{
        "status" : status.HTTP_200_OK,
        "message" : "record deleted successfully",
        "data" : client
    }

 