let score = 0;
let answeredQuestions = new Set();

function checkAnswer(questionId) {
    const selectedOption = document.querySelector(`input[name="q${questionId}"]:checked`);
    if (!selectedOption) {
        alert('Vui lòng chọn một đáp án!');
        return;
    }

    fetch('/check_answer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            question_id: questionId,
            selected_answer: selectedOption.value
        })
    })
    .then(response => response.json())
    .then(data => {
        const feedback = document.querySelector(`#question-${questionId} .feedback`);
        const result = feedback.querySelector('.result');
        const explanation = feedback.querySelector('.explanation');
        
        feedback.style.display = 'block';
        feedback.className = `feedback ${data.correct ? 'correct' : 'incorrect'}`;
        
        result.textContent = data.correct ? 'Đúng!' : 'Sai! Đáp án đúng là: ' + data.correct_answer;
        explanation.textContent = data.explanation;
        
        if (data.correct && !answeredQuestions.has(questionId)) {
            score++;
            document.getElementById('score').textContent = score;
        }
        
        answeredQuestions.add(questionId);
        document.querySelector(`#question-${questionId} .check-btn`).style.display = 'none';
        document.querySelector(`#question-${questionId} .next-btn`).style.display = 'inline-block';
        
        // Cập nhật trạng thái nút điều hướng
        updateNavigationButton(questionId);
    });
}

function nextQuestion(currentId) {
    const currentQuestion = document.getElementById(`question-${currentId}`);
    const nextQuestion = currentQuestion.nextElementSibling;
    
    if (nextQuestion && nextQuestion.classList.contains('question-card')) {
        currentQuestion.style.display = 'none';
        nextQuestion.style.display = 'block';
        updateNavigationButton(parseInt(nextQuestion.id.split('-')[1]));
    }
}

function jumpToQuestion(questionId) {
    document.querySelectorAll('.question-card').forEach(card => {
        card.style.display = 'none';
    });
    document.getElementById(`question-${questionId}`).style.display = 'block';
    updateNavigationButton(questionId);
}

function updateNavigationButton(currentQuestionId) {
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('current');
    });
    
    const navBtn = document.querySelector(`.nav-btn:nth-child(${currentQuestionId + 1})`);
    if (answeredQuestions.has(currentQuestionId)) {
        navBtn.classList.add('answered');
    }
    navBtn.classList.add('current');
} 