import datetime
import re


def convert_string_to_time(string):
    this_time = re.sub("\+[0-9]+$", "", string)
    try:
        time_object = datetime.datetime.strptime(this_time, "%Y-%m-%d %H:%M:%S.%f")
    except TypeError:
        # This exception is only for our test that wants str not date obj
        time_object = item.time_created
    except ValueError:
        time_object = datetime.datetime.strptime(this_time, "%Y-%m-%d %H:%M:%S")

    return time_object