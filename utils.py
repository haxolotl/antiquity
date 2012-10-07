
def is_leap_year(year):
    return (year % 4 == 0 and year % 100 != 0) or year % 400 == 0
    

def get_year_length(year):
    if is_leap_year(year):
        return 366
    else:
        return 365
    

def get_month_length(year, month):
    normal_lengths = [31,28,31,30,31,30,31,31,30,31,30,31]
    leap_lengths = [31,29,31,30,31,30,31,31,30,31,30,31]
    if is_leap_year(year):
        return leap_lengths[month-1]
    else:
        return normal_lengths[month-1]