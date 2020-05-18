from flask import Flask, render_template, redirect, request

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/add_question", methods=['GET', 'POST'])
def add_new_question():
    if request.method == "POST":
        return redirect('/')
    return render_template('add_question.html')


if __name__ == "__main__":
    app.run(debug=True)
