import util
import csv

QUESTIONS_HEADERS = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWERS_HEADERS = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


def read_data(file_name):
    data = []
    with open(util.is_file_exist(file_name), 'r') as data_from_file:
        csv_reader = csv.DictReader(data_from_file, delimiter=',')
        for datum in csv_reader:
            data.append(datum)
    return data


def overwrite_data(file_name, data):
    with open(util.is_file_exist(file_name), 'w') as data_from_file:
        if 'question' in file_name:
            fieldnames = QUESTIONS_HEADERS
        else:
            fieldnames = ANSWERS_HEADERS
        writer = csv.DictWriter(data_from_file, fieldnames, extrasaction='ignore')
        writer.writeheader()
        for entry in data:
            writer.writerow(entry)


def add_data(file_name, data):
    with open(util.is_file_exist(file_name), 'a') as data_from_file:
        if 'question' in file_name:
            fieldnames = QUESTIONS_HEADERS
        else:
            fieldnames = ANSWERS_HEADERS
        writer = csv.DictWriter(data_from_file, fieldnames)
        writer.writerow(data)
