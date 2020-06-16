from flask import render_template, redirect, request, Blueprint
import model.data_manager as data_manager
import os
add_data = Blueprint('add_data', __name__)
UPLOAD_FOLDER = 'static/images/'


@add_data.route("/add_question", methods=['GET', 'POST'])
def add_new_question():
    if request.method == "POST":
        question = data_manager.add_question_with_basic_headers()
        file = request.files['file']
        filename = file.filename
        if filename != '':
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            img_path = 'static/images/' + filename
            question['image'] = img_path
        question_id = data_manager.save_new_question(question)
        return redirect('/question/' + str(question_id))
    return render_template('modify_data_layout/add_question.html')


@add_data.route("/question/<data_id>/new_answer", methods=['GET', 'POST'])
def add_new_answer(data_id):
    if request.method == "POST":
        answer = data_manager.add_answer_with_basic_headers(data_id)
        file = request.files['file']
        filename = file.filename
        if filename != '':
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            img_path = 'static/images/' + filename
            answer['image'] = img_path
        data_manager.save_new_answer(answer, data_id)
        return redirect('/question/' + data_id)
    return render_template('modify_data_layout/new_answer.html', data_id=data_id)


@add_data.route("/<data_type>/<data_id>/new-comment", methods=['GET', 'POST'])
def add_new_comment(data_type, data_id):
    if request.method == "POST":
        is_question = data_type == "question"
        if is_question:
            data_manager.save_comment(data_id, is_question)
            return redirect('/list')
        else:
            data_manager.save_comment(data_id, is_question)
            answer = data_manager.fetch_answers_by_answer_id(data_id)
            question_id = answer['question_id']
            return redirect('/question/' + str(question_id))
    return render_template('modify_data_layout/add_new_comment.html', data_type=data_type, data_id=data_id)


@add_data.route("/question/<int:question_id>/new-tag", methods=['GET', 'POST'])
def add_new_tag(question_id):
    if request.method == "POST":
        if request.form.get("tag_list") == "":
            tag_name = request.form.get('message')
        else:
            tag_name = request.form.get("tag_list")
        tag_list = data_manager.get_question_tags()
        tag_id = get_tag_id(tag_list, tag_name)
        data_manager.add_tag_to_question_id(question_id, tag_id)
        return redirect('/list')
    tags = data_manager.get_tag_list()
    print(tags)
    return render_template('modify_data_layout/add_tag.html', question_id=question_id, tags=tags)


def get_tag_id(tag_list, tag_name):
    if not data_manager.check_for_id_duplicate(tag_list, 'name', tag_name):
        data_manager.add_tag(tag_name)
        return data_manager.get_tag_id()
    return data_manager.get_tag_id_by_tag_name(tag_name)
