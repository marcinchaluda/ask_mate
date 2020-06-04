from flask import Flask, render_template, redirect, request, Blueprint
import data_manager
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


@add_data.route("/question/<question_id>/new-tag", methods=['GET', 'POST'])
def add_new_tag(question_id):
    if request.method == "POST":
        tag_name = request.form.get('text_id')
        data_manager.add_tag(tag_name, question_id)
        return redirect('/list')
    return render_template('modify_data_layout/add_tag.html')
