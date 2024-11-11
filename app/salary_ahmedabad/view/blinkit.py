import pandas as pd

def calculate_blinkit_salary(
        row,
        from_order,
        to_order,
        first_order_amount,
        order_greter_than,
        second_order_amount
):
    order_done = row["DONE_PARCEL_ORDERS"]
    amount = 0

    if from_order <= order_done <= to_order:
        amount = order_done * first_order_amount

    # elif order_done >= order_greter_than:
    #     # amount = order_done * second_order_amount
    #     amount = ((order_done - to_order) * second_order_amount) + (to_order * first_order_amount)
        
    elif order_done >= order_greter_than:
        amount = order_done * second_order_amount

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
