from flask import Flask, render_template, redirect, request, Blueprint
import data_manager
import os
update_data = Blueprint('update_data', __name__)
NUMBER_OF_LATEST_QUESTIONS = 5


@update_data.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def update_question(question_id):
    question = data_manager.fetch_dictionary(question_id)[0]
    if request.method == "POST":
        data_manager.update_question(question_id)
        return redirect('/question/' + question_id)
    return render_template('modify_data_layout/update_question.html', question=question)


@update_data.route('/comment/<comment_id>/edit', methods=['GET', 'POST'])
def update_comment(comment_id):
    comment = data_manager.fetch_comments_by_id(comment_id)
    if request.method == "POST":
        data_manager.update_comment(comment)
        if comment['question_id']:
            return redirect('/list')
        else:
            answer = data_manager.fetch_answers_by_answer_id(comment['answer_id'])
            return redirect('/question/' + str(answer['question_id']))
    return render_template('modify_data_layout/update_comment.html', comment=comment)
