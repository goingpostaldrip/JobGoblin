import requests
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Optional, List
from urllib.parse import urlencode

from .config import HH_API_BASE_URL, ROLE_TO_SPECIALIZATION, FRONTEND_KEYWORDS
from .utils import clean_tags, parse_salary
from .skills_extractor import SkillsExtractor


class DataCollector:
    def __init__(self, exchange_rates: Optional[Dict]):
        self._rates = exchange_rates or {}
        self.skills_extractor = SkillsExtractor()

    @staticmethod
    def __encode_query_for_url(query: Optional[Dict]) -> str:
        if 'professional_roles' in query:
            query_copy = query.copy()
            roles = '&'.join([f'professional_role={r}' for r in query_copy.pop('professional_roles')])
            return roles + (f'&{urlencode(query_copy)}' if len(query_copy) > 0 else '')
        return urlencode(query)

    def __parse_vacancy_to_matrix(self, vacancy: Dict) -> Optional[Dict]:
        role, specialization = None, None

        if vacancy.get("professional_roles"):
            role_id = int(vacancy["professional_roles"][0]["id"])
            role = vacancy["professional_roles"][0]["name"]

            if role_id in ROLE_TO_SPECIALIZATION:
                specialization = ROLE_TO_SPECIALIZATION[role_id]

            # Программист-разработчик → проверяем на frontend
            elif role_id == 96:
                text_to_check = (vacancy.get("name", "") + " " + clean_tags(vacancy.get("description", "")))
                if FRONTEND_KEYWORDS.search(text_to_check):
                    specialization = "Frontend"
                else:
                    return None
            else:
                return None
        else:
            return None

        description = clean_tags(vacancy.get("description", ""))
        
        extracted_skills = self.skills_extractor.extract_skills_from_text(description)
        
        hard_from_api = [s["name"].title() for s in vacancy.get("key_skills", [])]
        
        hard_skills = list(set(hard_from_api + extracted_skills['hard_skills']))

        matrix_entry = {
            "id": vacancy.get("id"),
            "Специализация": specialization,
            "Профессиональная роль": role,
            "Функции": description,
            "Hard компетенции": hard_skills,
            "Soft компетенции": extracted_skills['soft_skills'],
            "Инструменты": extracted_skills['tools'],
            "Технологический стек": extracted_skills['technologies'],
            "Требования по опыту": vacancy.get("experience", {}).get("name", ""),
            "Размер вознаграждения": parse_salary(vacancy.get("salary"), self._rates),
            "Работодатель": vacancy.get("employer", {}).get("name"),
            "Описание": description,
        }
        return matrix_entry

    def get_vacancy(self, vacancy_id: str) -> Optional[Dict]:
        url = f"{HH_API_BASE_URL}{vacancy_id}"
        vacancy = requests.get(url).json()
        return self.__parse_vacancy_to_matrix(vacancy)

    def collect_vacancies(self, query: Optional[Dict], num_workers: int = 1) -> List[Dict]:
        url_params = self.__encode_query_for_url(query)
        target_url = f"{HH_API_BASE_URL}?{url_params}"

        # num_pages = first_response.get('pages', 0)

        ids = []
        for page_idx in range(2):  # Парсим 2 страницы для большего количества вакансий
            resp = requests.get(target_url, {'page': page_idx}).json()
            if "items" not in resp:
                break
            ids.extend(item['id'] for item in resp['items'])

        jobs_list = []
        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            for vacancy in executor.map(self.get_vacancy, ids):
                if vacancy:
                    jobs_list.append(vacancy)

        return jobs_list
