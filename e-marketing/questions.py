import re

def load_questions(filename):
    questions = []
    current_question = {}
    
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for line in lines:
        line = line.strip()
        
        if line.startswith('Câu'):
            if current_question:
                questions.append(current_question)
            current_question = {
                'id': len(questions),
                'question': line.split(':', 1)[1].strip(),
                'options': [],
                'correct_answer': '',
                'explanation': ''
            }
        elif line.startswith('['):
            options = eval(line)
            current_question['options'] = options
        elif line.startswith('Đáp án đúng:'):
            current_question['correct_answer'] = line.split(':', 1)[1].strip()
        elif line.startswith('Giải thích:'):
            current_question['explanation'] = line.split(':', 1)[1].strip()
            
    if current_question:
        questions.append(current_question)
        
    return questions 