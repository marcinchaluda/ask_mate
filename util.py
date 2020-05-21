import os
import uuid
import time

def is_file_exist(file_name):
    if os.path.isfile(file_name):
        return file_name
    return FileNotFoundError('File not Found!')


def generate_id():
    return str(uuid.uuid4())


def generate_seconds_since_epoch():
    current_time = str(time.time())
    current_time = current_time[0:10]
    return current_time


def convert_str_to_time(t):
    t = int(t)
    return time.ctime(t)
