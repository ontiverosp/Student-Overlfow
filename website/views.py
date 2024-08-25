from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Question, Answer
from . import db
import json

views = Blueprint("views", __name__)

@views.route('/')
@login_required
def home():
    questions = Question.query.all()
    return render_template("home.html", user=current_user, questions = questions)

@views.route('/my-questions')
@login_required
def myQuestions():
    return render_template("my_questions.html", user=current_user)

@views.route('question/<int:question_id>/', methods=['GET', 'POST'])
@login_required
def question(question_id):
    if request.method == 'POST': 
        answer = request.form.get('answer')

        if len(answer) < 1:
            flash('Answer is too short!', category='error') 
        else:
            new_asnwer = Answer(answer = answer, user_id=current_user.id, question_id=question_id)  
            db.session.add(new_asnwer)  
            db.session.commit()
            flash('Question answered!', category='success')

    answers = Answer.query.filter_by(question_id=question_id).all()
    question = Question.query.get_or_404(question_id)
    return render_template('question.html', user=current_user, question=question, answers = answers)

@views.route('edit/<int:question_id>/', methods=['GET', 'POST'])
@login_required
def edit(question_id):
    question = Question.query.get_or_404(question_id)
    if request.method == 'POST': 
        new_question = request.form.get('question')
        new_data = request.form.get('data')
        if len(new_question) < 1:
            flash('Question is too short!', category='error') 
        else:
            
            if question:
                if question.user_id == current_user.id:
                    question.question = new_question
                    question.data = new_data
                    db.session.commit()
                    flash('Question Edited!', category='success')
                    return redirect(url_for('views.myQuestions'))

    return render_template('edit.html', user=current_user, question=question)



@views.route('/ask', methods=['GET', 'POST'])
@login_required
def ask():
    if request.method == 'POST': 
        question = request.form.get('question')
        data = request.form.get('data')

        if len(question) < 1:
            flash('Question is too short!', category='error') 
        else:
            new_question = Question(data=data, question = question, user_id=current_user.id)  
            db.session.add(new_question)  
            db.session.commit()
            flash('Question added!', category='success')
    return render_template("ask.html", user=current_user)

@views.route('/delete-question', methods=['POST'])
def delete_question():  
    question = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    questionId = question['questionId']
    question = Question.query.get(questionId)
    if question:
        if question.user_id == current_user.id:
            Answer.query.filter_by(question_id=questionId).delete()
            db.session.delete(question)
            db.session.commit()

    return jsonify({})