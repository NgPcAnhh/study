let currentQuestions = [];
let currentQuestionIndex = 0;
let selectedOption = null;
let correctAnswers = 0;

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('start-btn').addEventListener('click', startQuiz);
    document.getElementById('check-btn').addEventListener('click', checkAnswer);
    document.getElementById('next-btn').addEventListener('click', showNextQuestion);
    document.getElementById('prev-btn').addEventListener('click', showPreviousQuestion);
});

async function startQuiz() {
    const questionCount = document.getElementById('question-count').value;
    if (!questionCount || questionCount < 1 || questionCount > 94) {
        alert('Please enter a valid number of questions (1-94)');
        return;
    }

    try {
        const response = await fetch(`http://localhost:5000/get_questions?count=${questionCount}`);
        const questions = await response.json();

        currentQuestions = questions;
        currentQuestionIndex = 0;
        correctAnswers = 0;

        document.getElementById('start-screen').style.display = 'none';
        document.getElementById('quiz-container').style.display = 'block';
        document.getElementById('question-tracker').style.display = 'block';

        renderQuestionTracker();
        showQuestion();
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to load questions.');
    }
}

function renderQuestionTracker() {
    const trackerGrid = document.getElementById('tracker-grid');
    trackerGrid.innerHTML = '';

    currentQuestions.forEach((_, index) => {
        const trackerItem = document.createElement('div');
        trackerItem.classList.add('tracker-item', 'unanswered');
        trackerItem.textContent = index + 1;
        trackerItem.addEventListener('click', () => jumpToQuestion(index));
        trackerGrid.appendChild(trackerItem);
    });
}

function updateTracker(index, isCorrect) {
    const trackerItems = document.querySelectorAll('.tracker-item');
    const trackerItem = trackerItems[index];

    trackerItem.classList.remove('unanswered', 'correct', 'incorrect');
    trackerItem.classList.add(isCorrect ? 'correct' : 'incorrect');
}

function showQuestion() {
    const question = currentQuestions[currentQuestionIndex];
    document.getElementById('question-text').textContent = 
        `Question ${currentQuestionIndex + 1}/${currentQuestions.length}: ${question.question}`;

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

    document.getElementById('result').textContent = '';
    document.getElementById('description').style.display = 'none';
    document.getElementById('check-btn').style.display = 'block';
    document.getElementById('next-btn').style.display = currentQuestionIndex < currentQuestions.length - 1 ? 'block' : 'none';
    document.getElementById('prev-btn').style.display = currentQuestionIndex > 0 ? 'block' : 'none';
}

function selectOption(optionDiv) {
    document.querySelectorAll('.option').forEach(opt => opt.classList.remove('selected'));
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

    if (isCorrect) {
        correctAnswers++;
        document.getElementById('correct-count').textContent = correctAnswers;
    }

    updateTracker(currentQuestionIndex, isCorrect);

    document.getElementById('result').textContent = isCorrect ? 'Correct!' : `Incorrect! The correct answer is: ${question.correct_answer.toUpperCase()}`;
    document.getElementById('description').textContent = `Explanation: ${question.description}`;
    document.getElementById('description').style.display = 'block';
}

function showNextQuestion() {
    if (currentQuestionIndex < currentQuestions.length - 1) {
        currentQuestionIndex++;
        showQuestion();
    }
}

function showPreviousQuestion() {
    if (currentQuestionIndex > 0) {
        currentQuestionIndex--;
        showQuestion();
    }
}

function jumpToQuestion(index) {
    currentQuestionIndex = index;
    showQuestion();
}
