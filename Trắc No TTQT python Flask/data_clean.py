import fitz
import re
import os

def extract_questions(pdf_path):
    doc = fitz.open(pdf_path)
    questions = []
    current_question = None
    is_question_part = False

    for page_num, page in enumerate(doc):
        # Chuyển generator thành list
        annotations = list(page.annots())
        print(f"Trang {page_num + 1}: {len(annotations)} annotations")
        
        text = page.get_text()
        lines = text.split("\n")

        highlights = []
        try:
            for annot in annotations:  # Sử dụng list annotations
                if annot.type[0] == 8:
                    quad_points = annot.vertices
                    quad_count = int(len(quad_points) / 4)
                    highlight_text = ""
                    for i in range(quad_count):
                        quad = quad_points[i * 4:(i + 1) * 4]
                        rect = fitz.Quad(quad).rect
                        highlight_text += page.get_textbox(rect).replace('\n', ' ')
                    highlights.append(highlight_text.strip())
                    print(f"Highlight found: {highlight_text.strip()}")
        except Exception as e:
            print(f"Lỗi khi xử lý annotations: {e}")

        for line in lines:
            line = line.strip()
            if re.match(r"^Question \d+/\d+", line):
                if current_question:
                    questions.append(current_question)
                current_question = {"question": line, "options": [], "answer": None}
                is_question_part = True
            elif re.match(r"^[ABCD]\.", line) and current_question:
                is_question_part = False
                current_question["options"].append(line)
                option_content = line[3:].strip()
                if any(option_content in hl for hl in highlights):
                    current_question["answer"] = line
                    print(f"Found answer: {line}")

    if current_question:
        questions.append(current_question)

    return questions

def main():
    # Sử dụng đường dẫn tuyệt đối hoặc tương đối chính xác
    current_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_path = os.path.join(current_dir, 'thanh-toan-quoc-te-nhom-2-questions.pdf')
    output_file = os.path.join(current_dir, 'output.txt')

    try:
        questions = extract_questions(pdf_path)
        
        # Ghi kết quả với xử lý ngoại lệ
        with open(output_file, 'w', encoding='utf-8') as f:
            for idx, q in enumerate(questions, 1):
                f.write(f"Câu hỏi:\n")
                f.write(f"{q['question']}\n")
                f.write(f"Phương án:\n")
                for opt in q['options']:
                    f.write(f"{opt}\n")
                if q['answer']:
                    f.write(f"Đáp án đúng:\n{q['answer']}\n")
                else:
                    f.write("Đáp án đúng:\nChưa xác định\n")
                f.write('--------------------------------------------------\n')

        print(f"Đã lưu {len(questions)} câu hỏi vào tệp '{output_file}'")
        
    except Exception as e:
        print(f"Lỗi: {e}")

if __name__ == '__main__':
    main()