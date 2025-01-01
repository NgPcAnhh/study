import random

def load_questions(filename):
    """Load questions and answers from the file."""
    with open(filename, encoding="utf-8") as file:
        content = file.read()

    questions = []
    blocks = content.split("\n\n")  # Split by blank lines
    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) >= 2:
            question_text = "\n".join(lines[:-1])
            if "ĐÁP ÁN ĐÚNG:" in block:
                correct_answer = block.split("ĐÁP ÁN ĐÚNG:", 1)[1].split("__", 1)[0].strip()
            elif "ĐÁP ÁN:" in block:
                correct_answer = block.split("ĐÁP ÁN:", 1)[1].split("__", 1)[0].strip()
            else:
                correct_answer = "Không xác định"
            questions.append((question_text, correct_answer))
    return questions

def quiz(questions, num_questions):
    """Run the quiz with random questions."""
    if num_questions.lower() == "all":
        num_questions = len(questions)
    else:
        num_questions = min(len(questions), int(num_questions))

    selected_questions = random.sample(questions, num_questions)
    score = 0

    for i, (question, correct_answer) in enumerate(selected_questions, start=1):
        print(f"\nCâu {i}: {question}")
        user_answer = input("Nhập đáp án của bạn (A/B/C/D): ").strip().upper()
        if user_answer == correct_answer[0].upper():
            print("ĐÚNG!")
            score += 1
        else:
            print("SAI!")
        print(f"ĐÁP ÁN ĐÚNG: {correct_answer}")

    print(f"\nBạn trả lời đúng {score}/{num_questions} câu.")

if __name__ == "__main__":
    filename = "bocauhoi.txt"
    questions = load_questions(filename)

    print("Chào mừng bạn đến với bài kiểm tra kiến thức!")
    num_questions = input("Bạn muốn kiểm tra bao nhiêu câu hỏi? (nhập số hoặc 'all' để kiểm tra toàn bộ): ")

    quiz(questions, num_questions)