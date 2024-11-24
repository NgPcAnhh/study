import random

def parse_questions(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()

    questions = []
    parts = content.strip().split('--------------------------------------------------')
    for part in parts:
        lines = [line.strip() for line in part.strip().split('\n') if line.strip()]
        if len(lines) < 6:
            continue
        try:
            # Bỏ qua dòng 'Câu hỏi:'
            if lines[0] == 'Câu hỏi:':
                question_line = lines[1]
            else:
                question_line = lines[0]

            # Lấy các phương án trả lời
            options_index = lines.index('Phương án:') + 1
            options = {}
            for i in range(options_index, options_index + 4):
                option_line = lines[i]
                key = option_line[0].lower()
                value = option_line[3:].strip()
                options[key] = value

            # Lấy đáp án đúng
            correct_line = lines[lines.index('Đáp án đúng:') + 1]
            correct_answer = correct_line[0].lower()

            questions.append({
                'question': question_line,
                'options': options,
                'correct_answer': correct_answer
            })
        except ValueError:
            continue
    return questions

def main():
    questions = parse_questions('questions_output.txt')
    total_questions = len(questions)
    num_questions = int(input(f'Nhập số câu hỏi muốn kiểm tra (1-{total_questions}): '))
    selected_questions = random.sample(questions, num_questions)
    random.shuffle(selected_questions)

    for idx, q in enumerate(selected_questions, 1):
        print(f"Câu hỏi {idx}: {q['question']}")
        for key in sorted(q['options'].keys()):
            print(f"{key.upper()}. {q['options'][key]}")
        answer = input('Câu trả lời của bạn (A, B, C, D): ').lower()
        if answer == q['correct_answer']:
            print('Bạn đã trả lời đúng!')
        else:
            correct_option = q['correct_answer'].upper()
            print(f"Sai rồi! Đáp án đúng là: {correct_option}. {q['options'][q['correct_answer']]}")
        print('--------------------------------------------------')
    print('Bạn đã hoàn thành bài kiểm tra.')

if __name__ == '__main__':
    main()