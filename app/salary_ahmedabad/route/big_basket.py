from functools import total_ordering
from fastapi import APIRouter, Depends, HTTPException, UploadFile,File, Form, status
from fastapi.responses import FileResponse
from pydantic import HttpUrl
from app.salary_ahmedabad.schema.big_basket import AhmedabadBigBascketSchema
from app.salary_ahmedabad.view.big_basket import calculate_big_basket_biker_salary, calculate_big_basket_micro_salary,create_table
import pandas as pd
import io
import tempfile
from app.file_system.s3_events import read_s3_contents, s3_client, upload_file
from decouple import config
from app import setting
from app.salary_ahmedabad.utils.utils import add_attendance_incentive_on_attendance


ahmedabadbigbascket = APIRouter()
processed_bucket = setting.PROCESSED_FILE_BUCKET


@ahmedabadbigbascket.post("/bigbasket/structure1/{file_id}/{file_name}")
def get_salary(
    file_id: str = None, # type: ignore
    file_name: str = None, # type: ignore
    file: UploadFile = File(...),
    biker_from_delivery: int = Form(1),
    biker_to_delivery: int = Form(8),
    first_biker_amount: int = Form(24),
    second_biker_from_delivery: int = Form(9),
    second_biker_to_delivery: int = Form(16),
    second_biker_amount: int = Form(27),
    third_biker_from_delivery: int = Form(17),
    third_biker_to_delivery: int = Form(22),
    third_biker_amount: int = Form(30),
    fourth_biker_from_delivery: int = Form(22),
    fourth_biker_to_delivery: int = Form(28),
    fourth_biker_amount: int = Form(33),
    biker_order_greter_than: int = Form(28),
    biker_second_amount: int = Form(26),
    micro_from_delivery: int = Form(1),
    micro_to_delivery: int = Form(22),
    micro_first_amount: int = Form(20),
    micro_order_greter_than : int = Form(23),
    micro_second_amount: int = Form(22),
    include_attendance_incentive : bool = Form(True),
    attendance_day : int = Form(26),
    rider_incentive_amount : int = Form(1500)
):
    df = pd.read_excel(file.file)

    df["DATE"] = pd.to_datetime(df["DATE"])

    file_key = f"uploads/{file_id}/{file_name}"

    try:

        response = s3_client.get_object(Bucket=processed_bucket, Key=file_key)

    except s3_client.exceptions.NoSuchKey:
    
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Please Calculate Zomato First"
        )

    df = df[(df["CITY_NAME"] == "ahmedabad") & (df["CLIENT_NAME"] == "bb 5k")]

    if df.empty:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail= "bb 5k client not found")

    df["BIKER_AMOUNT"] = df.apply(lambda row : calculate_big_basket_biker_salary(
        row,
        biker_from_delivery,
        biker_to_delivery,
        first_biker_amount,
        second_biker_from_delivery,
        second_biker_to_delivery,
        second_biker_amount,
        third_biker_from_delivery,
        third_biker_to_delivery,
        third_biker_amount,
        fourth_biker_from_delivery,
        fourth_biker_to_delivery,
        fourth_biker_amount,
        biker_order_greter_than,
        biker_second_amount
    ), axis=1)

    df["MICRO_AMOUNT"] = df.apply(lambda row : calculate_big_basket_micro_salary(
         row,
        micro_from_delivery,
        micro_to_delivery,
        micro_first_amount,
        micro_order_greter_than,
        micro_second_amount
    ), axis=1)

    df["ORDER_AMOUNT"] = df["BIKER_AMOUNT"] + df["MICRO_AMOUNT"]

    df["TOTAL_ORDERS"] = df["DONE_BIKER_ORDERS"] + df["DONE_MICRO_ORDERS"]

    table = create_table(df).reset_index()

    if include_attendance_incentive:
        table["ATTENDANCE_INCENTIVE"] = table.apply(lambda row : add_attendance_incentive_on_attendance(
            row,
            attendance_day,
            rider_incentive_amount
        ), axis=1)

    else :
        table["ATTENDANCE_INCENTIVE"] = 0

    table["PANALTIES"] = table["BIKE_PENALTY"] + table["OPS_PENALTY"] + table["TRAFFIC_CHALLAN"] + table["FATAK_PAY_ADVANCE"] + table["ARREARS_AMOUNT"] + table["OTHER_PENALTY"]

    table["OTHER_BONUSES"] = table["REFER_BONUS"] + table["OTHER_BONUS"] + table["OPS_BONUS"]

    table["FINAL_AMOUNT"] = table["ORDER_AMOUNT"] - table["PANALTIES"] + table["OTHER_BONUSES"] + table["ATTENDANCE_INCENTIVE"]

    table["VENDER_FEE (@6%)"] = (table["FINAL_AMOUNT"] * 0.06) + (table["FINAL_AMOUNT"])

    table["FINAL PAYBLE AMOUNT (@18%)"] = (table["VENDER_FEE (@6%)"] * 0.18) + (
        table["VENDER_FEE (@6%)"]
    )

    file_data = response["Body"].read()

    big_basket_ahmedabad = pd.DataFrame(table)

    df2 = pd.read_excel(io.BytesIO(file_data))

    df3 = pd.concat([df2, big_basket_ahmedabad], ignore_index=True)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
        with pd.ExcelWriter(temp_file.name, engine="xlsxwriter") as writer:
            df3.to_excel(writer, sheet_name="Sheet1", index=False)

            # file_key = f"uploads/{file_id}/modified.xlsx"
        s3_client.upload_file(temp_file.name, processed_bucket, file_key)

    return {
        "message" : "Big Basket Salary Calculated Successfully",
        "file_id": file_id,
        "file_name": file_name, 
        "file_key" : file_key
    }


    # with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
    #     with pd.ExcelWriter(temp_file.name, engine="xlsxwriter") as writer:
    #         table.to_excel(writer, sheet_name="Sheet1", index=False)

    # content_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    # response = FileResponse(temp_file.name, media_type=content_type)
    # response.headers["Content-Disposition"] = (
    #     'attachment; filename="month_year_city.xlsx"'
    # )

    # return response


