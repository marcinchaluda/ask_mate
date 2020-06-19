from flask import render_template, redirect, request, Blueprint, session
import model.data_manager as data_manager
import model.question_manager as question_manager
import model.answer_manager as answer_manager
import model.comment_manager as comment_manager
import model.tag_manager as tag_manager
import os
import services.security as security

add_data = Blueprint('add_data', __name__)
UPLOAD_FOLDER = 'static/images/'

@add_data.route("/add_question", methods=['GET', 'POST'])
def add_new_question():
    security.is_user_loggedin('add_question.html')
    question = question_manager.add_question_with_basic_headers()
    file = request.files['file']
    filename = file.filename
    if filename != '':
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        img_path = 'static/images/' + filename
        question['image'] = img_path
    question_id = question_manager.save_new_question(question)
    data_manager.update_user_count('count_of_asked_questions', session['email'], False)
    return redirect('/question/' + str(question_id))


@add_data.route("/question/<data_id>/new_answer", methods=['GET', 'POST'])
def add_new_answer(data_id):
    is_user_loggedin('new_answer.html', data_id=data_id)
    answer = answer_manager.add_answer_with_basic_headers(data_id)
    file = request.files['file']
    filename = file.filename
    if filename != '':
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        img_path = 'static/images/' + filename
        answer['image'] = img_path
    answer_manager.save_new_answer(answer, data_id)
    data_manager.update_user_count('count_of_answers', session['email'], False)
    return redirect('/question/' + data_id)


@add_data.route("/<data_type>/<data_id>/new-comment", methods=['GET', 'POST'])
def add_new_comment(data_type, data_id):
    if request.method == "GET":
        if 'email' not in session:
            return redirect('/login')
        return render_template('modify_data_layout/add_new_comment.html', data_type=data_type, data_id=data_id)
    is_question = data_type == "question"
    if is_question:
        comment_manager.save_comment(data_id, is_question)
        data_manager.update_user_count('count_of_comments', session['email'], False)
        return redirect('/list')
    comment_manager.save_comment(data_id, is_question)
    data_manager.update_user_count('count_of_comments', session['email'], False)
    answer = comment_manager.get_question_id_from_answer(data_id)
    question_id = answer['question_id']
    return redirect('/question/' + str(question_id))


@add_data.route("/question/<int:question_id>/new-tag", methods=['GET', 'POST'])
def add_new_tag(question_id):
    if request.method == "POST":
        tag_name = request.form.get('message') if request.form.get("tag_list") == "" else request.form.get("tag_list")
        tag_list = tag_manager.get_question_tags()
        tag_id = get_tag_id(tag_list, tag_name)
        tag_manager.add_tag_to_question_id(question_id, tag_id)
        return redirect('/list')
    tags = tag_manager.get_tag_list()
    return render_template('modify_data_layout/add_tag.html', question_id=question_id, tags=tags)


def get_tag_id(tag_list, tag_name):
    if data_manager.check_for_id_duplicate(tag_list, 'name', tag_name):
        return tag_manager.get_tag_id_by_tag_name(tag_name)
    tag_manager.add_tag(tag_name)
    return tag_manager.get_tag_id()
