from model import connection
from psycopg2.extras import RealDictCursor
from psycopg2 import sql

USERS_HEADERS = ['email', 'user_name', 'registration_time', 'count_of_asked_questions', 'count_of_answers',
                 'count_of_comments', 'reputation']


@connection.connection_handler
def get_user_by_email(cursor: RealDictCursor, email: str):
    query = "SELECT * FROM new_user WHERE email = %s;"
    cursor.execute(query, (email, ))
    return cursor.fetchone()


@connection.connection_handler
def add_new_user(cursor: RealDictCursor, new_user_data):
    query = sql.SQL('''INSERT INTO new_user
    VALUES({user_id}, {user_name}, {submission_time}, 0, 0, 0, 0, {password})''').format(
        user_id=sql.Literal(new_user_data['user_id']),
        user_name=sql.Literal(new_user_data['user_name']),
        submission_time=sql.Literal(new_user_data['submission_time']),
        password=sql.Literal(new_user_data['password'])
    )
    cursor.execute(query)
