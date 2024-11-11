import pandas as pd
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from app.salary_ahmedabad.schema.swiggy import AhmedabadSwiggySchema
from app.salary_ahmedabad.view.swiggy_structure2 import (
    calculate_salary_ahmedabad,
    create_table,
    add_bonus,
    calculate_bike_charges
)
from app.file_system.s3_events import read_s3_contents, s3_client, upload_file
from decouple import config
import io
import tempfile
from app import setting
from app.salary_ahmedabad.utils.utils import add_attendance_incentive, add_attendance_incentive_on_attendance


ahmedabad_swiggy_structure_router = APIRouter()
processed_bucket = setting.PROCESSED_FILE_BUCKET


@ahmedabad_swiggy_structure_router.post("/swiggy/structure1")
def claculate_salary(
    data: AhmedabadSwiggySchema = Depends(), file: UploadFile = File(...)
):

    df = pd.read_excel(file.file)

    df = df[(df["CITY_NAME"] == "ahmedabad") & (df["CLIENT_NAME"] == "swiggy")]

    if df.empty:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail= "Swiggy client not found")

    df["TOTAL_ORDERS"] = df["DONE_DOCUMENT_ORDERS"] + df["DONE_PARCEL_ORDERS"]

    df["ORDER_AMOUNT"] = df.apply(lambda row: calculate_salary_ahmedabad(row, data), axis=1)

    df["BIKE_CHARGES"] = df.apply(lambda row: calculate_bike_charges(row, data), axis=1)

    table = create_table(df).reset_index()

    table["BONUS"] = table.apply(lambda row : add_bonus(row, data), axis=1)

    if data.include_attendance_incentive:
        table["ATTENDANCE_INCENTIVE"] = table.apply(lambda row : add_attendance_incentive_on_attendance(
            row, 
            data.rider_attendance,
            data.rider_incentive
        ), axis=1)

    else:
        table["ATTENDANCE_INCENTIVE"] = 0

    table["PANALTIES"] = table["IGCC_AMOUNT"] + table["REJECTION_AMOUNT"] + table["BAD_ORDER_AMOUNT"] + table["BIKE_PENALTY"] + table["OPS_PENALTY"] + table["TRAFFIC_CHALLAN"] + table["FATAK_PAY_ADVANCE"] + table["ARREARS_AMOUNT"] + table["OTHER_PENALTY"]

    table["OTHER_BONUSES"] = table["REFER_BONUS"] + table["OTHER_BONUS"] + table["OPS_BONUS"]

    table["FINAL_AMOUNT"] = (
        (table["ORDER_AMOUNT"] + table["BONUS"]) - (table["PANALTIES"] + table["BIKE_CHARGES"]) + table["OTHER_BONUSES"] + table["ATTENDANCE_INCENTIVE"]
    )

    table["FINAL PAYBLE AMOUNT (@18%)"] = (table["VENDER_FEE (@6%)"] * 0.18) + (
        table["VENDER_FEE (@6%)"]
    )

    file_key = f"uploads/{data.file_id}/{data.file_name}"

    response = s3_client.get_object(Bucket=processed_bucket, Key=file_key)

    file_data = response["Body"].read()

    swiggy_ahmedabad_table = pd.DataFrame(table)

    df2 = pd.read_excel(io.BytesIO(file_data))

    df3 = pd.concat([df2, swiggy_ahmedabad_table], ignore_index=True)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
        with pd.ExcelWriter(temp_file.name, engine="xlsxwriter") as writer:
            df3.to_excel(writer, sheet_name="Sheet1", index=False)

            # file_key = f"uploads/{file_id}/modified.xlsx"
        s3_client.upload_file(temp_file.name, processed_bucket, file_key)

    return {"file_id": data.file_id, "file_name": data.file_name}

    # with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
    #     with pd.ExcelWriter(temp_file.name, engine="xlsxwriter") as writer:
    #         table.to_excel(writer, sheet_name="Sheet1", index=False)

    # content_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    # response = FileResponse(temp_file.name, media_type=content_type)
    # response.headers["Content-Disposition"] = (
    #     'attachment; filename="month_year_city.xlsx"'
    # )

    # return response
