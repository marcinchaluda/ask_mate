import os
import uuid
import datetime
import time


def is_file_exist(file_name):
    if os.path.isfile(file_name):
        return file_name
    raise FileNotFoundError('File not Found!')


def generate_id():
    return str(uuid.uuid4())


def generate_seconds_since_epoch():
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return current_time


def convert_str_to_time(t):
    t = int(t)
    return time.ctime(t)
