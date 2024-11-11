from curses.ascii import HT
from email.policy import HTTP
from itertools import product
from fastapi import APIRouter, Depends, HTTPException, status
from numpy import size
from app.Inventory_in.master_product.schema import ProductCategorySchema, ProductCategorySchemaV2
from app.Inventory_in.master_product.model import ProductCategoryDB, MasterProductDB
from sqlalchemy.orm import Session
from app.Inventory_in.master_product.view import generate_epc_code
from app.product.model.model import InvoiceProductsDB
from app.utils.util import get_current_user
from database.database import get_db
import uuid
from sqlalchemy.sql.expression import func
import json
from app.Inventory_in.master_product.view import EPCCodeGenerator
from app.Inventory_in.bike_category.model import BikeDb

product_cateogry_router = APIRouter()

@product_cateogry_router.post("/product_category/category")
def create_product(
    schema : ProductCategorySchema,
    db : Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    
    db_product = db.query(MasterProductDB).filter(func.lower(MasterProductDB.product_name) == func.lower(schema.product_name)).all()

    for product in db_product:
        if set(product.bike_category) == set(schema.bike_category):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product with the same name and bike category already exists"
            )
        
    code_generator = EPCCodeGenerator("EPC code", db=db)

    new_product = MasterProductDB(
        product_name = schema.product_name,
        EPC_code = code_generator.generate_code("EPC", 6),
        HSN_code = schema.hsn_code,
        category = schema.category,
        bike_category = schema.bike_category,
        size = schema.size,
        color = schema.color,
        unit = schema.unit,
        gst = schema.gst,
        user = current_user

    )


    db.add(new_product)

    db.commit()

    return{
        "status" : status.HTTP_201_CREATED,
        "message" : "Product category created successfully",
        "product" : new_product
    }

@product_cateogry_router.post("/v2/product_category/category")
def create_product_v2(
    schema : ProductCategorySchemaV2,
    db : Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    
    db_product = db.query(MasterProductDB).filter(func.lower(MasterProductDB.product_name) == func.lower(schema.product_name), MasterProductDB.is_deleted == False).all()

    for product in db_product:

        if (set(product.bike_category) == set(schema.bike_category) and
        product.HSN_code == schema.hsn_code and 
        product.category == schema.category and
        product.size == schema.size and
        product.color == schema.color):

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product is already exists"
            )
        
    code_generator = EPCCodeGenerator("EPC code", db=db)

    new_product = MasterProductDB(
        product_name = schema.product_name,
        EPC_code = code_generator.generate_code("EPC", 6),
        HSN_code = schema.hsn_code,
        category = schema.category,
        bike_category = schema.bike_category,
        size = schema.size,
        color = schema.color,
        unit = schema.unit,
        gst = schema.gst,
        user = current_user

    )


    db.add(new_product)


    db.commit()

    bikes = db.query(BikeDb).filter(BikeDb.bike_id.in_(schema.bike_category)).all()

    return{
        "status" : status.HTTP_201_CREATED,
        "message" : "Product category created successfully",
        "product_category" : {
            "EPC_code" : new_product.EPC_code,
            "product_name" : new_product.product_name,
            "category" : new_product.category_relation.category_name,
            "HSN_code" : new_product.HSN_code,
            "bike_category" : [bike.bike_name for bike in bikes],
            "size" : new_product.size_relation.size_name,
            "color" : new_product.color_relation.color_name,
            "unit" : new_product.unit_relation.unit_name,
            "gst" : new_product.gst_relation.gst_percentage,
            "created_at" : new_product.created_at,
            "updated_at" : new_product.updated_at,
            "user" : new_product.user

        }
    }


@product_cateogry_router.post("/v3/product_category/category")
def create_product_v3(
    schema : ProductCategorySchemaV2,
    db : Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    
    if current_user["inventory_privileges"]["edit"] == False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "You don't have enoght permission to create master products"
        )

    db_product = db.query(MasterProductDB).filter(func.lower(MasterProductDB.product_name) == func.lower(schema.product_name), MasterProductDB.is_deleted == False).all()

    for product in db_product:

        if (set(product.bike_category) == set(schema.bike_category) and
        product.HSN_code == schema.hsn_code and 
        product.category == schema.category and
        product.size == schema.size and
        product.color == schema.color):

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product is already exists"
            )
        
    code_generator = EPCCodeGenerator("EPC code", db=db)

    new_product = MasterProductDB(
        product_name = schema.product_name,
        EPC_code = code_generator.generate_code("EPC", 6),
        HSN_code = schema.hsn_code,
        category = schema.category,
        bike_category = schema.bike_category,
        size = schema.size,
        color = schema.color,
        unit = schema.unit,
        gst = schema.gst,
        user = current_user

    )


    db.add(new_product)


    db.commit()

    bikes = db.query(BikeDb).filter(BikeDb.bike_id.in_(schema.bike_category)).all()

    return{
        "status" : status.HTTP_201_CREATED,
        "message" : "Product category created successfully",
        "product_category" : {
            "EPC_code" : new_product.EPC_code,
            "product_name" : new_product.product_name,
            "category" : new_product.category_relation.category_name,
            "HSN_code" : new_product.HSN_code,
            "bike_category" : [bike.bike_name for bike in bikes],
            "size" : new_product.size_relation.size_name,
            "color" : new_product.color_relation.color_name,
            "unit" : new_product.unit_relation.unit_name,
            "gst" : new_product.gst_relation.gst_percentage,
            "created_at" : new_product.created_at,
            "updated_at" : new_product.updated_at,
            "user" : new_product.user

        }
    }
        

@product_cateogry_router.get("/get/product_category")
def get_products(
    db : Session = Depends(get_db)
):
    
    db_products = db.query(MasterProductDB).filter(MasterProductDB.is_deleted == False).all()

    if not db_products:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="Product not found"
        )
    
    return{
        "status" : status.HTTP_200_OK,
        "message" : "product categories fetched successfully",
        "products" : db_products
    }

@product_cateogry_router.get("/v2/get/product_category")
def get_products_v2(
    db : Session = Depends(get_db)
):
    
    db_products = db.query(MasterProductDB).filter(MasterProductDB.is_deleted == False).all()

    if not db_products:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="Product not found"
        )
    
    product_list = []
    for product in db_products:
        print(product)

        bikes = db.query(BikeDb).filter(BikeDb.bike_id.in_(product.bike_category)).all()
        final_product = {
        "EPC_code" : product.EPC_code,
        "product_name" : product.product_name,
        "category" : product.category_relation.category_name,
        "category_id" : product.category,
        "HSN_code" : product.HSN_code,
        "bike_category" : [bike.bike_name for bike in bikes],
        "bike_id" : product.bike_category,
        "size" : product.size_relation.size_name,
        "size_id" : product.size,
        "color" : product.color_relation.color_name,
        "color_id" : product.color,
        "unit" : product.unit_relation.unit_name,
        "unit_id" : product.unit,
        "gst" : product.gst_relation.gst_percentage,
        "gst_id" : product.gst,
        "created_at" : product.created_at,
        "updated_at" : product.updated_at
        }

        product_list.append(final_product)

    return{
        "status" : status.HTTP_200_OK,
        "message" : "product categories fetched successfully",
        "products" : product_list
    }

@product_cateogry_router.get("/v3/get/product_category")
def get_products_v3(
    db : Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    

    if current_user["inventory_privileges"]["view"] == False:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="you don't have enough permission to see this data"
        )
    
    
    db_products = db.query(MasterProductDB).filter(MasterProductDB.is_deleted == False).all()

    if not db_products:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="Product not found"
        )
    
    product_list = []
    for product in db_products:
        print(product)

        bikes = db.query(BikeDb).filter(BikeDb.bike_id.in_(product.bike_category)).all()
        final_product = {
        "EPC_code" : product.EPC_code,
        "product_name" : product.product_name,
        "category" : product.category_relation.category_name,
        "category_id" : product.category,
        "HSN_code" : product.HSN_code,
        "bike_category" : [bike.bike_name for bike in bikes],
        "bike_id" : product.bike_category,
        "size" : product.size_relation.size_name,
        "size_id" : product.size,
        "color" : product.color_relation.color_name,
        "color_id" : product.color,
        "unit" : product.unit_relation.unit_name,
        "unit_id" : product.unit,
        "gst" : product.gst_relation.gst_percentage,
        "gst_id" : product.gst,
        "created_at" : product.created_at,
        "updated_at" : product.updated_at
        }

        product_list.append(final_product)

    return{
        "status" : status.HTTP_200_OK,
        "message" : "product categories fetched successfully",
        "products" : product_list
    }

@product_cateogry_router.get("/get/product_category/id/{epc_code}")
def get_product_by_id(
    epc_code : str,
    db : Session = Depends(get_db)
):
    
    db_product = db.query(MasterProductDB).filter(MasterProductDB.EPC_code == epc_code).first()

    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="Product not found"
        )
    
    
    return{
        "status" : status.HTTP_200_OK,
        "message" : "product category fetched successfully",
        "products" : db_product
    }


@product_cateogry_router.get("/get/product_category/{hsn_code}")
def get_product(
    hsn_code : str,
    db : Session = Depends(get_db)
):
    
    db_product = db.query(MasterProductDB).filter(MasterProductDB.HSN_code == hsn_code, MasterProductDB.is_deleted == False).all()


    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="Product not found"
        )
        
    return{
        "status" : status.HTTP_200_OK,
        "message" : "product category fetched successfully",
        "products" : db_product
    }

@product_cateogry_router.get("/v2/get/product_category/{hsn_code}")
def get_product_v2(
    hsn_code : str,
    db : Session = Depends(get_db)
):
    
    db_product = db.query(MasterProductDB).filter(MasterProductDB.HSN_code == hsn_code, MasterProductDB.is_deleted == False).all()
     
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="Product not found"
        )
    
    products_with_category = []
    for product in db_product:
        bike_ids = product.bike_category
        bikes = db.query(BikeDb).filter(BikeDb.bike_id.in_(bike_ids)).all()

        bike_list = []
        for bike in bikes:
            bike_list.append(bike.bike_name)

        # bike_categories = [bike.bike_category_name for bike in product.bike_relationship]
        products_with_category.append({
            "EPC_code": product.EPC_code,
            "product_name": product.product_name,
            "HSN_code": product.HSN_code,
            "category": product.category_relation.category_name,  # Access the category name
            "bike_category": bike_list,
            "size": product.size_relation.size_name,
            "color": product.color_relation.color_name,
            "unit": product.unit_relation.unit_name,
            "gst": product.gst_relation.gst_percentage,
            "created_at": product.created_at,
            "updated_at": product.updated_at,
            "user": product.user
        })
        
    return{
        "status" : status.HTTP_200_OK,
        "message" : "product category fetched successfully",
        "products" : products_with_category
    }

    

# @product_cateogry_router.get("/get/product_category/epc_code/{epc_code}")
# def get_product_by_epc(
#     epc_code : str,
#     db : Session = Depends(get_db)
# ):
    
#     db_product = db.query(MasterProductDB).filter(MasterProductDB.EPC_code == epc_code).first()

#     if not db_product:v2
#         raise HTTPException(
#             status_code=status.HTTP_204_NO_CONTENT,
#             detail="Product not found"
#         )
    
#     return{
#         "status" : status.HTTP_200_OK,
#         "message" : "product category fetched successfully",
#         "products" : db_product
#     }


# @product_cateogry_router.patch("/get/product_category/{epc_code}")
# def update_product(
#     product_id : str,
#     schema : ProductCategorySchema,
#     db : Session = Depends(get_db)
# ):
    
#     db_product = db.query(MasterProductDB).filter(MasterProductDB.EPC_code == product_id).first()

#     if not db_product:
#         raise HTTPException(
#             status_code=status.HTTP_204_NO_CONTENT,
#             detail="Product not found"
#         )
    
#     existing_product_with_product_name = db.query(MasterProductDB).filter(func.lower(MasterProductDB.product_name) == func.lower(schema.product_name)).filter(MasterProductDB.product_id != product_id).first()

#     if existing_product_with_product_name:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Product Name is already present"
#         )
    
    
#     db_product.product_name = schema.product_name
#     db_product.HSN_code = schema.hsn_code
#     db_product.category = schema.category
#     db_product.bike_category = schema.bike_category
#     db_product.size = schema.size
#     db_product.color = schema.color
#     db_product.unit = schema.unit
#     db_product.gst = schema.gst

#     db.commit()

#     return{
#         "status" : status.HTTP_200_OK,
#         "message" : "product category updated successfully",
#         "products" : {
#             "product_id" : db_product.product_id,
#             "product_name" : db_product.product_name,
#             "hsn_code" : db_product.HSN_code,
#             "category" : db_product.category,
#             "bike_category" : db_product.bike_category,
#             "size" : db_product.size,
#             "color" : db_product.color,
#             "unit" : db_product.unit,
#             "gst" : db_product.gst,
#             "created_at" : db_product.created_at,
#             "updated_at" : db_product.updated_at
#         }
#     }


@product_cateogry_router.patch("/get/product_category/epc/{epc_code}")
def update_product_by_epc(
    epc_code : str,
    schema : ProductCategorySchema,
    db : Session = Depends(get_db)
):
    
    db_product = db.query(MasterProductDB).filter(MasterProductDB.EPC_code == epc_code).first()

    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="Product not found"
        )
    
    existing_product_with_product_name = db.query(MasterProductDB).filter(func.lower(MasterProductDB.product_name) == func.lower(schema.product_name)).all()

    for product in existing_product_with_product_name:
        if set(product.bike_category) == set(schema.bike_category):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This product already exist"
            )

    # if existing_product_with_product_name:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Product Name is already present"
    #     )
    
    
    db_product.product_name = schema.product_name
    db_product.HSN_code = schema.hsn_code
    db_product.category = schema.category
    db_product.bike_category = schema.bike_category
    db_product.size = schema.size
    db_product.color = schema.color
    db_product.unit = schema.unit
    db_product.gst = schema.gst

    db.commit()

    return{
        "status" : status.HTTP_200_OK,
        "message" : "product category updated successfully",
        "products" : {
            "EPC_code" : db_product.EPC_code,
            "product_name" : db_product.product_name,
            "HSN_code" : db_product.HSN_code,
            "category" : db_product.category,
            "bike_category" : db_product.bike_category,
            "size" : db_product.size,
            "color" : db_product.color,
            "unit" : db_product.unit,
            "gst" : db_product.gst,
            "created_at" : db_product.created_at,
            "updated_at" : db_product.updated_at
        }
    }


@product_cateogry_router.patch("/v2/get/product_category/epc/{epc_code}")
def update_product_by_epc_v2(
    epc_code : str,
    schema : ProductCategorySchema,
    db : Session = Depends(get_db)
):
    
    db_product = db.query(MasterProductDB).filter(MasterProductDB.EPC_code == epc_code).first()

    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="Product not found"
        )
    
    # existing_product_with_product_name = db.query(MasterProductDB).filter(func.lower(MasterProductDB.product_name) == func.lower(schema.product_name)).all()

    # for product in existing_product_with_product_name:
    #     if set(product.bike_category) == set(schema.bike_category):
    #         raise HTTPException(
    #             status_code=status.HTTP_400_BAD_REQUEST,
    #             detail="This product already exist"
    #         )

    # if existing_product_with_product_name:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Product Name is already present"
    #     )
    
    
    db_product.product_name = schema.product_name
    db_product.HSN_code = schema.hsn_code
    db_product.category = schema.category
    db_product.bike_category = schema.bike_category
    db_product.size = schema.size
    db_product.color = schema.color
    db_product.unit = schema.unit
    db_product.gst = schema.gst

    db.commit()

    bikes = db.query(BikeDb).filter(BikeDb.bike_id.in_(schema.bike_category)).all()

    return{
        "status" : status.HTTP_200_OK,
        "message" : "product category updated successfully",
        "products" : {
            "EPC_code" : db_product.EPC_code,
            "product_name" : db_product.product_name,
            "HSN_code" : db_product.HSN_code,
            "category" : db_product.category_relation.category_name,
            "bike_category" : [bike.bike_name for bike in bikes],
            "size" : db_product.size_relation.size_name,
            "color" : db_product.color_relation.color_name,
            "unit" : db_product.unit_relation.unit_name,
            "gst" : db_product.gst_relation.gst_percentage,
            "created_at" : db_product.created_at,
            "updated_at" : db_product.updated_at
        }
    }


@product_cateogry_router.patch("/v3/get/product_category/epc/{epc_code}")
def update_product_by_epc_v3(
    epc_code : str,
    schema : ProductCategorySchema,
    db : Session = Depends(get_db),
    current_user = Depends(get_current_user)
    ):

    if current_user["inventory_privileges"]["edit"] == False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "you don't have enough permission to update the master product"
        )
    
    db_product = db.query(MasterProductDB).filter(MasterProductDB.EPC_code == epc_code).first()

    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="Product not found"
        )
    
    # existing_product_with_product_name = db.query(MasterProductDB).filter(func.lower(MasterProductDB.product_name) == func.lower(schema.product_name)).all()

    # for product in existing_product_with_product_name:
    #     if set(product.bike_category) == set(schema.bike_category):
    #         raise HTTPException(
    #             status_code=status.HTTP_400_BAD_REQUEST,
    #             detail="This product already exist"
    #         )

    # if existing_product_with_product_name:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Product Name is already present"
    #     )
    
    
    db_product.product_name = schema.product_name
    db_product.HSN_code = schema.hsn_code
    db_product.category = schema.category
    db_product.bike_category = schema.bike_category
    db_product.size = schema.size
    db_product.color = schema.color
    db_product.unit = schema.unit
    db_product.gst = schema.gst

    db.commit()

    bikes = db.query(BikeDb).filter(BikeDb.bike_id.in_(schema.bike_category)).all()

    return{
        "status" : status.HTTP_200_OK,
        "message" : "product category updated successfully",
        "products" : {
            "EPC_code" : db_product.EPC_code,
            "product_name" : db_product.product_name,
            "HSN_code" : db_product.HSN_code,
            "category" : db_product.category_relation.category_name,
            "bike_category" : [bike.bike_name for bike in bikes],
            "size" : db_product.size_relation.size_name,
            "color" : db_product.color_relation.color_name,
            "unit" : db_product.unit_relation.unit_name,
            "gst" : db_product.gst_relation.gst_percentage,
            "created_at" : db_product.created_at,
            "updated_at" : db_product.updated_at
        }
    }


# @product_cateogry_router.delete("/get/product_category/{product_id}")
# def delete_product(
#     product_id : str,
#     db : Session = Depends(get_db)
# ):
    
#     db_product = db.query(MasterProductDB).filter(MasterProductDB.product_id == product_id).first()

#     if not db_product:
#         raise HTTPException(
#             status_code=status.HTTP_204_NO_CONTENT,
#             detail="Product not found"
#         )
    
#     db.delete(db_product)

#     db.commit() 
    
#     return{
#         "status" : status.HTTP_200_OK,
#         "message" : "product category deleted successfully",
#         "products" : {
#             db_product.product_id,
#             db_product.product_name,
#             db_product.HSN_code,
#             db_product.category,
#             db_product.bike_category,
#             db_product.size,
#             db_product.color,
#             db_product.unit,
#             db_product.gst
#         }
#     }


@product_cateogry_router.delete("/get/product_category/{epc_code}")
def delete_product_by_epc(
    epc_code : str,
    db : Session = Depends(get_db)
):
    
    db_product = db.query(MasterProductDB).filter(MasterProductDB.EPC_code == epc_code, MasterProductDB.is_deleted == False).first()


    if not db_product:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Product not found to delete"
    )

    # db_product_inventory = db.query(InvoiceProductsDB).filter(InvoiceProductsDB.EPC_code == epc_code, InvoiceProductsDB.is_deleted == False).first()
    
    # if db_product_inventory:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail= "The product cannot be deleted because it is referenced by items in the inventory."
    #     )

    db_product.is_deleted = True

    db.commit()

    bikes = db.query(BikeDb).filter(BikeDb.bike_id.in_(db_product.bike_category)).all()
    
    return {
        "status": status.HTTP_200_OK,
        "message": "Product category deleted successfully",
        # "products": {
        #     "product_name": db_product.product_name,
        #     "EPC_code": db_product.EPC_code,
        #     "HSN_code": db_product.HSN_code,
        #     # "category": db_product.category_relation.category,
        #     "bike_category": [bike.bike_name for bike in bikes],
        #     "size": db_product.size_relation.size,
        #     "color": db_product.color_relation.color,
        #     "unit": db_product.unit_relation.unit,
        #     "gst": db_product.gst_relation.gst_percentage
        # }
    }


@product_cateogry_router.delete("/v3/get/product_category/{epc_code}")
def delete_product_by_epc_v3(
    epc_code : str,
    db : Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if current_user["inventory_privileges"]["edit"] == False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "You don't have enough permission to delete master product"
        )

    db_product = db.query(MasterProductDB).filter(MasterProductDB.EPC_code == epc_code, MasterProductDB.is_deleted == False).first()


    if not db_product:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Product not found to delete"
    )

    # db_product_inventory = db.query(InvoiceProductsDB).filter(InvoiceProductsDB.EPC_code == epc_code, InvoiceProductsDB.is_deleted == False).first()
    
    # if db_product_inventory:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail= "The product cannot be deleted because it is referenced by items in the inventory."
    #     )

    db_product.is_deleted = True

    db.commit()

    bikes = db.query(BikeDb).filter(BikeDb.bike_id.in_(db_product.bike_category)).all()
    
    return {
        "status": status.HTTP_200_OK,
        "message": "Product category deleted successfully",
        # "products": {
        #     "product_name": db_product.product_name,
        #     "EPC_code": db_product.EPC_code,
        #     "HSN_code": db_product.HSN_code,
        #     # "category": db_product.category_relation.category,
        #     "bike_category": [bike.bike_name for bike in bikes],
        #     "size": db_product.size_relation.size,
        #     "color": db_product.color_relation.color,
        #     "unit": db_product.unit_relation.unit,
        #     "gst": db_product.gst_relation.gst_percentage
        # }
    }


@product_cateogry_router.get("/v2/get/hsn_code/{hsn_code}/product_name/{product_name:path}")
def get_product_by_name_code_v2(
    hsn_code : str,
    product_name : str,
    db : Session = Depends(get_db)
):
    
    db_product = db.query(MasterProductDB).filter(MasterProductDB.HSN_code == hsn_code, func.lower(func.trim(MasterProductDB.product_name)) == product_name.lower(), MasterProductDB.is_deleted == False).all()

    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    products_with_category = []
    for product in db_product:
        bike_ids = product.bike_category
        bikes = db.query(BikeDb).filter(BikeDb.bike_id.in_(bike_ids)).all()

        bike_list = []
        for bike in bikes:
            bike_list.append(bike.bike_name)

        # bike_categories = [bike.bike_category_name for bike in product.bike_relationship]
        products_with_category.append({
            "EPC_code": product.EPC_code,
            "product_name": product.product_name,
            "HSN_code": product.HSN_code,
            "category": product.category_relation.category_name,  # Access the category name
            "bike_category": bike_list,
            "size": product.size_relation.size_name,
            "color": product.color_relation.color_name,
            "unit": product.unit_relation.unit_name,
            "gst": product.gst_relation.gst_percentage,
            "created_at": product.created_at,
            "updated_at": product.updated_at,
            "user": product.user
        })
        
    return{
        "status" : status.HTTP_200_OK,
        "message" : "product category fetched successfully",
        "products" : products_with_category
    }


@product_cateogry_router.get("/v2/master_products/count")
def total_products(db : Session = Depends(get_db)):

    db_products_count = db.query(MasterProductDB).filter(MasterProductDB.is_deleted == False).count()

    return{
        "total_master_products" : db_products_count
    }