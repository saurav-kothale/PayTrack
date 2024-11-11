from typing import List
from fastapi import APIRouter, HTTPException, status , Depends
from database.database import SessionLocal, get_db
from app.User.user.model.user import User, UserRecord
from app.User.user.schema.user import (
    ResetPasswordData,
    UserLoginData,
    UserLoginDataV2,
    UserRecordResponse,
    UserRecordSchema,
    UserSignupData,
    mobile_no_varification, mobile_no_varification_updated
)
from datetime import timedelta

from werkzeug.security import generate_password_hash , check_password_hash
from fastapi.encoders import jsonable_encoder
from uuid import uuid4
# from app.utils.util import signJWT, decodeJWT, get_current_user
from app.utils.util import create_access_token, get_current_user 

# from app.utils.auth_bearer import JWTBearer
from sqlalchemy.orm import Session
from decouple import config
from app import setting
from datetime import datetime

signup_router = APIRouter()
accesstoken_expire_time = setting.ACCESSTOKEN_EXPIRE_TIME


@signup_router.post("/signup" , status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserSignupData, db : Session = Depends(get_db)):

    db_entry = db.query(User).filter(User.username == user_data.username).first()

    if db_entry is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail = "User already exist."
        )
   
    db_entry = db.query(User).filter(User.email_id == user_data.email_id).first()

    if db_entry is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exist."
        )
    db_mobile_number = db.query(User).filter(User.mobile_no == user_data.mobile_no).first()

    if db_mobile_number:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mobile Number already exists"
        )


    if mobile_no_varification_updated(user_data.mobile_no) is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST , detail="Mobile Number is not valid.Make sure you provided Contry code as well"
        )    

    if user_data.password != user_data.retype_password:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail="retype password should be same as password",
        )

    user = User(
        first_name = user_data.first_name,
        last_name = user_data.last_name,
        username = user_data.username,
        user_id = uuid4(),
        email_id = user_data.email_id,
        mobile_no = user_data.mobile_no,
        password = generate_password_hash(user_data.password),
        retype_password = generate_password_hash(user_data.retype_password),
    )

    db.add(user)

    db.commit()

    return {"status": status.HTTP_200_OK, "message": "User created successfully"}


@signup_router.post("/v2/signup" , status_code=status.HTTP_201_CREATED)
def create_user_v2(user_data: UserRecordSchema, db : Session = Depends(get_db)):

    db_entry = db.query(UserRecord).filter(UserRecord.username == user_data.username).first()

    if db_entry is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail = "User already exist."
        )
       

    if user_data.password != user_data.retype_password:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail="retype password should be same as password",
        )

    user = UserRecord(
        user_id = uuid4(),
        username = user_data.username,
        password = generate_password_hash(user_data.password),
        retype_password = generate_password_hash(user_data.retype_password),
        is_admin = user_data.is_admin,
        inventory_privileges = user_data.inventory_privileges.model_dump(),
        salary_privileges = user_data.salary_privileges.model_dump(),
        is_deleted = False,
        created_at = datetime.now(),
        updated_at = datetime.now()
    )

    db.add(user)

    db.commit()

    return {"status": status.HTTP_200_OK, "message": "User created successfully"}


@signup_router.get("/v2/user")
def get_users(db : Session = Depends(get_db)):

    db_user = db.query(UserRecord).filter(UserRecord.is_deleted == False).all()

    if not db_user :
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Users not found"
        )
    
    user_response = [
        {
            "user_id" : user.user_id,
            "user_name" : user.username,
            "is_admin" : user.is_admin,
            "inventory_privilege" : user.inventory_privileges,
            "salary_privilege" : user.salary_privileges,
            "created_at" : user.created_at,
            "updated_at" : user.updated_at
        }
        
        for user in db_user
    ]

    return {
        "status" : status.HTTP_200_OK,
        "message" : "User fetched successfully",
        "user" : user_response
    }


@signup_router.patch("/v2/signup/{user_id}" , status_code=status.HTTP_201_CREATED)
def update_user_v2(user_id : str, user_data: UserRecordSchema, db : Session = Depends(get_db)):

    db_entry = db.query(UserRecord).filter(UserRecord.user_id == user_id).first()

    if not db_entry:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail = "User not found to update"
        )
       

    if user_data.password != user_data.retype_password:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail="retype password should be same as password",
        )
    
    
    db_entry.username = user_data.username
    db_entry.password = user_data.password
    db_entry.retype_password = user_data.retype_password
    db_entry.is_admin = user_data.is_admin
    db_entry.inventory_privileges = user_data.inventory_privileges.model_dump()
    db_entry.salary_privileges = user_data.salary_privileges.model_dump()

    db.commit()

    return {"status": status.HTTP_200_OK, "message": "User Updated successfully successfully"}


login_router = APIRouter()


@login_router.post("/login", status_code=status.HTTP_201_CREATED)
def log_in(user_data : UserLoginData, db : Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email_id == user_data.email_id).first()
    if db_user and check_password_hash(db_user.password , user_data.password): # type: ignore


        access_token_data = {
            "user_id" : db_user.user_id,
            "first_name" : db_user.first_name,
            "last_name" : db_user.last_name,
            "user_name" : db_user.username,
            "mobile_number" : db_user.mobile_no,
            "email_id" : db_user.email_id

        }

        access_token = create_access_token(access_token_data, int(accesstoken_expire_time))

        response = {
            "access" : access_token,
            "user_name" : db_user.username,
            "massage" : "User Login Successfully"
        }

        return jsonable_encoder(response)
    
    raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST , detail = "Invalid Username Or Password")


@login_router.post("/v2/login", status_code=status.HTTP_201_CREATED)
def log_in_v2(user_data : UserLoginDataV2, db : Session = Depends(get_db)):
    db_user = db.query(UserRecord).filter(UserRecord.username == user_data.username).first()
    if db_user and check_password_hash(db_user.password , user_data.password): # type: ignore


        access_token_data = {
            "user_id" : db_user.user_id,
            "user_name" : db_user.username,
            "is_admin" : db_user.is_admin,
            "inventory_privileges" : db_user.inventory_privileges,
            "salary_privileges" : db_user.inventory_privileges

        }

        access_token = create_access_token(access_token_data, int(accesstoken_expire_time))

        response = {
            "access" : access_token,
            "user_name" : db_user.username,
            "massage" : "User Login Successfully"
        }

        return jsonable_encoder(response)
    
    raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST , detail = "Invalid Username Or Password")

protected_router = APIRouter()


@protected_router.get("/protected") 
def protected (current_user : str = Depends(get_current_user)):
    return {"user" : current_user}



forgot_password_route = APIRouter()


@forgot_password_route.post("/forget_password", status_code = status.HTTP_201_CREATED)
def recover_password(user_data: ResetPasswordData, db : Session = Depends(get_db)):

    db_entry = db.query(User).filter(User.email_id == user_data.email_id).first()

    if db_entry is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST , detail="email not found"
        )

    return {
        "status" : status.HTTP_202_ACCEPTED,
        "message" : "Link has been sent to your registered Email_id or Mobile number",
    }


delete_route = APIRouter()


@delete_route.delete("/delete" , status_code=status.HTTP_200_OK)
def delete_user(user_data : UserLoginData, db : Session = Depends(get_db)):
    user_to_delete = db.query(User).filter(User.email_id == user_data.email_id).first()
     
    if user_to_delete and check_password_hash(user_to_delete.password, user_data.password): # type: ignore
        db.delete(user_to_delete)
        db.commit() 

        return {
            "data" : user_to_delete,
            "status" : 200,
            "message" : "User delete successfully"
            }

    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = "Invalid Username or Password"
    )


@delete_route.delete("/v3/delete/{user_id}" , status_code=status.HTTP_200_OK)
def delete_user_v3(user_id : str, db : Session = Depends(get_db)):

    user_to_delete = db.query(UserRecord).filter(UserRecord.user_id == user_id, UserRecord.is_deleted == False).first()
     
    if not user_to_delete:

        raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = "User not found to delete"
    )

        
    user_to_delete.is_deleted = True

    db.commit()

    return {
        "data" : user_to_delete,
        "status" : 200,
        "message" : "User delete successfully"
        }







