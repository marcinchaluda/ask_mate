from model import connection, util
from flask import request, session
from psycopg2.extras import RealDictCursor

COMMENTS_HEADERS = ['submission_time', 'user_id', 'question_id', 'answer_id', 'message', 'edited_count']


def add_comment_with_basic_headers(data_id: str, is_this_comment_for_question: bool):
    comment = {}
    for header in COMMENTS_HEADERS:
        if header == 'submission_time':
            comment[header] = util.generate_seconds_since_epoch()
        elif header == 'edited_count':
            comment[header] = 0
        elif header == 'question_id' and is_this_comment_for_question:
            comment[header] = data_id
        elif header == 'answer_id' and not is_this_comment_for_question:
            comment[header] = data_id
        elif header == 'user_id':
            comment[header] = session['email']
        else:
            comment[header] = request.form.get(header)
    return comment


@connection.connection_handler
def get_question_id_from_answer(cursor: RealDictCursor, answer_id):
    query = "SELECT question_id FROM answer WHERE id = %s"
    cursor.execute(query, (answer_id, ))
    return cursor.fetchone()


@connection.connection_handler
def save_new_comment(cursor: RealDictCursor, comment: dict):
    query = f"""
    INSERT INTO comment (submission_time ,question_id, answer_id, edited_count, message, user_id) 
    VALUES (%(submission_time)s ,%(question_id)s, %(answer_id)s, %(edited_count)s, %(message)s, %(user_id)s)
    """
    cursor.execute(query, comment)


def save_comment(data_id, is_question):
    comment = add_comment_with_basic_headers(data_id, is_question)
    save_new_comment(comment)


@connection.connection_handler
def get_question_comments(cursor: RealDictCursor) -> dict:
    cursor.execute("SELECT id, question_id, answer_id, message, submission_time, edited_count FROM comment")
    return cursor.fetchall()


@connection.connection_handler
def update_comment(cursor: RealDictCursor, comment: dict):
    message = request.form.get('message')
    query = """
        UPDATE comment
        SET message = %(m)s, edited_count = %(e_c)s, submission_time = %(s_t)s
        WHERE id = %(c_i)s
    """
    cursor.execute(query, {'e_c': comment['edited_count']+1, 'm': message, 'c_i': comment['id'],
                           's_t': util.generate_seconds_since_epoch()})
