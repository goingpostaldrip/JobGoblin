import re
from typing import List, Dict
from .ner import NERExtractor
from .config import TECH_PATTERNS, NER_CONFIDENCE_THRESHOLD, SKILL_CATEGORIES


class SkillsExtractor:
    def __init__(self, confidence_threshold: float = None):
        self.ner_extractor = NERExtractor()
        self.confidence_threshold = confidence_threshold or NER_CONFIDENCE_THRESHOLD
        self.tech_patterns = TECH_PATTERNS
        self.skill_categories = SKILL_CATEGORIES
    
    def extract_skills_from_text(self, text: str) -> Dict[str, List[str]]:
        """
        Извлекает навыки из текста используя NER и регулярные выражения
        
        Args:
            text: Текст для анализа
            
        Returns:
            Словарь с категориями навыков
        """
        # Извлекаем навыки с помощью NER
        ner_entities = self.ner_extractor.extract(text, self.confidence_threshold)
        
        # Группируем по типам используя конфигурацию
        skills_by_type = {category: [] for category in self.skill_categories.keys()}
        
        for entity in ner_entities:
            skill_text = entity['text'].title()
            label = entity['label']
            
            # Находим подходящую категорию для лейбла
            for category, labels in self.skill_categories.items():
                if label in labels:
                    skills_by_type[category].append(skill_text)
                    break
        
        # Если NER не извлек навыки, используем регулярные выражения
        if not any(skills_by_type.values()):
            regex_skills = self._extract_skills_with_regex(text)
            skills_by_type['hard_skills'].extend(regex_skills)
        
        # Убираем дубликаты
        for category in skills_by_type:
            skills_by_type[category] = list(set(skills_by_type[category]))
        
        return skills_by_type
    
    def _extract_skills_with_regex(self, text: str) -> List[str]:
        """Извлекает навыки с помощью регулярных выражений"""
        skills = []
        
        for pattern in self.tech_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            skills.extend([match.title() for match in matches])
        
        return list(set(skills))  # Убираем дубликаты
    
    def create_enhanced_text(self, original_text: str, skills: Dict[str, List[str]]) -> str:
        """
        Создает расширенный текст с навыками для лучшего поиска
        
        Args:
            original_text: Исходный текст
            skills: Словарь с навыками по категориям
            
        Returns:
            Расширенный текст
        """
        enhanced_parts = [original_text]
        
        if skills['hard_skills']:
            enhanced_parts.append(f"Навыки: {', '.join(skills['hard_skills'])}")
        
        if skills['soft_skills']:
            enhanced_parts.append(f"Soft skills: {', '.join(skills['soft_skills'])}")
        
        if skills['tools']:
            enhanced_parts.append(f"Инструменты: {', '.join(skills['tools'])}")
        
        if skills['technologies']:
            enhanced_parts.append(f"Технологии: {', '.join(skills['technologies'])}")
        
        return " ".join(enhanced_parts)
    
    def process_vacancy(self, vacancy: Dict) -> str:
        """
        Обрабатывает вакансию и создает расширенный текст для поиска
        
        Args:
            vacancy: Словарь с данными вакансии
            
        Returns:
            Расширенный текст для поиска
        """
        description = vacancy.get("Описание", "")
        
        # Извлекаем навыки из описания
        extracted_skills = self.extract_skills_from_text(description)
        
        # Объединяем с уже существующими навыками из вакансии
        combined_skills = {
            'hard_skills': list(set(
                extracted_skills['hard_skills'] + 
                vacancy.get("Hard компетенции", [])
            )),
            'soft_skills': list(set(
                extracted_skills['soft_skills'] + 
                vacancy.get("Soft компетенции", [])
            )),
            'tools': list(set(
                extracted_skills['tools'] + 
                vacancy.get("Инструменты", [])
            )),
            'technologies': list(set(
                extracted_skills['technologies'] + 
                vacancy.get("Технологический стек", [])
            ))
        }
        
        return self.create_enhanced_text(description, combined_skills)
    
    def process_query(self, query: str) -> str:
        """
        Обрабатывает поисковый запрос пользователя
        
        Args:
            query: Поисковый запрос
            
        Returns:
            Расширенный запрос с навыками
        """
        skills = self.extract_skills_from_text(query)
        return self.create_enhanced_text(query, skills)
