from flask import Flask, render_template, redirect, request, url_for
import data_manager, util
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images/'


@app.route("/add_question", methods=['GET', 'POST'])
def add_new_question():
    text_id = "question_input"
    name = "message"
    if request.method == "POST":
        question = data_manager.add_question_with_basic_headers()
        file = request.files['file']
        filename = file.filename
        if filename != '':
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            img_path = 'static/images/' + filename
            question['image'] = img_path
        question = data_manager.save_new_question(question)
        return redirect('/question/' + str(question['id']))
    return render_template('modify_data_layout/add_question.html', text_id=text_id, text_name=name)


@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def update_question(question_id):
    questions = data_manager.get_all_questions()
    question = data_manager.fetch_dictionary(question_id, questions)
    text_id = "question_input"
    name = "message"
    if request.method == "POST":
        data_manager.update_question(data_manager.QUESTIONS_FILE, questions, question_id)
        return redirect('/question/' + question_id)
    return render_template('modify_data_layout/update_question.html', text_id=text_id, text_name=name, question=question)


@app.route("/question/<data_id>/new_answer", methods=['GET', 'POST'])
def add_new_answer(data_id):
    text_id = "answer_input"
    name = "message"
    if request.method == "POST":
        answer = data_manager.add_answer_with_basic_headers(data_id)
        file = request.files['file']
        filename = file.filename
        if filename != '':
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            img_path = 'static/images/' + filename
            answer['image'] = img_path
        data_manager.save_new_answer(answer, data_id)
        return redirect('/question/' + data_id)
    return render_template('modify_data_layout/new_answer.html', text_id=text_id, text_name=name, data_id=data_id)


@app.route("/<data_type>/<data_id>/delete")
def delete(data_type, data_id):
    if data_type == 'question':
        filepath = data_manager.QUESTIONS_FILE
    else:
        filepath = data_manager.ANSWERS_FILE
        question_id = data_manager.get_question_id_for_answer(data_id)
    data_manager.delete_dictionary(filepath, data_id)
    if data_type == 'question':
        filepath = data_manager.ANSWERS_FILE
        data_manager.delete_related_answers(filepath, data_id)
        return redirect('/list')
    return redirect('/question/' + question_id)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/list')
def display_data():
    if request.args:
        sorting_key = request.args['sort_by']
        reverse_bool = request.args['order_descending']
        questions = data_manager.get_sorted_questions(sorting_key, reverse_bool)
    else:
        questions = data_manager.get_all_questions()
    question_headers = data_manager.QUESTION_HEADERS
    return render_template('display_data/list.html', questions=questions, question_headers=question_headers)


@app.route('/question/<question_id>')
def display_answers(question_id):
    answer_headers = data_manager.ANSWER_HEADER
    answer_details = data_manager.fetch_answers(question_id)
    question_details = data_manager.fetch_dictionary(question_id)
    data_manager.update_view_number(question_id)
    return render_template('display_data/list_answers.html', answer_details=answer_details,
                           question_details=question_details, answer_headers=answer_headers)


@app.route('/<library_type>/<datum_id>/<vote>')
def get_vote(library_type, datum_id, vote):
    table_type = 'question' if library_type == 'question' else 'answer'
    data_manager.update_votes(table_type, datum_id, vote)
    if table_type == 'answer':
        answers = data_manager.get_question_id_for_answer(datum_id)
        return redirect('/question/' + str(answers[0]['question_id']))
    return redirect('/list')


if __name__ == "__main__":
    app.run(debug=True)
