from model import connection
from psycopg2.extras import RealDictCursor
from psycopg2 import sql

USERS_HEADERS = ['email', 'user_name', 'registration_time', 'count_of_asked_questions', 'count_of_answers',
                 'count_of_comments', 'reputation']


