import time
import calendar


def cal_timestamp(time_from=None):
    if not time_from:
        time_from = time.gmtime()

    return calendar.timegm(time_from)
