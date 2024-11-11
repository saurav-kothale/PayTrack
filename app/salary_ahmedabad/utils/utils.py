
def add_attendance_incentive(
        row, 
        attendance,
        incentive,
        average
):
    rider_attendance = row["ATTENDANCE"]
    rider_average = row["AVERAGE"]
    amount = 0

    if rider_attendance >= attendance and rider_average >= average:
        amount = incentive

    return amount


def add_attendance_incentive_on_attendance(
        row,
        attendance,
        incentive
):
    rider_attendance = row["ATTENDANCE"]
    amount = 0

    if rider_attendance >= attendance:
        amount = incentive

    return amount