import connection
import util
from flask import request
QUESTIONS_FILE = "sample_data/question.csv"
ANSWERS_FILE = "sample_data/answer.csv"
QUESTION_HEADERS = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWER_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


def get_all_questions():
    return connection.read_data(QUESTIONS_FILE)


def sort_condition(element, key):
    return int(element[key]) if key in ['view_number', 'vote_number', 'submission_time'] else element[key]


def get_sorted_questions(sorting_key, reverse_bool):
    return sorted(get_all_questions(), key=lambda i: sort_condition(i, sorting_key), reverse=reverse_bool)


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


def add_answer_with_basic_headers(question_id):
    answer = {}
    for header in ANSWER_HEADER:
        if header == 'id':
            answer[header] = '3'
        elif header == 'submission_time':
            answer[header] = 'sdalj'
        elif header == 'vote_number':
            answer[header] = 0
        elif header == 'question_id':
            answer[header] = question_id
        elif header == 'image':
            answer[header] = ''
        else:
            answer[header] = request.form.get(header)
    return answer


def save_new_answer(answer):
    connection.add_data(ANSWERS_FILE, answer)


def update_dictionary(file_name, data, key_to_find):
    for dictionary in data:
        if dictionary["view_number"] == key_to_find:
            dictionary[key_to_find] = int(dictionary[key_to_find]) + 1
    connection.overwrite_data(file_name, data)