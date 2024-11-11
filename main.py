from fastapi import FastAPI
from app.salary_surat.route.route import salary_router
from app.User.views.route import login_router, signup_router, protected_router,forgot_password_route, delete_route
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.file_system.route import file_router
from app.client.route import client_router
from app.vendor.route import vendor_router
from app.salary_ahmedabad.route.zomato import ahmedabad_router
from app.salary_surat.route.zomato_structure2 import surat_zomato_structure2_router
from app.salary_surat.route.swiggy_structure2 import surat_swiggy_structure2_router
from app.salary_surat.route.master_api.zomato import master_router
from app.salary_ahmedabad.route.flipkart import ahmedabad_flipkart_router
from app.salary_ahmedabad.route.ecom import ahmedabad_ecom_router
from app.salary_ahmedabad.route.blinkit import ahmedabad_blinkit_router
from app.salary_ahmedabad.route.big_basket import ahmedabadbigbascket
from app.salary_ahmedabad.route.bbnow import ahmedabadbbnow_router
from app.Inventory_in.route import inventory_router
from app.product.route.route import product_router
from app.Inventory_in.category_new.route import new_category_router
from app.Inventory_in.bike_category.route import bike_router
from app.Inventory_in.city_category.route import city_router
from app.Inventory_in.color_category.route import color_router
from app.Inventory_in.size_category.route import size_router
from app.inventory_out.route import inventory_out_router
from app.Inventory_in.master_product.route import product_cateogry_router
from app.Inventory_in.vendor_category.route import vendor_category_router
from app.Inventory_in.unit_category.route import unit_router
from app.weekly_salary.raw_file.route import weekly_raw
from app.weekly_salary.salary_file.route import weekly_salary
from app.sales.route import sales_router
from app.Inventory_in.gst_category.route import gst_router
from app.Inventory_in.transfer_product.route import transfer_router


app = FastAPI()

    
app.include_router(salary_router, prefix="/surat", tags= ["Surat Salary Structure 1"])
app.include_router(signup_router, tags= ["Authentication"])
app.include_router(login_router, tags= ["Authentication"])
app.include_router(protected_router, tags= ["Authentication"])
app.include_router(delete_route, tags= ["Authentication"])
app.include_router(forgot_password_route, tags= ["Authentication"])
app.include_router(file_router, tags=["File Operation"])
app.include_router(client_router, tags= ["Client"])
app.include_router(vendor_router, tags= ["Vender"])
app.include_router(ahmedabad_router, prefix="/ahmedabad", tags= ["Ahmedabad Salary Structure 1"])
app.include_router(surat_zomato_structure2_router, prefix= "/surat", tags=["Surat Structure 2"])
app.include_router(surat_swiggy_structure2_router, prefix='/surat', tags=["Surat Structure 2"])
# app.include_router(master_router, prefix='/surat')
app.include_router(ahmedabad_flipkart_router, prefix='/ahmedabad', tags= ["Ahmedabad Salary Structure 1"])
app.include_router(ahmedabad_ecom_router, prefix='/ahmedabad', tags= ["Ahmedabad Salary Structure 1"])
app.include_router(ahmedabad_blinkit_router, prefix='/ahmedabad', tags= ["Ahmedabad Salary Structure 1"])
app.include_router(ahmedabadbigbascket, prefix="/ahmedabad", tags= ["Ahmedabad Salary Structure 1"])
app.include_router(ahmedabadbbnow_router, prefix="/ahmedabad", tags= ["Ahmedabad Salary Structure 1"])
app.include_router(inventory_router, tags=["Inventory"])
app.include_router(product_router, tags=["Inventory Products"])
app.include_router(new_category_router, tags=["Category"])
app.include_router(bike_router, tags=["Bike Category"])
app.include_router(city_router, tags=["City Category"])
app.include_router(color_router, tags=["Color Category"])
app.include_router(size_router, tags=["Size Category"])
app.include_router(product_cateogry_router, tags=["Master Product"])
app.include_router(vendor_category_router, tags=["Vendor Category"])
app.include_router(unit_router, tags=['Unit Category'])
app.include_router(gst_router, tags=["GST"])
app.include_router(inventory_out_router, tags=["Inventory Out Router"])
app.include_router(weekly_raw, tags=["Weekly Raw"])
app.include_router(weekly_salary, tags=["Weekly Salary"])
app.include_router(sales_router, tags=["Sales"])
app.include_router(transfer_router, tags=["Transfer_Products"])


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True)
