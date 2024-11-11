import pandas as pd


def calculate_flipkart_salary(row, my_amount):
    order_done = row["DONE_PARCEL_ORDERS"]
    amount = 0

    amount = order_done * my_amount

    return amount


def create_table(dataframe):
    
    table = pd.pivot_table(
            data= dataframe,
            index=["DRIVER_ID", "DRIVER_NAME", "CLIENT_NAME", "CITY_NAME"],
            aggfunc={
            "REJECTION": "sum",
            "BAD_ORDER": "sum",
            "ORDER_AMOUNT": "sum",
            "DONE_PARCEL_ORDERS": "sum",
            "CUSTOMER_TIP": "sum",
            "RAIN_ORDER": "sum",
            "IGCC_AMOUNT": "sum",
            "ATTENDANCE": "sum",
            "TOTAL_ORDERS": "sum",
            "BIKE_PENALTY" : "sum",
            "OPS_BONUS"	: "sum",
            "OPS_PENALTY" : "sum",
            "TRAFFIC_CHALLAN" : "sum",
            "FATAK_PAY_ADVANCE"	: "sum",
            "ARREARS_AMOUNT" : "sum",
            "OTHER_PENALTY" : "sum",
            "REFER_BONUS" : "sum",
            "OTHER_BONUS" : "sum"
        }
       )

    return table