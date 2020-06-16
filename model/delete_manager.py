from model import connection
from psycopg2.extras import RealDictCursor


@connection.connection_handler
def delete_entry(cursor: RealDictCursor, data_type, data_id):
    query = "DELETE FROM ONLY {0} WHERE id = {1}".format(data_type, data_id)
    cursor.execute(query)


@connection.connection_handler
def delete_tag(cursor: RealDictCursor, question_id, tag_id):
    query = "DELETE FROM ONLY question_tag WHERE tag_id = {0} AND question_id = {1}".format(tag_id, question_id)
    cursor.execute(query)
    query = "DELETE FROM ONLY tag WHERE id = {0}".format(tag_id)
    cursor.execute(query)
