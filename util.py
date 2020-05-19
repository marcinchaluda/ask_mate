import os
import uuid


def is_file_exist(file_name):
    if os.path.isfile(file_name):
        return file_name
    else:
        raise FileNotFoundError('File not Found!')


def generate_id():
    return uuid.uuid4()
