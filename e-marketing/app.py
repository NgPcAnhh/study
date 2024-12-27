from flask import Flask, render_template, request, jsonify
import random
from questions import load_questions

app = Flask(__name__)

questions = load_questions('bocauhoi.txt')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/quiz', methods=['POST'])
def quiz():
    num_questions = request.form.get('num_questions')
    if num_questions.lower() == 'all':
        selected_questions = questions.copy()
        random.shuffle(selected_questions)
    else:
        try:
            num = int(num_questions)
            if num <= 0:
                return "Số câu hỏi phải lớn hơn 0", 400
            if num > len(questions):
                return f"Số câu hỏi không được vượt quá {len(questions)}", 400
                
            selected_questions = random.sample(questions, num)
            
        except ValueError:
            return "Số câu hỏi không hợp lệ", 400
            
    return render_template('quiz.html', questions=selected_questions)

@app.route('/check_answer', methods=['POST'])
def check_answer():
    data = request.get_json()
    question_id = data.get('question_id')
    selected_answer = data.get('selected_answer')
    
    question = next((q for q in questions if q['id'] == question_id), None)
    if question:
        is_correct = selected_answer == question['correct_answer']
        return jsonify({
            'correct': is_correct,
            'correct_answer': question['correct_answer'],
            'explanation': question['explanation'],
            'status': 'correct' if is_correct else 'incorrect'
        })
    return jsonify({'error': 'Question not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)