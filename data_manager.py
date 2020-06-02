
import connection
import util
from flask import request
from psycopg2.extras import RealDictCursor
QUESTIONS_FILE = "sample_data/question.csv"
ANSWERS_FILE = "sample_data/answer.csv"
QUESTION_HEADERS = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWER_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
VOTE_UP = 1
VOTE_DOWN = -1


@connection.connection_handler
def get_all_questions(cursor: RealDictCursor) -> list:
    query = """
        SELECT * FROM question"""
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_sorted_questions(cursor: RealDictCursor, sorting_key, reverse_bool) -> list:
    reverse_bool = 'DESC' if reverse_bool == 'True' else 'ASC'
    query = """
        SELECT * FROM question ORDER BY {0} {1}""".format(sorting_key, reverse_bool)
    cursor.execute(query)
    return cursor.fetchall()


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


def update_dictionary(file_name, data, key_to_find, vote=0):
    for dictionary in data:
        if dictionary[key_to_find] == key_to_find:
            dictionary[key_to_find] = int(dictionary[key_to_find]) + vote
    connection.overwrite_data(file_name, data)


def update_question(file_name, data, key_to_find):
    for dictionary in data:
        if dictionary['id'] == key_to_find:
            dictionary['message'] = request.form.get('message')
            dictionary['title'] = request.form.get('title')
    connection.overwrite_data(file_name, data)


def update_value_on_given_key(file_name, data_library, datum_id, key_to_find, vote):
    update_vote = VOTE_UP if vote == 'vote_up' else VOTE_DOWN
    data_details = fetch_dictionary(datum_id, data_library)
    data_details[key_to_find] = int(data_details[key_to_find]) + update_vote
    update_dictionary(file_name, data_library, key_to_find, update_vote)
