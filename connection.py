import util
import csv

QUESTIONS_FILE = "question.csv"
ANSWERS_FILE = "answer.csv"


def read_data(file_name):
    data = []
    with open(file_name, 'r') as data_from_file:
        csv_reader = csv.DictReader(data_from_file, delimiter=',')
        for datum in csv_reader:
            data.append(datum)
    return data
