import connection
import util
from flask import request
from psycopg2.extras import RealDictCursor

QUESTION_HEADERS = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWER_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
VOTE_UP = 1
VOTE_DOWN = -1


@connection.connection_handler
def get_all_questions(cursor: RealDictCursor) -> dict:
    query = "SELECT * FROM question"
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_sorted_questions(cursor: RealDictCursor, sorting_key, reverse_bool) -> list:
    reverse_bool = 'DESC' if reverse_bool == 'True' else 'ASC'
    query = """
        SELECT * FROM question ORDER BY {0} {1}""".format(sorting_key, reverse_bool)
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def fetch_dictionary(cursor: RealDictCursor, key_to_find: str) -> dict:
    query = "SELECT * FROM question WHERE id = %(key_to_find)s"
    cursor.execute(query, {'key_to_find': key_to_find})
    return cursor.fetchall()


@connection.connection_handler
def fetch_answers(cursor: RealDictCursor, key_to_find: str) -> dict:
    query = "SELECT * FROM answer WHERE question_id = %(key_to_find)s"
    cursor.execute(query, {'key_to_find': key_to_find})
    return cursor.fetchall()


@connection.connection_handler
def delete_dictionary(cursor: RealDictCursor, data_type, data_id):
    query = """
    DELETE FROM ONLY {0} WHERE id = {1}""".format(data_type, data_id)
    cursor.execute(query)


def add_question_with_basic_headers():
    question = {}
    for header in QUESTION_HEADERS:
        if header == 'view_number' or header == 'vote_number':
            question[header] = 0
        elif header == 'submission_time':
            question[header] = util.generate_seconds_since_epoch()
        else:
            question[header] = request.form.get(header)
    return question


@connection.connection_handler
def save_new_question(cursor: RealDictCursor, question: dict):
    query = f"""
    INSERT INTO question (submission_time ,view_number, vote_number, title, message, image) 
    VALUES (%(s_t)s ,%(v_n)s, %(vo_n)s, %(t)s, %(m)s, %(i)s )
    RETURNING id
    """
    cursor.execute(query, {'s_t': question['submission_time'], 'v_n': question['view_number'], 'vo_n': question['vote_number'],
                           't': question['title'], 'm': question['message'], 'i': question['image']})
    question_id = cursor.fetchone()['id']
    return question_id


def add_answer_with_basic_headers(question_id):
    answer = {}
    for header in ANSWER_HEADER:
        if header == 'submission_time':
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

@connection.connection_handler
def save_new_answer(cursor: RealDictCursor, answer: dict, data_id: str):
    query = f"""
    INSERT INTO answer (submission_time ,question_id, vote_number, message, image) 
    VALUES (%(s_t)s ,%(q_i)s, %(vo_n)s, %(m)s, %(i)s )
    """
    cursor.execute(query, {'s_t': answer['submission_time'], 'q_i': data_id,
                           'vo_n': answer['vote_number'], 'm': answer['message'], 'i': answer['image']})


@connection.connection_handler
def update_view_number(cursor: RealDictCursor, key_to_find: str):
    query = "UPDATE question SET view_number = view_number + 1 WHERE  id = %(key_to_find)s"
    cursor.execute(query, {'key_to_find': key_to_find})


def update_question(file_name, data, key_to_find):
    for dictionary in data:
        if dictionary['id'] == key_to_find:
            dictionary['message'] = request.form.get('message')
            dictionary['title'] = request.form.get('title')
    connection.overwrite_data(file_name, data)


@connection.connection_handler
def update_votes(cursor: RealDictCursor, table_type: str, datum_id: str, vote):
    update_vote = VOTE_UP if vote == 'vote_up' else VOTE_DOWN
    if table_type == 'answer':
        query = f"UPDATE answer SET vote_number = vote_number + {int(update_vote)} WHERE id = {datum_id}"
    else:
        query = f"UPDATE question SET vote_number = vote_number + {int(update_vote)} WHERE id = {datum_id}"
    cursor.execute(query)


@connection.connection_handler
def fetch_n_number_of_rows(cursor: RealDictCursor, rows_number: int) -> dict:
    query = f"SELECT * FROM question ORDER BY {'submission_time'} {'DESC'} FETCH FIRST {int(rows_number)} ROW ONLY"
    cursor.execute(query)
    return cursor.fetchall()
