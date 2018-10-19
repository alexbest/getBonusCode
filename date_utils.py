import datetime
import time


def get_timestamp(format):
    time_format = datetime.datetime.combine(datetime.date.today() - datetime.timedelta(),
                                            datetime.time.min).strftime(format)

    time_array = time.strptime(time_format, "%Y/%m/%d %H:%M:%S")
    time_stamp = int(time.mktime(time_array))
    return time_stamp


def get_now_time():
    return int(time.time())


def format_time(timestamp_mill):
    time_local = time.localtime(timestamp_mill)
    dt = time.strftime("%Y/%m/%d %H:00:00", time_local)
    return dt
