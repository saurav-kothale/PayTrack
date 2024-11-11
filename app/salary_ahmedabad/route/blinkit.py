from app.salary_ahmedabad.schema.blinkit import AhmedabadBlinkitSchema
from fastapi import APIRouter, Depends, UploadFile, File, Form, status
from fastapi.responses import FileResponse
from fastapi import HTTPException
import pandas as pd
from app.salary_ahmedabad.view.blinkit import calculate_blinkit_salary, create_table
import io
import tempfile
from app.file_system.s3_events import read_s3_contents, s3_client, upload_file
from decouple import config
from app import setting
from app.salary_ahmedabad.utils.utils import add_attendance_incentive_on_attendance


ahmedabad_blinkit_router = APIRouter()
processed_bucket = setting.PROCESSED_FILE_BUCKET


@ahmedabad_blinkit_router.post("/blinkit/structure1/{file_id}/{file_name}")
def get_salary(
    file_id : str = None, # type: ignore
    file_name: str = None, # type: ignore
    file: UploadFile = File(...),    
    from_order : int = Form(1),
    to_order : int = Form(19),
    first_order_amount : int = Form(24),
    order_greter_than : int = Form(20),
    second_order_amount : int = Form(28),
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

    df = df[(df["CITY_NAME"] == "ahmedabad") & (df["CLIENT_NAME"] == "blinkit")]

    if df.empty:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail= "blinkit client not found")

    df["ORDER_AMOUNT"] = df.apply(lambda row : calculate_blinkit_salary(
        row,
        from_order,
        to_order,
        first_order_amount,
        order_greter_than,
        second_order_amount
    ), axis=1)

    df["TOTAL_ORDERS"] = df["DONE_PARCEL_ORDERS"]

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

    blinkit_ahmedabad = pd.DataFrame(table)

    df2 = pd.read_excel(io.BytesIO(file_data))

    df3 = pd.concat([df2, blinkit_ahmedabad], ignore_index=True)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
        with pd.ExcelWriter(temp_file.name, engine="xlsxwriter") as writer:
            df3.to_excel(writer, sheet_name="Sheet1", index=False)

            # file_key = f"uploads/{file_id}/modified.xlsx"
        s3_client.upload_file(temp_file.name, processed_bucket, file_key)

    return {
        "message" : "Blinkit Salary Calculated Sucessfully",
        "file_id": file_id, 
        "file_name": file_name, 
        "file_key": file_key
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




