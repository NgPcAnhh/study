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
        # Get the path to questions_output.txt relative to server.py
        current_dir = os.path.dirname(os.path.abspath(__file__))
        questions_file = os.path.join(current_dir, 'questions_output.txt')
        
        all_questions = parse_questions(questions_file)
        if not all_questions:
            return jsonify({"error": "No questions found"}), 404
            
        max_questions = len(all_questions)
        if count > max_questions:
            count = max_questions
            
        selected_questions = random.sample(all_questions, count)
        return jsonify(selected_questions)
        
    except Exception as e:
        print(f"Error: {str(e)}")  # Server-side logging
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)