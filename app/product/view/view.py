import calendar

def add_gst(gst, amount):
    if gst == "GST 5":
        return amount * 1.05
    
    elif gst == "GST 12":
        return amount * 1.12
    
    elif gst == "GST 18":
        return amount * 1.18
    
    elif gst == "GST 28":
        return amount * 1.28
    
    
def new_add_gst(gst, amount):

    gst_amount = (gst/100) * amount

    total_amount = gst_amount + amount

    return total_amount


def get_month_abbreviation(month_number):
    return calendar.month_abbr[month_number]