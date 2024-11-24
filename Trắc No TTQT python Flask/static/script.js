let currentQuestions = [];
let currentQuestionIndex = 0;
let selectedOption = null;

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('start-btn').addEventListener('click', startQuiz);
    document.getElementById('check-btn').addEventListener('click', checkAnswer);
    document.getElementById('next-btn').addEventListener('click', showNextQuestion);
});

async function startQuiz() {
    const questionCount = document.getElementById('question-count').value;
    if (!questionCount || questionCount < 1) {
        alert('Please enter a valid number of questions');
        return;
    }

    try {
        console.log('Fetching questions...'); // Debug log
        const response = await fetch(`http://localhost:5000/get_questions?count=${questionCount}`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const questions = await response.json();
        console.log('Received questions:', questions); // Debug log

        if (!questions || questions.length === 0) {
            throw new Error('No questions received from server');
        }

        currentQuestions = questions;
        currentQuestionIndex = 0;
        
        // Update UI
        document.getElementById('start-screen').style.display = 'none';
        document.getElementById('quiz-container').style.display = 'block';
        
        showQuestion();
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to load questions: ' + error.message);
    }
}

function showQuestion() {
    if (!currentQuestions || currentQuestionIndex >= currentQuestions.length) {
        console.error('Invalid question data');
        return;
    }

    const question = currentQuestions[currentQuestionIndex];
    console.log('Current question:', question); // Debug log

    // Update question text
    document.getElementById('question-text').textContent = 
        `Question ${currentQuestionIndex + 1}/${currentQuestions.length}: ${question.question}`;
    
    // Clear and rebuild options
    const optionsContainer = document.getElementById('options-container');
    optionsContainer.innerHTML = '';
    
    Object.entries(question.options).forEach(([key, value]) => {
        const optionDiv = document.createElement('div');
        optionDiv.className = 'option';
        optionDiv.textContent = `${key.toUpperCase()}. ${value}`;
        optionDiv.dataset.option = key;
        optionDiv.addEventListener('click', () => selectOption(optionDiv));
        optionsContainer.appendChild(optionDiv);
    });
    
    // Reset UI states
    document.querySelectorAll('.option').forEach(opt => {
        opt.classList.remove('selected', 'correct', 'incorrect');
    });
    document.getElementById('check-btn').style.display = 'block';
    document.getElementById('next-btn').style.display = 'none';
    document.getElementById('result').textContent = '';
    selectedOption = null;
}

function selectOption(optionDiv) {
    document.querySelectorAll('.option').forEach(opt => {
        opt.classList.remove('selected');
    });
    optionDiv.classList.add('selected');
    selectedOption = optionDiv.dataset.option;
}

function checkAnswer() {
    if (!selectedOption) {
        alert('Please select an answer');
        return;
    }
    
    const question = currentQuestions[currentQuestionIndex];
    const isCorrect = selectedOption === question.correct_answer;
    
    // Show correct/incorrect answers
    document.querySelectorAll('.option').forEach(opt => {
        const optionKey = opt.dataset.option;
        if (optionKey === question.correct_answer) {
            opt.classList.add('correct');
        } else if (optionKey === selectedOption && !isCorrect) {
            opt.classList.add('incorrect');
        }
    });
    
    // Update UI
    document.getElementById('result').textContent = isCorrect ? 'Correct!' : 'Incorrect!';
    document.getElementById('check-btn').style.display = 'none';
    document.getElementById('next-btn').style.display = 'block';
}

function showNextQuestion() {
    currentQuestionIndex++;
    if (currentQuestionIndex < currentQuestions.length) {
        showQuestion();
    } else {
        alert('Quiz completed!');
        // Reset to start screen
        document.getElementById('quiz-container').style.display = 'none';
        document.getElementById('start-screen').style.display = 'block';
        currentQuestionIndex = 0;
        currentQuestions = [];
    }
}