const svgIcons = {
    mlEngineer: `<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="50" cy="50" r="40" fill="#6e3bce" opacity="0.2"/><path d="M30 40L50 20L70 40L50 60L30 40Z" stroke="#c23bb4" stroke-width="3" fill="none"/><circle cx="50" cy="40" r="8" fill="#6e3bce"/><path d="M40 60L50 70L60 60" stroke="#ffcc00" stroke-width="2" fill="none"/></svg>`,
    mlops: `<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="20" y="20" width="60" height="60" rx="10" fill="#6e3bce" opacity="0.2"/><circle cx="35" cy="35" r="5" fill="#c23bb4"/><circle cx="65" cy="35" r="5" fill="#c23bb4"/><circle cx="35" cy="65" r="5" fill="#c23bb4"/><circle cx="65" cy="65" r="5" fill="#c23bb4"/><path d="M35 35L65 35M35 65L65 65M35 35L35 65M65 35L65 65" stroke="#ffcc00" stroke-width="2"/></svg>`,
    dataAnalyst: `<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="20" y="30" width="60" height="50" rx="5" fill="#6e3bce" opacity="0.2"/><path d="M25 60L35 45L45 55L55 40L65 50L75 35" stroke="#c23bb4" stroke-width="3" fill="none"/><circle cx="25" cy="60" r="3" fill="#ffcc00"/><circle cx="35" cy="45" r="3" fill="#ffcc00"/><circle cx="45" cy="55" r="3" fill="#ffcc00"/><circle cx="55" cy="40" r="3" fill="#ffcc00"/><circle cx="65" cy="50" r="3" fill="#ffcc00"/><circle cx="75" cy="35" r="3" fill="#ffcc00"/></svg>`,
    fullstack: `<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="25" y="25" width="50" height="50" rx="5" fill="#6e3bce" opacity="0.2"/><rect x="30" y="30" width="15" height="15" rx="2" stroke="#c23bb4" stroke-width="2"/><rect x="55" y="30" width="15" height="15" rx="2" stroke="#c23bb4" stroke-width="2"/><rect x="30" y="55" width="15" height="15" rx="2" stroke="#c23bb4" stroke-width="2"/><rect x="55" y="55" width="15" height="15" rx="2" stroke="#c23bb4" stroke-width="2"/><path d="M45 30V45H30" stroke="#ffcc00" stroke-width="2" fill="none"/></svg>`,
    aiDataScience: `<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="50" cy="50" r="40" fill="#6e3bce" opacity="0.2"/><path d="M30 40Q50 20 70 40Q50 80 30 40Z" stroke="#c23bb4" stroke-width="3" fill="none"/><circle cx="50" cy="50" r="10" fill="#ffcc00" opacity="0.8"/><path d="M40 60L60 40" stroke="#ffcc00" stroke-width="2"/><path d="M40 40L60 60" stroke="#ffcc00" stroke-width="2"/></svg>`,

    // Иконки для навыков
    brain: `<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 4C8 4 6 6 6 10C6 12 8 14 10 14C10 14 10.5 16 12 16C13.5 16 14 14 14 14C16 14 18 12 18 10C18 6 16 4 12 4Z" stroke="#c23bb4" stroke-width="2"/><path d="M8 16V18C8 19 9 21 12 21C15 21 16 19 16 18V16" stroke="#c23bb4" stroke-width="2"/></svg>`,
    algorithm: `<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="3" y="3" width="18" height="18" rx="2" stroke="#c23bb4" stroke-width="2"/><path d="M8 8H16M8 12H16M8 16H12" stroke="#ffcc00" stroke-width="2"/></svg>`,
    data: `<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 3V21" stroke="#c23bb4" stroke-width="2"/><path d="M17 6L7 18" stroke="#c23bb4" stroke-width="2"/><circle cx="12" cy="8" r="2" fill="#ffcc00"/><circle cx="7" cy="18" r="2" fill="#ffcc00"/><circle cx="17" cy="6" r="2" fill="#ffcc00"/></svg>`,
    server: `<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="2" y="4" width="20" height="16" rx="2" stroke="#c23bb4" stroke-width="2"/><path d="M6 8H18M6 12H18M6 16H14" stroke="#ffcc00" stroke-width="2"/></svg>`,
    deployment: `<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 2L20 7L12 12L4 7L12 2Z" stroke="#c23bb4" stroke-width="2"/><path d="M4 7V17L12 22L20 17V7" stroke="#c23bb4" stroke-width="2"/><path d="M12 12V22" stroke="#ffcc00" stroke-width="2"/></svg>`,
    automation: `<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="12" r="9" stroke="#c23bb4" stroke-width="2"/><path d="M12 6V12L16 14" stroke="#ffcc00" stroke-width="2"/></svg>`,
    math: `<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M5 12H19M12 5V19" stroke="#c23bb4" stroke-width="2"/><circle cx="12" cy="12" r="9" stroke="#c23bb4" stroke-width="2"/></svg>`,
    python: `<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 3V21" stroke="#c23bb4" stroke-width="2"/><path d="M3 12H21" stroke="#c23bb4" stroke-width="2"/><circle cx="12" cy="6" r="2" fill="#ffcc00"/><circle cx="12" cy="18" r="2" fill="#ffcc00"/></svg>`,
    tensorflow: `<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6 6L18 18M6 18L18 6" stroke="#c23bb4" stroke-width="2"/><circle cx="12" cy="12" r="9" stroke="#c23bb4" stroke-width="2"/></svg>`,
    pandas: `<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="3" y="3" width="18" height="18" rx="2" stroke="#c23bb4" stroke-width="2"/><path d="M8 8H16M8 12H16M8 16H12" stroke="#ffcc00" stroke-width="2"/></svg>`,
    docker: `<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6 6H10M6 10H10M14 6H18M14 10H18" stroke="#c23bb4" stroke-width="2"/><rect x="3" y="3" width="18" height="18" rx="2" stroke="#c23bb4" stroke-width="2"/></svg>`,
    sql: `<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 3V21" stroke="#c23bb4" stroke-width="2"/><path d="M8 8H16M8 12H16M8 16H12" stroke="#ffcc00" stroke-width="2"/><circle cx="12" cy="6" r="2" fill="#ffcc00"/></svg>`,
    graduation: `<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 4L2 8L12 12L22 8L12 4Z" stroke="#c23bb4" stroke-width="2"/><path d="M2 8V14L12 18L22 14V8" stroke="#c23bb4" stroke-width="2"/><path d="M6 12V16" stroke="#ffcc00" stroke-width="2"/></svg>`,
    chart: `<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M3 3V21H21" stroke="#c23bb4" stroke-width="2"/><path d="M7 15L11 9L15 13L19 7" stroke="#ffcc00" stroke-width="2" fill="none"/></svg>`,
    cloud: `<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M18 10H16C16 7.8 14.2 6 12 6C9.8 6 8 7.8 8 10H6C3.8 10 2 11.8 2 14C2 16.2 3.8 18 6 18H18C20.2 18 22 16.2 22 14C22 11.8 20.2 10 18 10Z" stroke="#c23bb4" stroke-width="2"/><path d="M12 6V10" stroke="#ffcc00" stroke-width="2"/></svg>`,
    rocket: `<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M13 11L22 2" stroke="#c23bb4" stroke-width="2"/><path d="M13 11C13 11 17 7 22 2C17 7 21 11 21 11C21 11 17 15 13 11Z" stroke="#c23bb4" stroke-width="2"/><path d="M11 13C11 13 7 17 2 22C7 17 11 21 11 21C11 21 15 17 11 13Z" stroke="#c23bb4" stroke-width="2"/><path d="M9 12C9 12 6 9 3 6C6 9 9 6 9 6C9 6 12 9 9 12Z" stroke="#ffcc00" stroke-width="2"/></svg>`,
    check: `<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M20 6L9 17L4 12" stroke="#ffcc00" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
    nlp: `<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 3V21" stroke="#c23bb4" stroke-width="2"/><path d="M3 12H21" stroke="#c23bb4" stroke-width="2"/><circle cx="8" cy="8" r="2" fill="#ffcc00"/><circle cx="16" cy="8" r="2" fill="#ffcc00"/><circle cx="8" cy="16" r="2" fill="#ffcc00"/><circle cx="16" cy="16" r="2" fill="#ffcc00"/></svg>`,
    cv: `<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="3" y="3" width="18" height="18" rx="2" stroke="#c23bb4" stroke-width="2"/><circle cx="12" cy="10" r="3" stroke="#ffcc00" stroke-width="2"/><path d="M7 21V19C7 16.5 9.5 15 12 15C14.5 15 17 16.5 17 19V21" stroke="#ffcc00" stroke-width="2"/></svg>`
};

// База данных курсов для всех элементов ML Engineer
const coursesDatabase = {
    // Ключевые навыки
    "Алгоритмы ML": {
        description: "Понимание алгоритмов машинного обучения включает изучение различных методов и подходов, таких как линейная регрессия, логистическая регрессия, деревья решений, случайные леса, градиентный бустинг, метод опорных векторов и кластеризация.",
        courses: [
            { name: "Machine Learning by Andrew Ng", platform: "Coursera", link: "https://www.coursera.org/learn/machine-learning" },
            { name: "Practical Machine Learning", platform: "Kaggle", link: "https://www.kaggle.com/learn/machine-learning" },
            { name: "ML Algorithms Deep Dive", platform: "Udacity", link: "https://www.udacity.com/course/machine-learning-algorithms--ud1036" }
        ]
    },
    "ML Frameworks": {
        description: "Работа с фреймворками машинного обучения включает освоение TensorFlow, PyTorch, Keras и Scikit-learn. Эти инструменты предоставляют готовые реализации алгоритмов и упрощают процесс разработки.",
        courses: [
            { name: "TensorFlow Developer Certificate", platform: "Coursera", link: "https://www.coursera.org/professional-certificates/tensorflow-in-practice" },
            { name: "PyTorch for Deep Learning", platform: "Udemy", link: "https://www.udemy.com/course/pytorch-for-deep-learning" },
            { name: "Advanced Keras Techniques", platform: "Pluralsight", link: "https://www.pluralsight.com/courses/keras-advanced-deep-learning" }
        ]
    },
    "Обработка данных": {
        description: "Обработка и очистка данных - критически важный этап в машинном обучении. Включает работу с пропущенными значениями, обработку выбросов, нормализацию и feature engineering.",
        courses: [
            { name: "Data Cleaning with Python", platform: "DataCamp", link: "https://www.datacamp.com/courses/data-cleaning-with-python" },
            { name: "Feature Engineering for ML", platform: "Coursera", link: "https://www.coursera.org/learn/feature-engineering" },
            { name: "Pandas for Data Science", platform: "Real Python", link: "https://realpython.com/learning-paths/pandas-data-science" }
        ]
    },
    "Распределенные системы": {
        description: "Работа с распределенными системами включает понимание принципов параллельных вычислений, использование Apache Spark, Hadoop, Dask для обработки больших данных.",
        courses: [
            { name: "Big Data with Apache Spark", platform: "edX", link: "https://www.edx.org/course/big-data-analysis-with-apache-spark" },
            { name: "Distributed Systems Fundamentals", platform: "Coursera", link: "https://www.coursera.org/learn/distributed-systems" },
            { name: "Spark and Python for Big Data", platform: "Udemy", link: "https://www.udemy.com/course/spark-and-python-for-big-data-with-pyspark" }
        ]
    },
    "Валидация моделей": {
        description: "Методы оценки и валидации моделей включают cross-validation, метрики качества (accuracy, precision, recall, F1, ROC-AUC), анализ learning curves.",
        courses: [
            { name: "Model Evaluation and Validation", platform: "Coursera", link: "https://www.coursera.org/learn/model-evaluation-validation" },
            { name: "Advanced Model Validation", platform: "Kaggle", link: "https://www.kaggle.com/learn/advanced-model-validation" },
            { name: "ML Model Performance", platform: "LinkedIn Learning", link: "https://www.linkedin.com/learning/machine-learning-model-performance" }
        ]
    },
    "Production deployment": {
        description: "Развертывание ML-моделей в production включает контейнеризацию (Docker), оркестрацию (Kubernetes), создание API (FastAPI, Flask), мониторинг моделей.",
        courses: [
            { name: "Deploying ML Models", platform: "Coursera", link: "https://www.coursera.org/learn/deploying-machine-learning-models" },
            { name: "MLOps Fundamentals", platform: "Udacity", link: "https://www.udacity.com/course/machine-learning-dev-ops-engineer-nanodegree--nd0821" },
            { name: "Docker for ML", platform: "Pluralsight", link: "https://www.pluralsight.com/courses/docker-machine-learning" }
        ]
    },

    // Инструменты и технологии
    "Python": {
        description: "Python - основной язык программирования для машинного обучения. Включает изучение синтаксиса, структур данных, ООП и специализированных библиотек.",
        courses: [
            { name: "Python for Everybody", platform: "Coursera", link: "https://www.coursera.org/specializations/python" },
            { name: "Advanced Python Programming", platform: "Udemy", link: "https://www.udemy.com/course/advanced-python-programming" },
            { name: "Python Data Structures", platform: "edX", link: "https://www.edx.org/course/python-data-structures" }
        ]
    },
    "TensorFlow/PyTorch": {
        description: "TensorFlow и PyTorch - ведущие фреймворки для глубокого обучения. Изучение включает построение нейронных сетей, обучение моделей и развертывание.",
        courses: [
            { name: "TensorFlow in Practice", platform: "Coursera", link: "https://www.coursera.org/specializations/tensorflow-in-practice" },
            { name: "Deep Learning with PyTorch", platform: "Udacity", link: "https://www.udacity.com/course/deep-learning-pytorch--ud188" },
            { name: "Advanced TensorFlow Techniques", platform: "Pluralsight", link: "https://www.pluralsight.com/courses/advanced-tensorflow-techniques" }
        ]
    },
    "Scikit-learn": {
        description: "Scikit-learn - библиотека для классического машинного обучения. Включает реализацию большинства алгоритмов ML и инструменты для предобработки данных.",
        courses: [
            { name: "Machine Learning with Scikit-Learn", platform: "Coursera", link: "https://www.coursera.org/learn/machine-learning-with-scikit-learn" },
            { name: "Hands-On ML with Scikit-Learn", platform: "Udemy", link: "https://www.udemy.com/ccourse/hands-on-machine-learning-with-scikit-learn" },
            { name: "Scikit-Learn Fundamentals", platform: "DataCamp", link: "https://www.datacamp.com/courses/supervised-learning-with-scikit-learn" }
        ]
    },
    "Pandas/Numpy": {
        description: "Pandas и Numpy - фундаментальные библиотеки для работы с данными в Python. Включают манипуляции с данными, очистку и преобразования.",
        courses: [
            { name: "Data Analysis with Pandas", platform: "DataCamp", link: "https://www.datacamp.com/courses/data-manipulation-with-pandas" },
            { name: "Numpy for Data Science", platform: "Coursera", link: "https://www.coursera.org/learn/python-data-analysis" },
            { name: "Pandas Masterclass", platform: "Udemy", link: "https://www.udemy.com/course/data-analysis-with-pandas" }
        ]
    },
    "MLflow/Kubeflow": {
        description: "MLflow и Kubeflow - инструменты для управления ML workflows, включая отслеживание экспериментов, управление моделями и orchestration pipelines.",
        courses: [
            { name: "MLflow for ML Engineering", platform: "Coursera", link: "https://www.coursera.org/learn/mlflow" },
            { name: "Kubeflow for Machine Learning", platform: "Udemy", link: "https://www.udemy.com/course/kubeflow" },
            { name: "MLOps with MLflow and Kubeflow", platform: "Pluralsight", link: "https://www.pluralsight.com/courses/mlops-mlflow-kubeflow" }
        ]
    },
    "Docker/K8s": {
        description: "Docker и Kubernetes - инструменты для контейнеризации и оркестрации приложений. Критически важны для развертывания ML-моделей в production.",
        courses: [
            { name: "Docker Mastery", platform: "Udemy", link: "https://www.udemy.com/course/docker-mastery" },
            { name: "Kubernetes for Developers", platform: "Coursera", link: "https://www.coursera.org/learn/kubernetes-for-developers" },
            { name: "Docker and Kubernetes for ML", platform: "LinkedIn Learning", link: "https://www.linkedin.com/learning/docker-and-kubernetes-for-machine-learning" }
        ]
    },
    "SQL/NoSQL": {
        description: "SQL и NoSQL базы данных для хранения и управления данными. Включают проектирование баз данных, запросы и оптимизацию производительности.",
        courses: [
            { name: "SQL for Data Science", platform: "Coursera", link: "https://www.coursera.org/learn/sql-for-data-science" },
            { name: "NoSQL Databases", platform: "edX", link: "https://www.edx.org/course/nosql-databases" },
            { name: "Advanced SQL for Data Engineers", platform: "Udemy", link: "https://www.udemy.com/course/advanced-sql-for-data-engineers" }
        ]
    },

    // Элементы roadmap
    "Математика: линейная алгебра, статистика": {
        description: "Фундаментальная математическая база для машинного обучения. Линейная алгебра для работы с векторами и матрицами, статистика для анализа данных.",
        courses: [
            { name: "Mathematics for Machine Learning", platform: "Coursera", link: "https://www.coursera.org/specializations/mathematics-machine-learning" },
            { name: "Linear Algebra for Data Science", platform: "edX", link: "https://www.edx.org/course/linear-algebra-foundations-to-frontiers" },
            { name: "Statistics for Data Science", platform: "Udacity", link: "https://www.udacity.com/course/statistics-for-data-science--ud200" }
        ]
    },
    "Программирование на Python": {
        description: "Изучение языка Python с нуля до продвинутого уровня. Синтаксис, структуры данных, функции, ООП и работа с библиотеками.",
        courses: [
            { name: "Python for Everybody", platform: "Coursera", link: "https://www.coursera.org/specializations/python" },
            { name: "Complete Python Bootcamp", platform: "Udemy", link: "https://www.udemy.com/course/complete-python-bootcamp" },
            { name: "Advanced Python Programming", platform: "LinkedIn Learning", link: "https://www.linkedin.com/learning/advanced-python" }
        ]
    },
    "Основы машинного обучения": {
        description: "Введение в машинное обучение: основные концепции, типы обучения, базовые алгоритмы и практическое применение.",
        courses: [
            { name: "Intro to Machine Learning", platform: "Udacity", link: "https://www.udacity.com/course/intro-to-machine-learning--ud120" },
            { name: "Machine Learning Fundamentals", platform: "edX", link: "https://www.edx.org/course/machine-learning-fundamentals" },
            { name: "Practical Machine Learning", platform: "Coursera", link: "https://www.coursera.org/learn/practical-machine-learning" }
        ]
    },
    "Работа с данными (Pandas, Numpy)": {
        description: "Практическая работа с данными: загрузка, очистка, преобразование и анализ с использованием библиотек Pandas и Numpy.",
        courses: [
            { name: "Data Manipulation with Pandas", platform: "DataCamp", link: "https://www.datacamp.com/courses/data-manipulation-with-pandas" },
            { name: "Python for Data Analysis", platform: "Coursera", link: "https://www.coursera.org/learn/python-data-analysis" },
            { name: "Numpy and Pandas Masterclass", platform: "Udemy", link: "https://www.udemy.com/course/data-analysis-with-python-numpy-and-pandas" }
        ]
    },
    "Глубокое обучение и нейронные сети": {
        description: "Изучение глубокого обучения: архитектуры нейронных сетей, методы обучения, regularization и современные подходы.",
        courses: [
            { name: "Deep Learning Specialization", platform: "Coursera", link: "https://www.coursera.org/specializations/deep-learning" },
            { name: "Neural Networks and Deep Learning", platform: "edX", link: "https://www.edx.org/course/neural-networks-and-deep-learning" },
            { name: "Advanced Deep Learning", platform: "Udacity", link: "https://www.udacity.com/course/deep-learning--ud730" }
        ]
    },
    "Обработка естественного языка (NLP)": {
        description: "Методы обработки естественного языка: токенизация, embedding, трансформеры и современные NLP модели.",
        courses: [
            { name: "NLP Specialization", platform: "Coursera", link: "https://www.coursera.org/specializations/natural-language-processing" },
            { name: "Advanced NLP with Transformers", platform: "Udemy", link: "https://www.udemy.com/course/natural-language-processing-with-transformers" },
            { name: "NLP with Deep Learning", platform: "Stanford Online", link: "https://online.stanford.edu/courses/cs224n-natural-language-processing-deep-learning" }
        ]
    },
    "Компьютерное зрение (Computer Vision)": {
        description: "Алгоритмы компьютерного зрения: обработка изображений, CNN, object detection, segmentation и генеративные модели.",
        courses: [
            { name: "Computer Vision Specialization", platform: "Coursera", link: "https://www.coursera.org/specializations/computer-vision" },
            { name: "Deep Learning for Computer Vision", platform: "Udacity", link: "https://www.udacity.com/course/computer-vision-nanodegree--nd891" },
            { name: "Advanced Computer Vision", platform: "edX", link: "https://www.edx.org/course/advanced-computer-vision" }
        ]
    },
    "Рекомендательные системы": {
        description: "Построение рекомендательных систем: collaborative filtering, content-based filtering, hybrid approaches и evaluation.",
        courses: [
            { name: "Recommendation Systems", platform: "Coursera", link: "https://www.coursera.org/learn/recommender-systems" },
            { name: "Building Recommendation Engines", platform: "LinkedIn Learning", link: "https://www.linkedin.com/learning/building-recommendation-engines" },
            { name: "Advanced Recommender Systems", platform: "Udacity", link: "https://www.udacity.com/course/recommender-systems--ud1006" }
        ]
    }
};

// Данные профессий (только ML Engineer полноценный, остальные - заглушки)
const professionsData = [
    {
        id: "ml-engineer",
        title: "ML Engineer",
        subtitle: "Инженер машинного обучения",
        icon: svgIcons.mlEngineer,
        tools: "Python, TensorFlow, PyTorch, Scikit-learn, SQL, Docker",
        description: "ML Engineer (инженер машинного обучения) — это специалист, который разрабатывает, внедряет и поддерживает системы машинного обучения в production-среде. Они работают на стыке data science и software engineering, создавая масштабируемые и эффективные ML-решения. В обязанности входит: проектирование ML pipelines, feature engineering, обучение и валидация моделей, развертывание в production, мониторинг и поддержка ML систем.",
        skills: [
            { icon: svgIcons.brain, name: "Алгоритмы ML", desc: "Глубокое понимание алгоритмов машинного обучения" },
            { icon: svgIcons.algorithm, name: "ML Frameworks", desc: "Опыт работы с TensorFlow, PyTorch, Keras" },
            { icon: svgIcons.data, name: "Обработка данных", desc: "Навыки обработки и очистки больших данных" },
            { icon: svgIcons.server, name: "Распределенные системы", desc: "Опыт работы с распределенными системами" },
            { icon: svgIcons.chart, name: "Валидация моделей", desc: "Методы оценки и валидации ML-моделей" },
            { icon: svgIcons.deployment, name: "Production deployment", desc: "Развертывание ML-моделей в production" }
        ],
        toolsList: [
            { icon: svgIcons.python, name: "Python", desc: "Основной язык программирования" },
            { icon: svgIcons.tensorflow, name: "TensorFlow/PyTorch", desc: "Фреймворки глубокого обучения" },
            { icon: svgIcons.pandas, name: "Scikit-learn", desc: "Библиотека ML алгоритмов" },
            { icon: svgIcons.data, name: "Pandas/Numpy", desc: "Обработка и анализ данных" },
            { icon: svgIcons.automation, name: "MLflow/Kubeflow", desc: "Управление ML workflows" },
            { icon: svgIcons.docker, name: "Docker/K8s", desc: "Контейнеризация и оркестрация" },
            { icon: svgIcons.sql, name: "SQL/NoSQL", desc: "Работа с базами данных" }
        ],
        roadmap: [
            {
                title: "Фундаментальные основы",
                icon: svgIcons.graduation,
                items: [
                    "Математика: линейная алгебра, статистика",
                    "Программирование на Python",
                    "Основы машинного обучения",
                    "Работа с данными (Pandas, Numpy)"
                ]
            },
            {
                title: "Продвинутое ML",
                icon: svgIcons.chart,
                items: [
                    "Глубокое обучение и нейронные сети",
                    "Обработка естественного языка (NLP)",
                    "Компьютерное зрение (Computer Vision)",
                    "Рекомендательные системы"
                ]
            },
            {
                title: "Production окружение",
                icon: svgIcons.cloud,
                items: [
                    "Развертывание моделей (Docker, Kubernetes)",
                    "ML pipelines (Kubeflow, MLflow)",
                    "Мониторинг ML систем",
                    "Оптимизация производительности"
                ]
            },
            {
                title: "Специализация",
                icon: svgIcons.rocket,
                items: [
                    "Выбор специализации (NLP, CV, Speech)",
                    "Углубленное изучение фреймворков",
                    "Участие в open-source проектах",
                    "Решение реальных бизнес-задач"
                ]
            }
        ]
    },
    {
        id: "mlops",
        title: "MLOps",
        subtitle: "Machine Learning Operations",
        icon: svgIcons.mlops,
        tools: "Docker, Kubernetes, MLflow, AWS/GCP",
        description: "Раздел в разработке. Нажмите для подробностей...",
        skills: [
            { icon: svgIcons.automation, name: "Автоматизация", desc: "Навыки автоматизации процессов" },
            { icon: svgIcons.deployment, name: "Развертывание", desc: "Развертывание ML систем" }
        ],
        toolsList: [
            { icon: svgIcons.docker, name: "Docker", desc: "Контейнеризация" },
            { icon: svgIcons.server, name: "Kubernetes", desc: "Оркестрация" }
        ],
        roadmap: [
            {
                title: "Основы",
                icon: svgIcons.graduation,
                items: ["Основы DevOps", "Системы контроля версий"]
            }
        ]
    },
    {
        id: "data-analyst",
        title: "Data Analyst",
        subtitle: "Аналитик данных",
        icon: svgIcons.dataAnalyst,
        tools: "SQL, Python, Tableau, Excel",
        description: "Раздел в разработке. Нажмите для подробностей...",
        skills: [
            { icon: svgIcons.chart, name: "Визуализация", desc: "Создание дашбордов" },
            { icon: svgIcons.data, name: "Анализ", desc: "Анализ данных" }
        ],
        toolsList: [
            { icon: svgIcons.sql, name: "SQL", desc: "Базы данных" },
            { icon: svgIcons.python, name: "Python", desc: "Программирование" }
        ],
        roadmap: [
            {
                title: "Основы",
                icon: svgIcons.graduation,
                items: ["Основы анализа", "SQL базы"]
            }
        ]
    },
    {
        id: "fullstack",
        title: "FullStack Developer",
        subtitle: "Фулстек разработчик",
        icon: svgIcons.fullstack,
        tools: "JavaScript, React, Node.js",
        description: "Раздел в разработке. Нажмите для подробностей...",
        skills: [
            { icon: svgIcons.algorithm, name: "Frontend", desc: "Разработка интерфейсов" },
            { icon: svgIcons.server, name: "Backend", desc: "Серверная разработка" }
        ],
        toolsList: [
            { icon: svgIcons.python, name: "JavaScript", desc: "Основной язык" },
            { icon: svgIcons.data, name: "React", desc: "Frontend框架" }
        ],
        roadmap: [
            {
                title: "Основы",
                icon: svgIcons.graduation,
                items: ["HTML/CSS", "JavaScript основы"]
            }
        ]
    },
    {
        id: "ai-data-science",
        title: "AI & Data Science",
        subtitle: "Искусственный интеллект",
        icon: svgIcons.aiDataScience,
        tools: "Python, ML, Deep Learning",
        description: "Раздел в разработке. Нажмите для подробностей...",
        skills: [
            { icon: svgIcons.brain, name: "AI алгоритмы", desc: "Алгоритмы ИИ" },
            { icon: svgIcons.math, name: "Статистика", desc: "Математическая база" }
        ],
        toolsList: [
            { icon: svgIcons.python, name: "Python", desc: "Основной язык" },
            { icon: svgIcons.tensorflow, name: "TensorFlow", desc: "Фреймворк" }
        ],
        roadmap: [
            {
                title: "Основы",
                icon: svgIcons.graduation,
                items: ["Математика", "Программирование"]
            }
        ]
    }
];

// Функция для показа модального окна навыка
function showSkillModal(skillName, skillIcon) {
    const skillData = coursesDatabase[skillName];
    if (!skillData) {
        // Если нет данных о курсах, показываем заглушку
        const modal = document.getElementById('skillModal');
        const modalIcon = document.getElementById('skillModalIcon');
        const modalTitle = document.getElementById('skillModalTitle');
        const modalDescription = document.getElementById('skillModalDescription');
        const modalCourses = document.getElementById('skillModalCourses');

        modalIcon.innerHTML = skillIcon || svgIcons.graduation;
        modalTitle.textContent = skillName;
        modalDescription.textContent = "Информация о курсах для этого навыка находится в разработке. Проверьте позже!";
        modalCourses.innerHTML = '';

        modal.style.display = 'block';
        document.getElementById('overlay').style.display = 'block';
        return;
    }

    const modal = document.getElementById('skillModal');
    const modalIcon = document.getElementById('skillModalIcon');
    const modalTitle = document.getElementById('skillModalTitle');
    const modalDescription = document.getElementById('skillModalDescription');
    const modalCourses = document.getElementById('skillModalCourses');

    modalIcon.innerHTML = skillIcon;
    modalTitle.textContent = skillName;
    modalDescription.textContent = skillData.description;

    // Заполняем курсы
    modalCourses.innerHTML = '';
    skillData.courses.forEach(course => {
        const courseEl = document.createElement('div');
        courseEl.className = 'course-item';
        courseEl.innerHTML = `
            <div class="course-name">${course.name}</div>
            <div class="course-platform">${course.platform}</div>
            <a href="${course.link}" target="_blank" class="course-link">Перейти к курсу</a>
        `;
        modalCourses.appendChild(courseEl);
    });

    modal.style.display = 'block';
    document.getElementById('overlay').style.display = 'block';
}

// Функция для показа деталей профессии
function showProfessionDetail(profession) {
    const overlay = document.getElementById('overlay');
    const detail = document.getElementById('professionDetail');
    const detailIcon = document.getElementById('detailIcon');
    const detailTitle = document.getElementById('detailTitle');
    const detailSubtitle = document.getElementById('detailSubtitle');
    const detailDescription = document.getElementById('detailDescription');
    const detailSkills = document.getElementById('detailSkills');
    const detailTools = document.getElementById('detailTools');
    const detailRoadmap = document.getElementById('detailRoadmap');

    // Заполняем основные данные
    detailIcon.innerHTML = profession.icon;
    detailTitle.textContent = profession.title;
    detailSubtitle.textContent = profession.subtitle;
    detailDescription.textContent = profession.description;

    // Заполняем навыки
    detailSkills.innerHTML = '';
    profession.skills.forEach(skill => {
        const skillEl = document.createElement('div');
        skillEl.className = 'skill-item';
        skillEl.innerHTML = `
            <div class="skill-icon">${skill.icon}</div>
            <div class="skill-name">${skill.name}</div>
            <div class="skill-desc">${skill.desc}</div>
        `;
        // Добавляем обработчик клика
        skillEl.addEventListener('click', (e) => {
            e.stopPropagation();
            showSkillModal(skill.name, skill.icon);
        });
        detailSkills.appendChild(skillEl);
    });

    // Заполняем инструменты
    detailTools.innerHTML = '';
    profession.toolsList.forEach(tool => {
        const toolEl = document.createElement('div');
        toolEl.className = 'skill-item';
        toolEl.innerHTML = `
            <div class="skill-icon">${tool.icon}</div>
            <div class="skill-name">${tool.name}</div>
            <div class="skill-desc">${tool.desc}</div>
        `;
        // Добавляем обработчик клика для инструментов
        toolEl.addEventListener('click', (e) => {
            e.stopPropagation();
            showSkillModal(tool.name, tool.icon);
        });
        detailTools.appendChild(toolEl);
    });

    // Заполняем roadmap
    detailRoadmap.innerHTML = `
        <div class="roadmap-container">
            <div class="roadmap-title">Дорожная карта развития</div>
            <div class="roadmap">
                ${profession.roadmap.map((phase, index) => `
                    <div class="roadmap-phase">
                        <div class="phase-header">
                            <div class="phase-icon">${phase.icon}</div>
                            <h3 class="phase-title">${phase.title}</h3>
                        </div>
                        <div class="phase-items">
                            ${phase.items.map(item => `
                                <div class="phase-item">
                                    ${svgIcons.check}
                                    <span>${item}</span>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                `).join('')}
            </div>
        </div>
    `;

    // Добавляем обработчики для элементов roadmap
    const phaseItems = detailRoadmap.querySelectorAll('.phase-item');
    phaseItems.forEach(item => {
        item.addEventListener('click', (e) => {
            const skillName = item.textContent.trim();
            showSkillModal(skillName, svgIcons.graduation);
        });
    });

    // Добавляем обработчики для фаз roadmap
    const roadmapPhases = detailRoadmap.querySelectorAll('.roadmap-phase');
    roadmapPhases.forEach(phase => {
        phase.addEventListener('click', (e) => {
            if (e.target.classList.contains('phase-item')) return;
            const phaseTitle = phase.querySelector('.phase-title').textContent;
            showSkillModal(phaseTitle, svgIcons.graduation);
        });
    });

    // Показываем оверлей и детали
    overlay.style.display = 'block';
    detail.style.display = 'block';
}

// Обработчики событий
document.getElementById('closeDetail').addEventListener('click', closeDetail);
document.getElementById('closeSkillModal').addEventListener('click', closeSkillModal);
document.getElementById('overlay').addEventListener('click', closeAllModals);

function closeDetail() {
    document.getElementById('professionDetail').style.display = 'none';
    document.getElementById('overlay').style.display = 'none';
}

function closeSkillModal() {
    document.getElementById('skillModal').style.display = 'none';
    document.getElementById('overlay').style.display = 'none';
}

function closeAllModals() {
    closeDetail();
    closeSkillModal();
}

// Заполняем сетку профессий
function populateProfessionsGrid() {
    const grid = document.getElementById('professionsGrid');
    grid.innerHTML = '';

    professionsData.forEach(profession => {
        const card = document.createElement('div');
        card.className = 'profession-card';
        card.dataset.id = profession.id;

        card.innerHTML = `
            <div class="profession-icon">${profession.icon}</div>
            <div class="profession-title">${profession.title}</div>
            <div class="profession-tools">${profession.tools}</div>
        `;

        card.addEventListener('click', () => showProfessionDetail(profession));
        grid.appendChild(card);
    });
}

// Инициализация при загрузке страницы
window.addEventListener('DOMContentLoaded', () => {
    populateProfessionsGrid();
});