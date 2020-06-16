from model import connection, util
from flask import request
from psycopg2.extras import RealDictCursor

ANSWER_HEADER = ['id', 'user_id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


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
