import PyPDF2

question = []
def extract_questions(file_path):
    # Mở file PDF
    pdf_file = open(file_path, 'rb')
    # Tạo đối tượng PDF reader
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    
    var = []
    found_question = False
    in_question_section = False
    correct_answer = None
    correct_answer_text = None

    # Duyệt qua từng trang trong file PDF
    for page in pdf_reader.pages:
        # Lấy text từ trang
        text = page.extract_text()
        # Tách text thành các dòng
        lines = text.split('\n')
        
        # Xử lý từng dòng
        for line in lines:
            if "Câu" in line:
                # Nếu đã tìm thấy câu hỏi trước đó
                if found_question:
                    if correct_answer:
                        var.append(correct_answer_text)
                        var.append(correct_answer)
                    question.append(var)
                    var = []
                    correct_answer = None
                    correct_answer_text = None
                var.append(line)
                found_question = True
                in_question_section = True
            elif found_question:
                if "Câu" in line:
                    in_question_section = False
                if in_question_section:
                    if "(Đáp án đúng)" in line:
                        correct_answer = line.replace("(Đáp án đúng)", "").strip()
                        correct_answer_text = line.strip()
                    var.append(line)
                
    # Xử lý câu hỏi cuối cùng
    if var:
        if correct_answer:
            var.append(correct_answer_text)
            var.append(correct_answer)
        question.append(var)
    # Xóa "(Đáp án đúng)" khỏi tất cả các phần tử trong question
    for i in range(len(question)):
        for j in range(len(question[i])):
            question[i][j] = question[i][j].replace("(Đáp án đúng)", "").strip()
    
    # Đóng file PDF
    pdf_file.close()
        
    return question

def extract_process(questions):
    only_question = []
    only_answers = []
    description = []
    correct_answers = []
    
    for question_group in questions:
        # Lấy đáp án đúng từ phần tử cuối
        correct_answer = question_group[-1]
        correct_answers.append(correct_answer)
        
        # Tìm vị trí của đáp án A đầu tiên
        a_index = -1
        for i, line in enumerate(question_group[:-2]):  # Bỏ qua 2 phần tử cuối
            if line.strip().startswith('A.'):
                a_index = i
                break
                
        # Gộp tất cả các dòng trước đáp án A thành câu hỏi
        question_text = ' '.join(question_group[:a_index]).strip()
        answers = [''] * 4  # Khởi tạo list chứa 4 đáp án ABCD
        desc = ""
        
        # Tìm các đáp án và xử lý đáp án nhiều dòng
        for i, line in enumerate(question_group[1:-2]):  # Bỏ qua 2 phần tử cuối
            line = line.strip()
            if line.startswith('A.'):
                # Lấy tất cả dòng từ A đến B
                a_text = [line]
                for next_line in question_group[i+2:-2]:
                    if next_line.strip().startswith('B.'):
                        break
                    a_text.append(next_line.strip())
                answers[0] = ' '.join(a_text)
            
            elif line.startswith('B.'):
                # Lấy tất cả dòng từ B đến C
                b_text = [line]
                for next_line in question_group[i+2:-2]:
                    if next_line.strip().startswith('C.'):
                        break
                    b_text.append(next_line.strip())
                answers[1] = ' '.join(b_text)
                
            elif line.startswith('C.'):
                # Lấy tất cả dòng từ C đến D
                c_text = [line]
                for next_line in question_group[i+2:-2]:
                    if next_line.strip().startswith('D.'):
                        break
                    c_text.append(next_line.strip())
                answers[2] = ' '.join(c_text)
                
            elif line.startswith('D.'):
                # Lấy tất cả dòng từ D đến hết phần đáp án
                d_text = [line]
                for next_line in question_group[i+2:-2]:
                    if next_line.strip().startswith('Giải thích:'):
                        break
                    d_text.append(next_line.strip())
                answers[3] = ' '.join(d_text)
            else:
                desc += line.strip() + " "
        
        # Thêm vào các list tương ứng
        only_question.append(question_text)
        only_answers.append(answers)
        
        # Tìm phần giải thích trong câu hỏi
        desc = "Giải thích: "  # Giá trị mặc định
        found_explanation = False
        explanation_start = -1
        
        # Tìm vị trí bắt đầu của phần giải thích
        for i, line in enumerate(question_group[:-2]):  # Bỏ qua 2 phần tử cuối
            if line.strip().startswith('Giải thích:'):
                found_explanation = True
                explanation_start = i
                break
                
        if found_explanation:
            # Lấy toàn bộ phần giải thích từ vị trí tìm thấy đến phần tử cuối
            explanation_lines = question_group[explanation_start:-2]
            desc = ' '.join(line.strip() for line in explanation_lines)
            
        description.append(desc.strip())
    
    return only_answers, only_question, description, correct_answers

file_path = "trac-nghiem-e-markrting.pdf"
questions = extract_questions(file_path)
only_answers, only_question, description, correct_answers = extract_process(questions)

with open('bocauhoi.txt', 'w', encoding='utf-8') as f:
    for i in range(len(only_question)):
        f.write(only_question[i] + '\n')
        f.write(str(only_answers[i]) + '\n')
        f.write(f"Đáp án đúng: {correct_answers[i]}\n")
        f.write(description[i] + '\n')
        f.write("_" * 200 + '\n')
