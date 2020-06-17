from model import connection
from psycopg2.extras import RealDictCursor
from psycopg2 import sql

VOTE_UP = 1
VOTE_DOWN = -1


@connection.connection_handler
def get_all_data(cursor: RealDictCursor, data_table: str, **kwargs) -> dict:
    query = sql.SQL('SELECT * FROM ') + sql.SQL('{table}').format(table=sql.Identifier(data_table))
    query = append_where_kwargs(query, kwargs)
    cursor.execute(query)
    return cursor.fetchall()


def append_where_kwargs(query, parameters):
    if parameters:
        for column_name, row_value in parameters.items():
            query_clause = sql.SQL(" WHERE {column} = {value}").format(column=sql.Identifier(column_name),
                                                                      value=sql.Literal(row_value))
            return query + query_clause
    return query


@connection.connection_handler
def fetch_data(cursor: RealDictCursor, key_to_find: str, data_table: str) -> dict:
    current_id = 'question_id' if data_table == 'answer' else 'id'
    query = sql.SQL("SELECT * FROM {table} WHERE {current_id}={id}").\
        format(table=sql.Identifier(data_table), current_id=sql.Identifier(current_id), id=sql.Literal(key_to_find))
    cursor.execute(query)
    return cursor.fetchall()


# @connection.connection_handler
# def get_data_id(cursor: RealDictCursor, column: str, data_id: str, data_table: str):
#     query = sql.SQL("SELECT {column} FROM ").format(column=sql.Literal(column)) + \
#             sql.SQL("{table} WHERE id={data_id}").format(table=sql.Identifier(data_table), data_id=sql.Literal(data_id))
#     cursor.execute(query)
#     return cursor.fetchone()[column]


@connection.connection_handler
def get_question_id_for_answer(cursor: RealDictCursor, data_id: str):
    query = "SELECT question_id FROM answer WHERE id = {0}".format(data_id)
    cursor.execute(query)
    return cursor.fetchone()['question_id']


@connection.connection_handler
def get_answer_id_for_comment(cursor: RealDictCursor, data_id: str):
    query = "SELECT answer_id FROM comment WHERE id = {0}".format(data_id)
    cursor.execute(query)
    try:
        return cursor.fetchone()['answer_id']
    except TypeError:
        return None


@connection.connection_handler
def update_votes(cursor: RealDictCursor, table_type: str, datum_id: str, vote):
    update_vote = VOTE_UP if vote == 'vote_up' else VOTE_DOWN
    query = sql.SQL('UPDATE {table} SET vote_number = vote_number + {update_vote} WHERE id = {datum_id}').\
        format(table=sql.Identifier(table_type), update_vote=sql.Literal(int(update_vote)),
               datum_id=sql.Literal(datum_id))
    cursor.execute(query)


@connection.connection_handler
def get_phrase_match_data(cursor: RealDictCursor, phrase: str) -> dict:
    question_query = """
        SELECT question.id, question.submission_time, question.view_number, question.vote_number, question.title, 
        question.message, question.image 
        FROM question
        FULL JOIN answer ON answer.question_id = question.id 
        WHERE question.title ILIKE %(phrase)s 
        OR question.message ILIKE %(phrase)s
        OR answer.message ILIKE %(phrase)s"""
    cursor.execute(question_query, {'phrase': '%' + phrase + '%'})
    data = remove_duplicates(cursor.fetchall(), 'id')
    return data


def remove_duplicates(data, key_to_find):
    no_duplicates = []
    for datum in data:
        if not no_duplicates:
            no_duplicates.append(datum)
        else:
            duplicate = check_for_id_duplicate(no_duplicates, key_to_find, datum['id'])
            if not duplicate:
                no_duplicates.append(datum)
    return no_duplicates


def check_for_id_duplicate(data, key_to_find, id_to_check):
    for element in data:
        if element[key_to_find] == id_to_check:
            return True
    return False
