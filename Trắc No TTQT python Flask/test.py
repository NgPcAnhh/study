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
            # Lấy câu hỏi
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
            correct_index = lines.index('Đáp án đúng:') + 1
            correct_answer = lines[correct_index][0].lower()

            # Lấy toàn bộ phần description từ "Đáp án đúng" đến hết
            description = ' '.join(lines[correct_index:]).strip()

            questions.append({
                'question': question_line,
                'options': options,
                'correct_answer': correct_answer,
                'description': description
            })
        except ValueError:
            continue
    return questions

def main():
    questions = parse_questions('questions_output.txt')
    total_questions = len(questions)
    answered_questions = []

    num_questions = int(input(f'Nhập số câu hỏi muốn kiểm tra (1-{total_questions}): '))
    selected_questions = random.sample(questions, num_questions)

    for idx, q in enumerate(selected_questions, 1):
        print(f"Câu hỏi {idx}: {q['question']}")
        for key in sorted(q['options'].keys()):
            print(f"{key.upper()}. {q['options'][key]}")

        while True:
            answer = input('Câu trả lời của bạn (A, B, C, D hoặc Nhấn Enter để bỏ qua): ').lower()
            if answer in ['a', 'b', 'c', 'd', '']:
                break
            print('Vui lòng nhập A, B, C, D hoặc Enter để bỏ qua.')

        if answer:
            is_correct = answer == q['correct_answer']
            result_text = 'Bạn đã trả lời đúng!' if is_correct else f'Sai rồi! Đáp án đúng là: {q["correct_answer"].upper()}'
            print(result_text)
            print(f"Giải thích đầy đủ: {q['description']}")
            answered_questions.append({
                'question': q['question'],
                'your_answer': answer,
                'correct_answer': q['correct_answer'],
                'description': q['description'],
                'is_correct': is_correct
            })
        else:
            print('Bạn đã bỏ qua câu hỏi này.')
            print(f"Giải thích đầy đủ: {q['description']}")

        print('--------------------------------------------------')

    print('Bạn đã hoàn thành bài kiểm tra.')
    while True:
        review = input('Bạn có muốn xem lại các câu đã trả lời không? (Y/N): ').lower()
        if review == 'y':
            print('Kết quả trả lời:')
            for idx, q in enumerate(answered_questions, 1):
                status = 'Đúng' if q['is_correct'] else 'Sai'
                print(f"{idx}. {q['question']}\n   Trạng thái: {status}")
                print(f"   Đáp án của bạn: {q['your_answer']} - Đáp án đúng: {q['correct_answer'].upper()}")
                print(f"   Giải thích đầy đủ: {q['description']}")
                print('--------------------------------------------------')
            break
        elif review == 'n':
            print('Cảm ơn bạn đã tham gia!')
            break
        else:
            print('Vui lòng nhập Y (Có) hoặc N (Không).')

if __name__ == '__main__':
    main()
