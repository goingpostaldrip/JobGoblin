function loadRecommendations() {
    try {
        const raw = localStorage.getItem('jg_recommendations');
        if (!raw) return null;
        return JSON.parse(raw);
    } catch (e) { return null; }
}

function renderFromRecommendations(rec) {
    if (!rec || !rec.recommendations) {
        console.log('No recommendations data found');
        return;
    }
    const data = rec.recommendations;
    console.log('Rendering full recommendations:', data);

    const subtitle = document.querySelector('.sidebar-subtitle');
    if (subtitle && data.nearest_position && data.nearest_position.title) {
        subtitle.textContent = data.nearest_position.title;
    }

    const welcomeMessage = document.querySelector('.welcome-message');
    if (welcomeMessage && data.nearest_position && data.nearest_position.title) {
        welcomeMessage.textContent = `Добро пожаловать, ${data.nearest_position.title}!`;
    }

    if (data.user_stats) {
        updateUserStats(data.user_stats);
    }

    // 3. ОБНОВЛЯЕМ НАВЫКИ
    if (data.skills_data) {
        updateSkills(data.skills_data);
    }

    // 4. ОБНОВЛЯЕМ ДОРОЖНУЮ КАРТУ
    if (data.roadmap_data) {
        updateRoadmap(data.roadmap_data);
    }

    // 5. ОБНОВЛЯЕМ РЕКОМЕНДАЦИИ (КУРСЫ И ВАКАНСИИ)
    updateRecommendations(data);

    // 6. Показываем вкладку рекомендаций по умолчанию
    const recommendationsTab = document.querySelector('[data-tab="recommendations"]');
    const recommendationsContent = document.querySelector('#recommendations');
    if (recommendationsTab && recommendationsContent) {
        document.querySelectorAll('.nav-item').forEach(item => item.classList.remove('active'));
        recommendationsTab.classList.add('active');

        document.querySelectorAll('.tab-content').forEach(content => content.style.display = 'none');
        document.querySelectorAll('.recommendations-container').forEach(content => content.style.display = 'none');
        recommendationsContent.style.display = 'block';
    }
}

function updateUserStats(stats) {
    console.log('Updating user stats:', stats);

    // Обновляем описание уровня
    const levelDesc = document.querySelector('#current-level .stat-description');
    if (levelDesc) {
        levelDesc.textContent = `Ваш уровень: ${stats.current_level}. Средний по рынку: ${stats.market_average}`;
    }

    // Обновляем описание зарплаты
    const salaryDesc = document.querySelector('#current-level .stat-card:nth-child(2) .stat-description');
    if (salaryDesc) {
        salaryDesc.textContent = `Ваша ценность: ${stats.salary_range}. Средняя по рынку: ${stats.market_salary}`;
    }

    // Обновляем прогресс в разделе Progress
    const progressCards = document.querySelectorAll('#progress .progress-card');
    if (progressCards.length >= 3) {
        progressCards[0].querySelector('.progress-percentage').textContent = `${stats.overall_progress}%`;
        progressCards[1].querySelector('.progress-percentage').textContent = `${stats.activity_level}%`;
        progressCards[2].querySelector('.progress-percentage').textContent = `${stats.months_to_goal} мес`;
    }

    // Обновляем график уровня
    updateLevelChart(stats);
}

function updateLevelChart(stats) {
    console.log('Updating level chart with stats:', stats);

    // Определяем позицию пользователя на графике
    const levelPositions = {
        'Junior': 0,
        'Middle': 1,
        'Senior': 2,
        'Lead': 3
    };

    const userLevelIndex = levelPositions[stats.current_level] || 1;

    // Обновляем данные графика
    const levelChart = Chart.getChart('levelChart');
    if (levelChart) {
        const newData = [0, 0, 0, 0];
        newData[userLevelIndex] = 70; // Высота столбца для пользователя

        levelChart.data.datasets[1].data = newData;
        levelChart.update();
    }
}

function updateSkills(skillsData) {
    console.log('Updating skills:', skillsData);

    if (skillsData.soft_skills) {
        updateSkillsSection('soft-skills', skillsData.soft_skills);
        updateSkillsChart('softSkillsChart', skillsData.soft_skills);
    }

    if (skillsData.hard_skills) {
        updateSkillsSection('hard-skills', skillsData.hard_skills);
        updateSkillsChart('hardSkillsChart', skillsData.hard_skills);
    }
}

function updateSkillsSection(sectionId, skills) {
    const section = document.getElementById(sectionId);
    if (!section) return;

    const skillMapping = {
        'ML Algorithms': 'ML Algorithms',
        'Deep Learning': 'Deep Learning',
        'Data Processing': 'Data Processing',
        'Cloud Services': 'Cloud Services',
        'Рациональность': 'Рациональность',
        'Открытость': 'Открытость',
        'Упорство': 'Упорство',
        'Гибкость': 'Гибкость',
        'Ответственность': 'Ответственность',
        'Креативность': 'Креативность',
        'Коммуникабельность': 'Коммуникабельность'
    };

    const skillItems = section.querySelectorAll('.skill-item');
    skillItems.forEach(item => {
        const skillName = item.querySelector('.skill-name');
        if (skillName) {
            const originalName = skillName.textContent.split(' ')[0];
            const mappedName = skillMapping[originalName] || originalName;

            if (skills[mappedName]) {
                const percentage = skills[mappedName];
                skillName.innerHTML = `${originalName} <span>${percentage}%</span>`;
                const progressBar = item.querySelector('.skill-progress .skill-progress-bar');
                if (progressBar) {
                    progressBar.style.width = `${percentage}%`;
                }
            }
        }
    });
}

function updateSkillsChart(chartId, skills) {
    const chart = Chart.getChart(chartId);
    if (chart && skills) {
        const labels = chart.data.labels;
        const newData = labels.map(label => skills[label] || 0);
        chart.data.datasets[0].data = newData;
        chart.update();
    }
}

function updateRoadmap(roadmapData) {
    console.log('Updating roadmap:', roadmapData);

    if (roadmapData.milestones) {
        const milestones = document.querySelectorAll('.roadmap-milestone');
        roadmapData.milestones.forEach((milestone, index) => {
            if (milestones[index]) {
                const title = milestones[index].querySelector('.milestone-title');
                const details = milestones[index].querySelector('.milestone-details');
                const skills = milestones[index].querySelector('.milestone-skills');

                if (title) {
                    const icon = title.querySelector('i') ? title.querySelector('i').outerHTML : '';
                    title.innerHTML = `${icon} ${milestone.title}`;
                }

                if (details) {
                    details.textContent = `${milestone.duration} • ${milestone.courses} курса`;
                }

                if (skills && milestone.skills) {
                    skills.innerHTML = milestone.skills.map(skill =>
                        `<span class="skill-tag ${milestone.completed ? 'completed' : ''}" data-skill="${skill}">${skill}</span>`
                    ).join('');
                }
            }
        });
    }
}

function updateRecommendations(data) {
    console.log('Updating recommendations...');

    // Рендер курсов
    const coursesContainer = document.querySelector('.recommendations-fullscreen .horizontal-scroll');
    if (coursesContainer && data.recommended_courses && data.recommended_courses.length > 0) {
        coursesContainer.innerHTML = '';
        data.recommended_courses.forEach((c, index) => {
            const card = document.createElement('div');
            card.className = 'course-card fade-in';
            card.innerHTML = `
                <div class="course-title">${c.title || 'Название курса'}</div>
                <div class="course-platform">${c.platform || 'Платформа'}</div>
                <div class="course-duration">⏱ ${c.duration || 'Длительность не указана'}</div>
                <div class="course-progress"><div class="course-progress-bar" style="width: 0%"></div></div>
                <div class="stat-description">Не начат</div>
            `;
            coursesContainer.appendChild(card);
        });
    }

    // Рендер вакансий
    const allScrollContainers = document.querySelectorAll('.recommendations-fullscreen .horizontal-scroll');
    const vacanciesContainer = allScrollContainers.length > 1 ? allScrollContainers[1] : null;

    if (vacanciesContainer && data.relevant_vacancies && data.relevant_vacancies.length > 0) {
        vacanciesContainer.innerHTML = '';
        data.relevant_vacancies.forEach((v, index) => {
            const card = document.createElement('div');
            card.className = 'vacancy-card fade-in';
            card.innerHTML = `
                <div class="vacancy-title">${v.title || 'Название вакансии'}</div>
                <div class="vacancy-company">${v.company || 'Компания'}</div>
                <div class="vacancy-salary">Совпадение: ${v.match_score || 0}%</div>
                <div class="vacancy-tags">${(v.key_skills || []).slice(0,6).map(s => `<span class='vacancy-tag'>${s}</span>`).join('')}</div>
            `;
            vacanciesContainer.appendChild(card);
        });
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const rec = loadRecommendations();
    if (rec) renderFromRecommendations(rec);
    const fadeElements = document.querySelectorAll('.fade-in');
    fadeElements.forEach((element, index) => {
        element.style.animationDelay = `${index * 0.1}s`;
    });

    // Обработка кликов по навигации
    const navItems = document.querySelectorAll('.nav-item');
    const tabContents = {
        'current-level': document.getElementById('current-level'),
        'learning-path': document.getElementById('learning-path'),
        'recommendations': document.querySelector('.recommendations-container'),
        'progress': document.getElementById('progress')
    };

    // Сначала скрываем все вкладки кроме текущего уровня
    document.getElementById('learning-path').style.display = 'none';
    document.querySelector('.recommendations-container').style.display = 'none';
    document.getElementById('progress').style.display = 'none';

    navItems.forEach(item => {
        item.addEventListener('click', function() {
            const tabId = this.getAttribute('data-tab');

            // Активируем вкладку навигации
            navItems.forEach(i => i.classList.remove('active'));
            this.classList.add('active');

            // Показываем соответствующий контент
            Object.keys(tabContents).forEach(key => {
                if (tabContents[key]) {
                    tabContents[key].style.display = key === tabId ? 'block' : 'none';
                }
            });
        });
    });

    // Обработка кликов в футере
    document.querySelectorAll('.footer-item').forEach(item => {
        item.addEventListener('click', function() {
            const text = this.querySelector('.nav-text').textContent;
            alert(`Раздел "${text}" находится в разработке`);
        });
    });

    // Обработка вкладок компетенций
    const competenceTabs = document.querySelectorAll('.tab');
    const competenceContents = document.querySelectorAll('#soft-skills, #hard-skills');

    competenceTabs.forEach(tab => {
        tab.addEventListener('click', function() {
            const tabId = this.getAttribute('data-tab');

            // Активируем вкладку
            competenceTabs.forEach(t => t.classList.remove('active'));
            this.classList.add('active');

            // Показываем соответствующий контент
            competenceContents.forEach(content => {
                content.style.display = content.id === tabId ? 'block' : 'none';
            });
        });
    });

    // График уровней
    const levelCtx = document.getElementById('levelChart').getContext('2d');
    new Chart(levelCtx, {
        type: 'bar',
        data: {
            labels: ['Junior', 'Middle', 'Senior', 'Lead'],
            datasets: [{
                label: 'Количество специалистов',
                data: [120, 85, 45, 15],
                backgroundColor: 'rgba(100, 100, 100, 0.5)',
                borderColor: 'rgba(100, 100, 100, 1)',
                borderWidth: 1
            }, {
                label: 'Ваш уровень',
                data: [0, 0, 70, 0],
                backgroundColor: 'rgba(255, 204, 0, 0.7)',
                borderColor: 'rgba(255, 204, 0, 1)',
                borderWidth: 1,
                barPercentage: 0.3
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: '#ccc'
                    }
                },
                x: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: '#ccc'
                    }
                }
            },
            plugins: {
                legend: {
                    labels: {
                        color: '#fff'
                    }
                }
            }
        }
    });

    // График зарплат
    const salaryCtx = document.getElementById('salaryChart').getContext('2d');
    new Chart(salaryCtx, {
        type: 'bar',
        data: {
            labels: ['80-120K', '120-160K', '160-200K', '200-240K', '240-280K'],
            datasets: [{
                label: 'Количество вакансий',
                data: [35, 65, 90, 55, 25],
                backgroundColor: 'rgba(100, 100, 100, 0.5)',
                borderColor: 'rgba(100, 100, 100, 1)',
                borderWidth: 1
            }, {
                label: 'Ваша ценность',
                data: [0, 0, 0, 85, 0],
                backgroundColor: 'rgba(255, 204, 0, 0.7)',
                borderColor: 'rgba(255, 204, 0, 1)',
                borderWidth: 1,
                barPercentage: 0.3
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: '#ccc'
                    }
                },
                x: {
                    grid: {
                        color: 'rgba(255, 255, 255, 极式)'
                    },
                    ticks: {
                        color: '#ccc'
                    }
                }
            },
            plugins: {
                legend: {
                    labels: {
                        color: '#fff'
                    }
                }
            }
        }
    });

    // Создание диаграмм-паутин для компетенций
    // Soft Skills
    const softSkillsCtx = document.getElementById('softSkillsChart').getContext('2d');
    const softSkillsData = {
        labels: [
            'Рациональность', 'Открытость', 'Упорство', 'Гибкость',
            'Ответственность', 'Креативность', 'Коммуникабельность'
        ],
        datasets: [{
            label: 'Уровень Soft Skills',
            data: [70, 85, 90, 75, 95, 80, 75],
            fill: true,
            backgroundColor: 'rgba(255, 204, 0, 0.2)',
            borderColor: 'rgb(255, 204, 0)',
            pointBackgroundColor: 'rgb(255, 153, 0)',
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: 'rgb(255, 153, 0)'
        }]
    };

    const softSkillsConfig = {
        type: 'radar',
        data: softSkillsData,
        options: {
            elements: {
                line: {
                    borderWidth: 3
                }
            },
            scales: {
                r: {
                    angleLines: {
                        color: 'rgba(255, 255, 255, 0.2)'
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.2)'
                    },
                    pointLabels: {
                        color: '#fff',
                        font: {
                            size: 11
                        }
                    },
                    ticks: {
                        backdropColor: 'transparent',
                        color: '#fff',
                        font: {
                            size: 9
                        }
                    },
                    suggestedMin: 0,
                    suggestedMax: 100
                }
            },
            plugins: {
                legend: {
                    labels: {
                        color: '#fff'
                    }
                }
            }
        }
    };

    new Chart(softSkillsCtx, softSkillsConfig);

    // Hard Skills
    const hardSkillsCtx = document.getElementById('hardSkillsChart').getContext('2d');
    const hardSkillsData = {
        labels: [
            'Python', 'ML Algorithms', 'Deep Learning', 'Data Processing',
            'MLOps', 'Cloud Services', 'Statistics'
        ],
        datasets: [{
            label: 'Уровень Hard Skills',
            data: [85, 78, 70, 65, 60, 45, 75],
            fill: true,
            backgroundColor: 'rgba(255, 204, 0, 0.2)',
            borderColor: 'rgb(255, 204, 0)',
            pointBackgroundColor: 'rgb(255, 153, 0)',
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: 'rgb(255, 153, 0)'
        }]
    };

    const hardSkillsConfig = {
        type: 'radar',
        data: hardSkillsData,
        options: {
            elements: {
                line: {
                    borderWidth: 3
                }
            },
            scales: {
                r: {
                    angleLines: {
                        color: 'rgba(255, 255, 255, 0.2)'
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.2)'
                    },
                    pointLabels: {
                        color: '#fff',
                        font: {
                            size: 11
                        }
                    },
                    ticks: {
                        backdropColor: 'transparent',
                        color: '#fff',
                        font: {
                            size: 9
                        }
                    },
                    suggestedMin: 0,
                    suggestedMax: 100
                }
            },
            plugins: {
                legend: {
                    labels: {
                        color: '#fff'
                    }
                }
            }
        }
    };

    new Chart(hardSkillsCtx, hardSkillsConfig);

    // Обработка кликов по навыкам в roadmap
    const skillTags = document.querySelectorAll('.skill-tag');
    const modal = document.getElementById('course-modal');
    const modalTitle = document.getElementById('modal-skill-title');
    const modalCoursesList = document.getElementById('modal-courses-list');
    const closeModal = document.querySelector('.close-modal');

    skillTags.forEach(tag => {
        tag.addEventListener('click', function() {
            const skillName = this.getAttribute('data-skill');
            const courses = this.getAttribute('data-courses').split('|');

            // Заполняем модальное окно
            modalTitle.textContent = `Курсы по навыку: ${skillName}`;
            modalCoursesList.innerHTML = '';

            courses.forEach(course => {
                const courseItem = document.createElement('div');
                courseItem.className = 'course-item';
                courseItem.innerHTML = `
                    <div class="course-title">${course}</div>
                    <div class="course-platform">Платформа: Coursera</div>
                    <div class="course-duration">Длительность: 4 недели</div>
                `;
                modalCoursesList.appendChild(courseItem);
            });

            // Показываем модальное окно
            modal.style.display = 'flex';
        });
    });

    // Закрытие модального окна
    closeModal.addEventListener('click', function() {
        modal.style.display = 'none';
    });

    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });

    // Обработка переключения диаграмм Ганта
    const ganttTabs = document.querySelectorAll('.gantt-tab');
    ganttTabs.forEach(tab => {
        tab.addEventListener('click', function() {
            ganttTabs.forEach(t => t.classList.remove('active'));
            this.classList.add('active');
            // Здесь можно добавить логику переключения между диаграммами
        });
    });

    // Обработка кликов по периодам в диаграмме Ганта
    const ganttPeriods = document.querySelectorAll('.gantt-period');
    ganttPeriods.forEach(period => {
        period.addEventListener('click', function() {
            const courseName = this.getAttribute('data-course');
            modalTitle.textContent = `Информация о курсе: ${courseName}`;
            modalCoursesList.innerHTML = `
                <div class="course-item">
                    <div class="course-title">${courseName}</div>
                    <div class="course-platform">Платформа: Coursera</div>
                    <div class="course-duration">Длительность: 8 недель</div>
                    <div class="course-duration">Сложность: Средняя</div>
                    <div class="course-duration">Рекомендуемые предварительные знания: Python, основы математики</div>
                </div>
            `;
            modal.style.display = 'flex';
        });
    });
});