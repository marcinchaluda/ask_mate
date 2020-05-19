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
    return render_template('modify_data_layout/add_question.html')


@app.route("/<data_type>/<data_id>/delete")
def delete(data_type, data_id):
    data_manager.delete_dictionary(data_type + '.csv', data_id)
    if data_type == 'question':
        redirect('/')
    else:
        question_id = request.args.get('question_id')
        redirect('question/' + question_id)



if __name__ == "__main__":
    app.run(debug=True)
