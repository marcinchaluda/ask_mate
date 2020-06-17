from model import connection, util
from flask import request, session
from psycopg2.extras import RealDictCursor

QUESTION_HEADERS = ['id', 'user_id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']


@connection.connection_handler
def get_sorted_questions(cursor: RealDictCursor, sorting_key, reverse_bool) -> list:
    reverse_bool = 'DESC' if reverse_bool == 'True' else 'ASC'
    query = """
        SELECT * FROM question ORDER BY {0} {1}""".format(sorting_key, reverse_bool)
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def fetch_n_number_of_rows(cursor: RealDictCursor, rows_number: int) -> dict:
    query = f"SELECT * FROM question ORDER BY {'submission_time'} {'DESC'} FETCH FIRST {int(rows_number)} ROW ONLY"
    cursor.execute(query)
    return cursor.fetchall()


def add_question_with_basic_headers():
    question = {}
    for header in QUESTION_HEADERS:
        if header == 'view_number' or header == 'vote_number':
            question[header] = 0
        elif header == 'submission_time':
            question[header] = util.generate_seconds_since_epoch()
        elif header == 'user_id':
            question[header] = session['email']
        else:
            question[header] = request.form.get(header)
    return question


@connection.connection_handler
def save_new_question(cursor: RealDictCursor, question: dict):
    query = f"""
    INSERT INTO question (submission_time, user_id, view_number, vote_number, title, message, image) 
    VALUES (%(submission_time)s, %(user_id)s ,%(view_number)s, %(vote_number)s, %(title)s, %(message)s, %(image)s )
    RETURNING id
    """
    cursor.execute(query, question)
    question_id = cursor.fetchone()['id']
    return question_id


@connection.connection_handler
def update_view_number(cursor: RealDictCursor, key_to_find: str):
    query = "UPDATE question SET view_number = view_number + 1 WHERE  id = %(key_to_find)s"
    cursor.execute(query, {'key_to_find': key_to_find})


@connection.connection_handler
def update_question(cursor: RealDictCursor, question_id: str):
    message = request.form.get('message')
    title = request.form.get('title')
    query = """
        UPDATE question
        SET message = %(m)s, title = %(t)s
        WHERE id = %(q_i)s
    """
    cursor.execute(query, {'m': message, 'q_i': question_id, 't': title})
