// Элементы интерфейса
const uploadScreen = document.getElementById('upload-screen');
const interviewScreen = document.getElementById('interview-screen');
const cvUpload = document.getElementById('cv-upload');
const successMessage = document.getElementById('success-message');
const fileName = document.getElementById('file-name');

// Элементы чата
const chatContainer = document.getElementById('chat-container');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');
const stageTitle = document.getElementById('stage-title');
const progressBar = document.getElementById('progress-bar');
const typingIndicator = document.getElementById('typing');

// Данные собеседования
const interviewStages = [
    {
        title: "Этап 1: Определение контекста",
        questions: [
            "В какой профессиональной сфере вы работаете?",
            "Какая у вас текущая должность?",
            "Сколько времени вы работаете в этой профессиональной области?",
            "Расскажите о вашем опыте работы",
            "Какие проекты вы реализовали за последнее время?"
        ]
    },
    {
        title: "Этап 2: Определение целей",
        questions: [
            "Какая сфера и специализация вас интересует?",
            "Какой вид профессиональной деятельности вам наиболее интересен?",
            "Какие у вас амбиции по должности?",
            "Какие ожидания по заработной плате?",
            "Есть ли у вас карьерные цели на ближайшие 2-3 года?"
        ]
    },
    {
        title: "Этап 3: Определение уровня",
        questions: [
            "Какие у вас ключевые профессиональные навыки?",
            "Какими инструментами и технологиями вы владеете?",
            "Расскажите о ваших soft-скиллах",
            "Какое у вас образование?",
            "Какие курсы и сертификации вы проходили?"
        ]
    }
];

let currentStage = 0;
let currentQuestion = 0;
let userAnswers = [[], [], []];

// Обработка загрузки CV
cvUpload.addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file) {
        // Проверка размера файла
        if (file.size > 5 * 1024 * 1024) {
            alert('Файл слишком большой. Максимальный размер: 5MB');
            return;
        }

        // Проверка типа файла
        const validTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
        if (!validTypes.includes(file.type)) {
            alert('Пожалуйста, загрузите файл в формате PDF или DOCX');
            return;
        }

        // Показываем имя файла
        fileName.textContent = `Выбран файл: ${file.name}`;

        // Показываем сообщение об успехе
        successMessage.style.display = 'block';

        // Переходим к собеседованию через 2 секунды
        setTimeout(() => {
            uploadScreen.style.display = 'none';
            interviewScreen.style.display = 'flex';
            startInterview();
        }, 2000);
    }
});

function startInterview() {
    setTimeout(() => {
        askQuestion();
    }, 1000);
}

function askQuestion() {
    typingIndicator.style.display = 'flex';

    setTimeout(() => {
        typingIndicator.style.display = 'none';

        const question = interviewStages[currentStage].questions[currentQuestion];
        addBotMessage(question);

        // Обновляем прогресс
        updateProgress();

        // Активируем input
        userInput.disabled = false;
        sendButton.disabled = false;
        userInput.focus();

    }, 1500);
}

function addBotMessage(text) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';
    messageDiv.innerHTML = `
        <div class="avatar bot-avatar">AI</div>
        <div class="message-content">
            <div class="message-text">${text}</div>
        </div>
    `;
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function addUserMessage(text) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user-message';
    messageDiv.innerHTML = `
        <div class="avatar user-avatar">👤</div>
        <div class="message-content">
            <div class="message-text">${text}</div>
        </div>
    `;
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function updateProgress() {
    const totalQuestions = interviewStages.reduce((acc, stage) => acc + stage.questions.length, 0);
    const answeredQuestions = userAnswers.flat().length;
    const progress = (answeredQuestions / totalQuestions) * 100;
    progressBar.style.width = progress + '%';
}

function handleUserAnswer() {
    const answer = userInput.value.trim();
    if (!answer) return;

    // Сохраняем ответ
    userAnswers[currentStage].push(answer);
    addUserMessage(answer);

    // Очищаем input
    userInput.value = '';
    userInput.disabled = true;
    sendButton.disabled = true;

    // Переходим к следующему вопросу или этапу
    currentQuestion++;

    if (currentQuestion >= interviewStages[currentStage].questions.length) {
        currentQuestion = 0;
        currentStage++;

        if (currentStage >= interviewStages.length) {
            // Все этапы завершены
            setTimeout(() => {
                finishInterview();
            }, 1000);
            return;
        }

        // Обновляем заголовок этапа
        stageTitle.textContent = interviewStages[currentStage].title;

        // Сообщение о переходе к новому этапу
        setTimeout(() => {
            addBotMessage("Отлично! Переходим к следующему этапу.");
            setTimeout(askQuestion, 1500);
        }, 1000);
    } else {
        // Следующий вопрос в текущем этапе
        setTimeout(askQuestion, 1000);
    }
}

function finishInterview() {
    addBotMessage("Спасибо за ответы! Анализирую ваши данные...");

    setTimeout(() => {
        addBotMessage("На основе ваших ответов я составлю персональный карьерный план.");

        setTimeout(() => {
            addBotMessage("Переходим к рекомендациям...");

            // Здесь будет переход к результатам
            setTimeout(() => {
                // Формируем payload для backend /recommendations
                const userContext = {
                    current_skills: userAnswers[2] || [],
                    experience: (userAnswers[0] && userAnswers[0][2]) || '',
                    current_position: (userAnswers[0] && userAnswers[0][1]) || '',
                    goals: (userAnswers[1] && userAnswers[1][4]) || '',
                    interests: (userAnswers[1] ? userAnswers[1].slice(0, 2) : [])
                };

                const body = {
                    user_context: userContext,
                    target_position: (userAnswers[1] && userAnswers[1][0]) || undefined,
                    top_k_vacancies: 5
                };

                console.log('Sending request to backend:', body);

                fetch('http://localhost:8000/recommendations', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(body)
                })
                .then(res => {
                    console.log('Response status:', res.status);
                    if (!res.ok) {
                        throw new Error(`HTTP error! status: ${res.status}`);
                    }
                    return res.json();
                })
                .then(data => {
                    console.log('Received recommendations:', data);
                    try {
                        localStorage.setItem('jg_recommendations', JSON.stringify(data));
                        console.log('Saved to localStorage');
                    } catch (e) {
                        console.error('localStorage error:', e);
                    }
                    window.location.href = '/roadmap.html';
                })
                .catch(err => {
                    console.error('Recommendations error', err);
                    alert('Не удалось получить рекомендации. Попробуйте позже. Ошибка: ' + err.message);
                });
            }, 2000);
        }, 2000);
    }, 2000);
}

// Обработчики событий
sendButton.addEventListener('click', handleUserAnswer);

userInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter' && !sendButton.disabled) {
        handleUserAnswer();
    }
});

// Заглушки для других вкладок
document.querySelectorAll('.tab.inactive').forEach(tab => {
    tab.addEventListener('click', function() {
        alert('Этот раздел находится в разработке');
    });
});