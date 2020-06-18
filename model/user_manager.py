from model import connection
from psycopg2.extras import RealDictCursor
from psycopg2 import sql
import model.data_manager as data_manger

USERS_HEADERS = ['email', 'user_name', 'registration_time', 'count_of_asked_questions', 'count_of_answers',
                 'count_of_comments', 'reputation']
REPUTATION_POINTS = {'question_vote_up': 5, 'question_vote_down': -2, 'answer_vote_up': 10, 'answer_vote_down': -2,
                     'answer_accepted': 15, 'answer_uncheck': 0}


@connection.connection_handler
def get_user_by_email(cursor: RealDictCursor, email: str):
    query = "SELECT * FROM new_user WHERE email = %s;"
    cursor.execute(query, (email, ))
    return cursor.fetchone()


@connection.connection_handler
def get_user_id(cursor: RealDictCursor, data_table: str, data_id: str):
    query = sql.SQL("SELECT user_id FROM {table} WHERE id={id}"). \
        format(table=sql.Identifier(data_table), id=sql.Literal(data_id))
    cursor.execute(query)
    return cursor.fetchone()['user_id']


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


@connection.connection_handler
def update_reputation(cursor: RealDictCursor, user_id: str, table_type: str, vote: str, datum_id: str):
    if vote == 'accepted' or vote == 'uncheck':
        check_accepted_answer(vote, user_id, datum_id)
    reputation_points = int(REPUTATION_POINTS[f"{table_type}_{vote}"])
    query = sql.SQL('UPDATE new_user SET reputation = reputation + {reputation_points} WHERE email={user_id}').\
        format(reputation_points=sql.Literal(reputation_points), user_id=sql.Literal(user_id))
    cursor.execute(query)


@connection.connection_handler
def check_accepted_answer(cursor: RealDictCursor, vote: str, user_id: str, answer_id: str):
    selection_status = 'True' if vote == "accepted" else 'False'
    query = sql.SQL('UPDATE answer SET accepted_answer={selection_status} WHERE user_id={user_id} '
                    'AND id={answer_id}').format(selection_status=sql.Literal(selection_status),
                                                        user_id=sql.Literal(user_id), answer_id=sql.Literal(answer_id))
    cursor.execute(query)


@connection.connection_handler
def get_accepted_answer_column(cursor: RealDictCursor, question_id: str) -> dict:
    query = sql.SQL('SELECT id, accepted_answer FROM answer WHERE question_id={question_id}').\
        format(question_id=sql.Literal(question_id))
    cursor.execute(query)
    return cursor.fetchall()


def is_best_answer_selected(question_id):
    answers = [value['accepted_answer'] for value in get_accepted_answer_column(question_id)]
    return True if True in answers else False


def get_best_answer(question_id):
    for answer in get_accepted_answer_column(question_id):
        if answer['accepted_answer']:
            return answer['id']




