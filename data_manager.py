import connection
import util
from flask import request
QUESTIONS_FILE = "sample_data/question.csv"
ANSWERS_FILE = "sample_data/answer.csv"
QUESTION_HEADERS = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWER_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


def get_all_questions():
    return connection.read_data(QUESTIONS_FILE)


def get_sorted_questions(sorting_key, reverse_bool):
    return sorted(get_all_questions(), key=lambda i: i[sorting_key], reverse=reverse_bool)


def get_all_answers():
    return connection.read_data(ANSWERS_FILE)


def fetch_dictionary(key_to_find, dictionary_list):
    for dictionary in dictionary_list:
        for key, value in dictionary.items():
            if value == key_to_find:
                return dictionary


def fetch_answers(key_to_find):
    dictionaries = []
    for dictionary in get_all_answers():
        if dictionary["question_id"] == key_to_find:
            dictionaries.append(dictionary)
    return dictionaries


def delete_dictionary(filename, id):
    data = connection.read_data(filename)
    dict_to_delete = fetch_dictionary(id, data)
    data.remove(dict_to_delete)
    connection.overwrite_data(filename, data)
    return None


def add_question_with_basic_headers():
    question = {}
    for header in QUESTION_HEADERS:
        if header == 'id':
            question[header] = '6'
        elif header == 'submission_time':
            question[header] = "sadfasf"
        elif header == 'view_number' or header == 'vote_number':
            question[header] = 0
        elif header == 'image':
            question[header] = ''
        else:
            question[header] = request.form.get(header)
    return question


def save_new_question(question):
    connection.add_data(QUESTIONS_FILE, question)


if __name__ == "__main__":
    print(fetch_answers("1"))