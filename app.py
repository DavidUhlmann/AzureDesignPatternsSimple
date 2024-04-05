import webbrowser
from threading import Timer
from flask import Flask, request, render_template, session, redirect, url_for, jsonify
import random
import os
import time
from DesignPatternsGame import load_design_patterns

app = Flask(__name__)
app.secret_key = 'your_secret_key'

patterns_details = load_design_patterns()

@app.route('/')
def home():
    # Directly redirect users to the quiz setup page as I want to simplify
    return redirect(url_for('quiz'))

@app.route('/quiz')
def quiz():
    total_questions = len(patterns_details)
    return render_template('quiz.html', total_questions=total_questions)

@app.route('/start_quiz', methods=['POST'])
def start_quiz():
    num_questions = min(int(request.form.get('num_questions', 0)), len(patterns_details))
    session['question_indices'] = random.sample(range(len(patterns_details)), num_questions)
    session['current_question_index'] = 0
    session['correct_answers'] = 0
    session['patterns_to_review'] = []
    return redirect(url_for('question'))

@app.route('/question')
def question():
    index = session.get('current_question_index')
    if index is not None and index < len(session.get('question_indices', [])):
        question = patterns_details[session['question_indices'][index]]
        return render_template('question.html', question=question, question_num=index + 1, total_questions=len(session['question_indices']))
    return redirect(url_for('results'))

@app.route('/answer', methods=['POST'])
def answer():
    session['patterns_to_review'] = session.get('patterns_to_review', [])
    if request.form.get('answer') == 'no':
        session['patterns_to_review'].append(session['question_indices'][session['current_question_index']])
    else:
        session['correct_answers'] = session.get('correct_answers', 0) + 1
    session['current_question_index'] += 1
    return redirect(url_for('question') if session['current_question_index'] < len(session['question_indices']) else url_for('results'))

@app.route('/results')
def results():
    patterns_to_review = [patterns_details[i] for i in session.get('patterns_to_review', [])]
    return render_template('results.html', correct_answers=session.get('correct_answers', 0), total_questions=len(session.get('question_indices', [])), patterns_details=patterns_to_review)

@app.route('/reset_session', methods=['POST'])
def reset_session():
    session.clear()  # This clears the Flask session
    return jsonify(success=True)  # Respond with success

@app.route('/restart')
def restart_quiz():
    session.clear()  # Ensure the session is cleared
    return redirect(url_for('home'))  # Redirect to the quiz start or setup page

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == '__main__':
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        Timer(1, open_browser).start()
    app.run(host='0.0.0.0', debug=True)