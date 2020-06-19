from flask import Flask, render_template, redirect, request, session
import model.data_manager as data_manager
import model.question_manager as question_manager
import model.answer_manager as answer_manager
import model.comment_manager as comment_manager
import model.tag_manager as tag_manager
import model.delete_manager as delete_manager
import model.user_manager as user_manager
from controller.update import update_data
from controller.add import add_data
from controller.user_operations import user_data

app = Flask(__name__, template_folder="../view/templates", static_folder="../view/static")
app.register_blueprint(update_data)
app.register_blueprint(add_data)
app.register_blueprint(user_data)
app.secret_key = b'\xd7S@C\xe00\xf8\x11\xefj\xf1\xbcN\xb1$\xd5'
NUMBER_OF_LATEST_QUESTIONS = 5


@app.route('/')
def home():
    questions = question_manager.fetch_n_number_of_rows(NUMBER_OF_LATEST_QUESTIONS)
    return render_template('index.html', questions=questions, is_logged_in=is_logged_in(), user_id=get_current_user())


@app.route('/list', methods=['GET', 'POST'])
def display_data():
    if request.args:
        sorting_key = request.args['sort_by']
        reverse_bool = request.args['order_descending']
        questions = question_manager.get_sorted_questions(sorting_key, reverse_bool)
    else:
        questions = data_manager.get_all_data('question')
    tags = tag_manager.get_question_tags()
    comments = comment_manager.get_question_comments()
    question_headers = question_manager.QUESTION_HEADERS
    return render_template('./display_data/list.html', questions=questions, question_headers=question_headers, tags=tags,
                           comments=comments, is_logged_in=is_logged_in(), user_id=get_current_user())


@app.route('/question/<question_id>')
def display_answers(question_id):
    current_user = get_current_user()
    answer_headers = answer_manager.ANSWER_HEADER
    answer_details = data_manager.fetch_data(question_id, 'answer')
    question_details = data_manager.fetch_data(question_id, 'question')
    best_answer = user_manager.is_best_answer_selected(question_id)
    answer_id = user_manager.get_best_answer(question_id)
    question_manager.update_view_number(question_id)
    comments = comment_manager.get_question_comments()
    return render_template('display_data/list_answers.html', answer_details=answer_details,
                           question_details=question_details, answer_headers=answer_headers,
                           comments=comments, is_logged_in=is_logged_in(), current_user=current_user,
                           answer_id=answer_id, best_answer=best_answer)


@app.route('/<library_type>/<datum_id>/<vote>')
def get_vote(library_type, datum_id, vote):
    table_type = 'question' if library_type == 'question' else 'answer'
    if vote not in ['accepted', 'uncheck']:
        data_manager.update_votes(table_type, datum_id, vote)
    if is_logged_in():
        user_id = user_manager.get_user_id(table_type, datum_id)
        user_manager.update_reputation(user_id, table_type, vote, datum_id)
        if table_type == 'answer':
            answers = data_manager.get_question_id_for_answer(datum_id)
            return redirect("/question/{0}".format(answers))
    return redirect('/list')


@app.route('/search')
def search_phrase():
    phrase = request.args.get('q')
    questions = data_manager.get_phrase_match_data(phrase)
    question_headers = question_manager.QUESTION_HEADERS
    return render_template('display_data/search_box_answers.html', questions=questions,
                           question_headers=question_headers)


@app.route("/<data_type>/<data_id>/delete")
def delete(data_type, data_id):
    question_id = None
    if data_type == 'answer':
        question_id = data_manager.get_question_id_for_answer(data_id)
        data_manager.update_user_count('count_of_answers', session['email'], True)
    if data_type == 'comment':
        answer_id = data_manager.get_answer_id_for_comment(data_id)
        data_manager.update_user_count('count_of_comments', session['email'], True)
        if answer_id:
            question_id = data_manager.get_question_id_for_answer(answer_id)
    data_manager.update_user_count('count_of_asked_questions', session['email'], True)
    delete_manager.delete_entry(data_type, data_id)
    if data_type == 'answer' or (data_type == 'comment' and question_id):
        return redirect('/question/' + str(question_id))
    return redirect('/list')


@app.route('/question/<question_id>/tag/<tag_id>/delete')
def delete_tag(question_id, tag_id):
    delete_manager.delete_tag(question_id, tag_id)
    return redirect('/list')


@app.route('/users')
def display_users():
    if is_logged_in():
        user_headers = user_manager.USERS_HEADERS
        users = data_manager.get_all_data('new_user')
        return render_template('display_data/list_users.html', users=users, user_headers=user_headers)
    return redirect('/login')


@app.route('/tags')
def show_tags():
    tags_metadata = data_manager.get_tags_with_metadata()
    return render_template('display_data/tags.html', tags_metadata=tags_metadata)


def is_logged_in():
    return 'email' in session


def get_current_user():
    if is_logged_in():
        return session['email']


if __name__ == "__main__":
    app.run(debug=True)

