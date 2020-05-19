import connection


QUESTIONS_FILE = "sample_data/question.csv"
ANSWERS_FILE = "sample_data/answer.csv"
QUESTION_HEADERS = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWER_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


def get_all_questions():
    return connection.read_data(QUESTIONS_FILE)


def get_all_answers():
    return connection.read_data(ANSWERS_FILE)


def fetch_dictionary(key_to_find, dictionary_list):
    for dictionary in dictionary_list:
        for key, value in dictionary.items():
            if value == key_to_find:
                return dictionary


def delete_dictionary(filename, id):
    data = connection.read_data(filename)
    dict_to_delete = fetch_dictionary(id, data)
    del data.remove(dict_to_delete)
    connection.overwrite_data(filename, data)
    return None
