from model import connection
from model.data_manager import remove_duplicates
from psycopg2.extras import RealDictCursor


@connection.connection_handler
def add_tag(cursor: RealDictCursor, tag_name: str):
    query = f"""
    INSERT INTO tag (name) 
    VALUES (%(tag_name)s)
    """
    cursor.execute(query, {'tag_name': tag_name})


@connection.connection_handler
def get_question_tags(cursor: RealDictCursor) -> dict:
    query = """
            SELECT tag.name, tag.id, question_tag.question_id
            FROM tag
            FULL JOIN question_tag ON question_tag.tag_id = tag.id 
            """
    cursor.execute(query)
    return cursor.fetchall()


def get_tag_list():
    return remove_duplicates(get_question_tags(), 'name')


@connection.connection_handler
def get_tag_id(cursor: RealDictCursor) -> dict:
    query = """SELECT id FROM tag ORDER BY id DESC FETCH FIRST ROW ONLY"""
    cursor.execute(query)
    return cursor.fetchone()['id']


@connection.connection_handler
def get_tag_id_by_tag_name(cursor: RealDictCursor, tag_name: str) -> dict:
    query = """SELECT id FROM tag WHERE name = %(tag_name)s"""
    cursor.execute(query, {'tag_name': tag_name})
    return cursor.fetchone()['id']


@connection.connection_handler
def add_tag_to_question_id(cursor: RealDictCursor, question_id: int, tag_id: int):
    query = f"""
        INSERT INTO question_tag (question_id, tag_id) 
        VALUES (%(question_id)s, %(tag_id)s)
        """
    cursor.execute(query, {'question_id': int(question_id), 'tag_id': int(tag_id)})
