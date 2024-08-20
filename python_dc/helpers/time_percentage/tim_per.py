import datetime
TOTAL_DAY_SECS = 86400.0

def timedelta_percentage(input_datetime):
    d = input_datetime - datetime.datetime.combine(input_datetime.date(), datetime.time())
    return d.total_seconds() / TOTAL_DAY_SECS