
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


def str_to_bool(source_string):
    return source_string.lower() in 'true'


def get_sorted_questions(sorting_key, reverse_bool):
    return sorted(get_all_questions(), key=lambda i: sort_condition(i, sorting_key), reverse=str_to_bool(reverse_bool))


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


def get_question_id_for_answer(data_id):
    answer = fetch_dictionary(data_id, get_all_answers())
    return answer['question_id']


def delete_dictionary(filename, id):
    data = connection.read_data(filename)
    dict_to_delete = fetch_dictionary(id, data)
    data.remove(dict_to_delete)
    connection.overwrite_data(filename, data)
    return None


def delete_related_answers(filename, id):
    if 'question' in filename:
        data = connection.read_data(filename)
        dict_to_delete = fetch_dictionary(id, data)
        data.remove(dict_to_delete)
        connection.overwrite_data(filename, data)
    else:
        data = connection.read_data(filename)
        for dict in fetch_answers(id):
            data.remove(dict)
        connection.overwrite_data(filename, data)
    return None


def add_question_with_basic_headers():
    question = {}
    for header in QUESTION_HEADERS:
        if header == 'id':
            question[header] = util.generate_id()
        elif header == 'submission_time':
            question[header] = util.generate_seconds_since_epoch()
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
            answer[header] = util.generate_id()
        elif header == 'submission_time':
            answer[header] = util.generate_seconds_since_epoch()
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


def update_dictionary(file_name, data, key_to_find, vote_down=False):
    for dictionary in data:
        if dictionary[key_to_find] == key_to_find:
            if vote_down:
                dictionary[key_to_find] = int(dictionary[key_to_find]) - 1
            else:
                dictionary[key_to_find] = int(dictionary[key_to_find]) + 1
    connection.overwrite_data(file_name, data)


def update_question(file_name, data, key_to_find):
    for dictionary in data:
        if dictionary['id'] == key_to_find:
            dictionary['message'] = request.form.get('message')
            dictionary['title'] = request.form.get('title')
    connection.overwrite_data(file_name, data)


def update_value_on_given_key(key_to_find, datum_id, data, vote_down=False, answers_file=True):
    data_details = fetch_dictionary(datum_id, data)
    if vote_down and answers_file:
        data_details[key_to_find] = int(data_details[key_to_find]) - 1
        file_name = ANSWERS_FILE
    elif not vote_down and answers_file:
        data_details[key_to_find] = int(data_details[key_to_find]) + 1
        file_name = ANSWERS_FILE
    else:
        data_details[key_to_find] = int(data_details[key_to_find]) + 1
        file_name = QUESTIONS_FILE
    update_dictionary(file_name, data, key_to_find, True)
