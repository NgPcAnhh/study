def process_quiz_data(file_path, answers_path):
    # Đọc file đáp án đúng
    with open(answers_path, "r", encoding="utf-8") as file:
        correct_answers_data = file.read()

    # Xử lý dữ liệu đáp án đúng
    correct_answers = {}
    answer_blocks = correct_answers_data.strip().split("\n\n")
    for block in answer_blocks:
        lines = block.split("\n")
        question_key = lines[0].split(":")[0]  # Lấy phần "Câu X"
        correct_answer = lines[1]  # Lấy dòng chứa đáp án đúng
        correct_answers[question_key] = correct_answer

    # Đọc file câu hỏi
    with open(file_path, "r", encoding="utf-8") as file:
        data = file.read()

    # Tách các câu hỏi
    questions = data.strip().split("\n\n")

    # Xử lý từng câu hỏi
    output = []
    for question in questions:
        lines = question.split("\n")
        question_text = lines[0]  # Dòng đầu là câu hỏi
        answers = lines[1:]       # Các dòng sau là đáp án

        # Xác định đáp án đúng từ correct_answers
        correct_answer = correct_answers.get(question_text.split(":")[0], "")

        # Gộp câu hỏi và đáp án đúng
        output.append(f"{question}\n\u0110ÁP ÁN ĐÚNG: {correct_answer}\n")

    # Xuất dữ liệu
    final_output = "\n".join(output)
    print(final_output)

# Đường dẫn tới file lsd.txt và file đáp án
file_path = "lsd.txt"
answers_path = "dapan.txt"
process_quiz_data(file_path, answers_path)
