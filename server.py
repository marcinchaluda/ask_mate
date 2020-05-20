from flask import Flask, render_template, redirect, request, url_for
import data_manager

app = Flask(__name__)


@app.route("/add_question", methods=['GET', 'POST'])
def add_new_question():
    text_id = "question_input"
    name = "message"
    if request.method == "POST":
        question = data_manager.add_question_with_basic_headers()
        data_manager.save_new_question(question)
        return redirect('/question/' + question['id'])
    return render_template('modify_data_layout/add_question.html', text_id=text_id, text_name=name)


@app.route("/update_question", methods=['GET', 'POST'])
def update_question():
    id = "question_input"
    name = "question"
    if request.method == "POST":
        return redirect('/')
    return render_template('modify_data_layout/update_question.html', text_id=id, text_name=name)


@app.route("/question/<data_id>/new_answer", methods=['GET', 'POST'])
def add_new_answer(data_id):
    text_id = "answer_input"
    name = "message"
    if request.method == "POST":
        answer = data_manager.add_answer_with_basic_headers(data_id)
        data_manager.save_new_answer(answer)
        return redirect('/question/' + data_id)
    return render_template('modify_data_layout/new_answer.html', text_id=text_id, text_name=name, data_id=data_id)


@app.route("/<data_type>/<data_id>/delete")
def delete(data_type, data_id):
    filepath = data_manager.QUESTIONS_FILE if data_type == 'question' else data_manager.ANSWERS_FILE
    data_manager.delete_dictionary(filepath, data_id)
    if data_type == 'question':
        filepath = data_manager.ANSWERS_FILE
        data_manager.delete_related_answers(filepath, data_id)
        return redirect('/list')
    return redirect('/question/' + data_id)


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
    questions = data_manager.get_all_questions()
    answer_details = data_manager.fetch_answers(question_id)
    question_details = data_manager.fetch_dictionary(question_id, questions)
    question_details['view_number'] = int(question_details['view_number']) + 1
    data_manager.update_dictionary(data_manager.QUESTIONS_FILE, questions, "view_number")
    return render_template('display_data/list_answers.html', answer_details=answer_details,
                           question_details=question_details)


@app.route('/question/<question_id>/vote_up')
def vote_up(question_id):
    questions = data_manager.get_all_questions()
    question_details = data_manager.fetch_dictionary(question_id, questions)
    question_details['vote_number'] = int(question_details['vote_number']) + 1
    data_manager.update_dictionary(data_manager.QUESTIONS_FILE, questions, "vote_number")
    return redirect('/list')


@app.route("/question/<question_id>/vote_down")
def vote_down(question_id):
    questions = data_manager.get_all_questions()
    question_details = data_manager.fetch_dictionary(question_id, questions)
    question_details['vote_number'] = int(question_details['vote_number']) - 1
    data_manager.update_dictionary(data_manager.QUESTIONS_FILE, questions, "vote_number", True)
    return redirect('/list')


if __name__ == "__main__":
    app.run(debug=True)
