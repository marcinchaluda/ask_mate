from flask import render_template, redirect, request, Blueprint
import model.data_manager as data_manager
import model.question_manager as question_manager
import model.comment_manager as comment_manager
update_data = Blueprint('update_data', __name__)
NUMBER_OF_LATEST_QUESTIONS = 5


@update_data.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def update_question(question_id):
    question = data_manager.fetch_data(question_id, 'question')[0]
    if request.method == "POST":
        question_manager.update_question(question_id)
        return redirect('/question/' + question_id)
    return render_template('modify_data_layout/update_question.html', question=question)


@update_data.route('/comment/<comment_id>/edit', methods=['GET', 'POST'])
def update_comment(comment_id):
    comment = data_manager.fetch_data(comment_id, 'comment')[0]
    if request.method == "POST":
        comment_manager.update_comment(comment)
        if comment['question_id']:
            return redirect('/list')
        else:
            answer = data_manager.fetch_data(comment['answer_id'], 'answer')
            return redirect('/question/' + str(answer['question_id']))
    return render_template('modify_data_layout/update_comment.html', comment=comment)
