from flask import Flask, render_template, redirect, request
import data_manager


app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/add_question", methods=['GET', 'POST'])
def add_new_question():
    if request.method == "POST":
        return redirect('/')
    return render_template('add_question.html')


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
    return render_template('display_data/list_answers.html', answer_details=answer_details, question_details=question_details)


if __name__ == "__main__":
    app.run(debug=True)
