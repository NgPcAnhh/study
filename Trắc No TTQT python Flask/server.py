from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from test import parse_questions
import random
import os

app = Flask(__name__, static_url_path='', static_folder='static')
CORS(app)

@app.route('/')
def home():
    return send_from_directory('static', 'index.html')

@app.route('/get_questions', methods=['GET'])
def get_questions():
    try:
        count = int(request.args.get('count', 1))
        current_dir = os.path.dirname(os.path.abspath(__file__))
        questions_file = os.path.join(current_dir, 'questions_output.txt')
        
        all_questions = parse_questions(questions_file)
        if not all_questions:
            return jsonify({"error": "No questions found"}), 404

        max_questions = min(len(all_questions), 94)  # Giới hạn tối đa 94 câu hỏi
        count = min(count, max_questions)

        selected_questions = random.sample(all_questions, count)  # Chọn câu hỏi không lặp
        for idx, question in enumerate(selected_questions):
            question['id'] = idx + 1  # Gán ID cho từng câu hỏi
        
        return jsonify(selected_questions)
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    try:
        data = request.get_json()
        question_id = data.get('question_id')
        selected_option = data.get('selected_option')

        current_dir = os.path.dirname(os.path.abspath(__file__))
        questions_file = os.path.join(current_dir, 'questions_output.txt')
        all_questions = parse_questions(questions_file)

        question = next((q for q in all_questions if q.get('id') == question_id), None)
        if not question:
            return jsonify({"error": "Question not found"}), 404

        # Check the answer
        is_correct = selected_option.strip().lower() == question['correct_answer'].strip().lower()

        # Return the result with full answer details
        return jsonify({
            'is_correct': is_correct,
            'correct_answer': question['correct_answer'],
            'description': question['description']
        })

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

    try:
        data = request.get_json()
        question_id = data.get('question_id')
        selected_option = data.get('selected_option')

        current_dir = os.path.dirname(os.path.abspath(__file__))
        questions_file = os.path.join(current_dir, 'questions_output.txt')
        all_questions = parse_questions(questions_file)

        question = next((q for q in all_questions if q.get('id') == question_id), None)
        if not question:
            return jsonify({"error": "Question not found"}), 404

        # Check the answer
        is_correct = selected_option.strip().lower() == question['correct_answer'].strip().lower()

        # Return the result with full answer details
        return jsonify({
            'is_correct': is_correct,
            'correct_answer': question['correct_answer'],
            'description': question['description']
        })

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

    try:
        data = request.get_json()
        question_id = data.get('question_id')
        selected_option = data.get('selected_option')

        current_dir = os.path.dirname(os.path.abspath(__file__))
        questions_file = os.path.join(current_dir, 'questions_output.txt')
        all_questions = parse_questions(questions_file)

        question = next((q for q in all_questions if q.get('id') == question_id), None)
        if not question:
            return jsonify({"error": "Question not found"}), 404

        # Check the answer
        is_correct = selected_option.strip().lower() == question['correct_answer'].strip().lower()

        # Return the result with full answer details
        return jsonify({
            'is_correct': is_correct,
            'correct_answer': question['correct_answer'],
            'description': question['description']
        })

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/review_answers', methods=['POST'])
def review_answers():
    try:
        answered_questions = request.get_json()  # Client gửi danh sách câu đã làm
        if not answered_questions:
            return jsonify({"error": "No answers to review"}), 400

        current_dir = os.path.dirname(os.path.abspath(__file__))
        questions_file = os.path.join(current_dir, 'questions_output.txt')
        all_questions = parse_questions(questions_file)

        # Map answers to full question details
        results = []
        for answer in answered_questions:
            question = next((q for q in all_questions if q.get('id') == answer['question_id']), None)
            if question:
                results.append({
                    'question': question['question'],
                    'your_answer': answer.get('selected_option'),
                    'correct_answer': question['correct_answer'],
                    'description': question['description'],
                    'is_correct': answer.get('selected_option') == question['correct_answer']
                })

        return jsonify(results)

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
