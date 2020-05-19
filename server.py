from flask import Flask, render_template, redirect, request
import data_manager

app = Flask(__name__)


@app.route("/add_question", methods=['GET', 'POST'])
def add_new_question():
    id = "question_input"
    name = "question"
    if request.method == "POST":
        return redirect('/')
    return render_template('modify_data_layout/add_question.html', text_id=id, text_name=name)\


@app.route("/update_question", methods=['GET', 'POST'])
def update_question():
    id = "question_input"
    name = "question"
    if request.method == "POST":
        return redirect('/')
    return render_template('modify_data_layout/update_question.html', text_id=id, text_name=name)


@app.route("/new_answer", methods=['GET', 'POST'])
def add_new_answer():
    id = "question_input"
    name = "question"
    if request.method == "POST":
        return redirect('/')
    return render_template('modify_data_layout/new_answer.html', text_id=id, text_name=name)


@app.route("/<data_type>/<data_id>/delete")
def delete(data_type, data_id):
    filepath = data_manager.QUESTIONS_FILE if data_type == 'question' else data_manager.ANSWERS_FILE
    data_manager.delete_dictionary(filepath, data_id)
    if data_type == 'question':
        return redirect('/')
    else:
        question_id = data_id
        return redirect('question/' + question_id)


@app.route("/")
@app.route('/list')
def display_data():
    questions = data_manager.get_all_questions()
    question_headers = data_manager.QUESTION_HEADERS
    return render_template('display_data/list.html', questions=questions, question_headers=question_headers)


@app.route('/question/<question_id>')
def display_answers(question_id):
    answers = data_manager.get_all_answers()
    questions = data_manager.get_all_questions()
    answer_details = data_manager.fetch_dictionary(question_id, answers)
    question_details = data_manager.fetch_dictionary(question_id, questions)
    return render_template('display_data/list_answers.html', answer_details=answer_details,
                           question_details=question_details)


if __name__ == "__main__":
    app.run(debug=True)
