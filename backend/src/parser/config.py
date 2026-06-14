import re

HH_API_BASE_URL = "https://api.hh.ru/vacancies/"

ROLE_TO_SPECIALIZATION = {
    165: "Специалист по машинному обучению",  # Data Scientist
    156: "Специалист по машинному обучению",  # Data Analyst
    96: "Программист"
}

FRONTEND_KEYWORDS = re.compile(
    r"frontend|фронтенд|react|vue|angular|typescript|javascript",
    re.IGNORECASE
)

# Паттерны для извлечения технологий и навыков
TECH_PATTERNS = [
    # Языки программирования
    r'\b(Java|JavaScript|TypeScript|Python|C\+\+|C#|Go|Rust|Kotlin|Swift|PHP|Ruby|Scala|R|MATLAB|Julia)\b',
    # ML/AI фреймворки
    r'\b(PyTorch|TensorFlow|Keras|Scikit-learn|Pandas|NumPy|SciPy|OpenCV|NLTK|spaCy|Transformers|Hugging Face|LangChain|LangGraph)\b',
    # Веб-фреймворки
    r'\b(Django|Flask|FastAPI|Express|Node\.js|React|Vue|Angular|Svelte|Next\.js|Nuxt\.js|Laravel|Spring|ASP\.NET)\b',
    # Базы данных
    r'\b(PostgreSQL|MySQL|MongoDB|Redis|Elasticsearch|Cassandra|DynamoDB|SQLite|Oracle|SQL Server)\b',
    # DevOps и инфраструктура
    r'\b(Docker|Kubernetes|AWS|Azure|GCP|Terraform|Ansible|Jenkins|GitLab|GitHub|Git|Linux|Bash|Nginx|Apache)\b',
    # Протоколы и API
    r'\b(REST|GraphQL|gRPC|WebSocket|HTTP|HTTPS|OAuth|JWT|RPC|SOAP)\b',
    # Области знаний
    r'\b(ML|AI|Machine Learning|Deep Learning|Data Science|Computer Vision|NLP|Natural Language Processing|Big Data|Analytics|Statistics|Mathematics)\b',
    # Дополнительные технологии
    r'\b(Microservices|CI/CD|DevOps|Agile|Scrum|TDD|BDD|API|SDK|Framework|Library|Tool|Platform)\b'
]

# Настройки NER
NER_CONFIDENCE_THRESHOLD = 0.3

# Категории навыков для NER
SKILL_CATEGORIES = {
    'hard_skills': ["SKILL", "TECH"],
    'soft_skills': ["SOFT", "TRAIT"],
    'tools': ["TOOL"],
    'technologies': ["TECH"]
}