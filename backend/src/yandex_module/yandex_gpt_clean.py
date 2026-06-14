import json
import logging
import tempfile
import pathlib
from typing import Dict, List, Optional
from yandex_cloud_ml_sdk import YCloudML
from yandex_cloud_ml_sdk.search_indexes import (
    StaticIndexChunkingStrategy,
    TextSearchIndexType,
)
import os

logger = logging.getLogger(__name__)

class YandexGPTService:
    def __init__(self):
        self.sdk = YCloudML(
            folder_id=os.environ.get("FOLDER_ID"), 
            auth=os.environ.get("YANDEX_OAUTH_TOKEN")
        )
        self.assistant = None
        self.thread = None
        self.search_index = None
        
    def generate_recommendations(self, 
                               user_context: Dict,
                               rag_context: List[Dict],
                               target_position: Optional[str] = None) -> Dict:
        
        try:
            context_file = self._create_context_file(user_context, rag_context)
            search_index = self._create_search_index(context_file)
            tool = self.sdk.tools.search_index(
                search_index,
                call_strategy={
                    "type": "function",
                    "function": {
                        "name": "career_guidance",
                        "instruction": "Используй информацию из индекса для формирования рекомендаций по карьерному развитию"
                    }
                }
            )
            assistant = self.sdk.assistants.create(
                "yandexgpt",
                instruction="Ты — эксперт по карьерному консультированию в IT-сфере. Используй информацию из предоставленных документов для формирования детальных рекомендаций. Отвечай структурированно в JSON формате.",
                tools=[tool]
            )
            thread = self.sdk.threads.create()
            prompt = self._create_recommendation_prompt(user_context, target_position)
            thread.write(prompt)
            run = assistant.run(thread)
            result = run.wait()
            response_text = result.text if hasattr(result, 'text') else str(result)
            recommendations = self._parse_gpt_response(response_text)
            self._cleanup_resources(search_index, thread, assistant, context_file)
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Ошибка при генерации рекомендаций: {e}")
            raise
    
    def _create_context_file(self, user_context: Dict, rag_context: List[Dict]) -> str:
        context_text = self._build_context_text(user_context, rag_context)
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
            f.write(context_text)
            return f.name
    
    def _create_search_index(self, context_file: str):
        try:
            file = self.sdk.files.upload(
                context_file,
                ttl_days=1,
                expiration_policy="static"
            )
            operation = self.sdk.search_indexes.create_deferred(
                [file],
                index_type=TextSearchIndexType(
                    chunking_strategy=StaticIndexChunkingStrategy(
                        max_chunk_size_tokens=1000,
                        chunk_overlap_tokens=200,
                    )
                ),
            )
            search_index = operation.wait()
            logger.info(f"Поисковый индекс создан: {search_index.id}")
            return search_index
            
        except Exception as e:
            logger.error(f"Ошибка при создании поискового индекса: {e}")
            raise
    
    def _cleanup_resources(self, search_index, thread, assistant, context_file):
        try:
            if search_index:
                search_index.delete()
                logger.info("Поисковый индекс удален")
            if thread:
                thread.delete()
                logger.info("Тред удален")
            if assistant:
                assistant.delete()
                logger.info("Ассистент удален")
            if context_file and os.path.exists(context_file):
                os.unlink(context_file)
                logger.info("Временный файл удален")
                
        except Exception as e:
            logger.error(f"Ошибка при очистке ресурсов: {e}")
    
    def _build_context_text(self, user_context: Dict, rag_context: List[Dict]) -> str:
        context_parts = []
        
        if user_context:
            context_parts.append("=== КОНТЕКСТ ПОЛЬЗОВАТЕЛЯ ===")
            if user_context.get('current_skills'):
                context_parts.append(f"Текущие навыки: {', '.join(user_context['current_skills'])}")
            if user_context.get('experience'):
                context_parts.append(f"Опыт работы: {user_context['experience']}")
            if user_context.get('current_position'):
                context_parts.append(f"Текущая позиция: {user_context['current_position']}")
            if user_context.get('goals'):
                context_parts.append(f"Цели: {user_context['goals']}")
            if user_context.get('interests'):
                context_parts.append(f"Области интересов: {', '.join(user_context['interests'])}")
        
        if rag_context:
            context_parts.append("\n=== РЕЛЕВАНТНЫЕ ВАКАНСИИ ===")
            for i, vacancy in enumerate(rag_context[:5], 1):
                if vacancy is None:
                    continue
                    
                context_parts.append(f"\nВакансия {i}:")
                context_parts.append(f"Позиция: {vacancy.get('Специализация', 'Не указано')}")
                context_parts.append(f"Компания: {vacancy.get('Работодатель', 'Не указано')}")
                context_parts.append(f"Опыт: {vacancy.get('Требования по опыту', 'Не указано')}")
                context_parts.append(f"Навыки: {', '.join(vacancy.get('Hard компетенции', []))}")
                context_parts.append(f"Описание: {vacancy.get('Описание', '')[:300]}...")
        
        return "\n".join(context_parts)
    
    def _create_recommendation_prompt(self, user_context: Dict, target_position: Optional[str]) -> str:
        user_info = []
        if user_context.get('current_skills'):
            user_info.append(f"Навыки: {', '.join(user_context['current_skills'])}")
        if user_context.get('experience'):
            user_info.append(f"Опыт: {user_context['experience']}")
        if user_context.get('current_position'):
            user_info.append(f"Текущая позиция: {user_context['current_position']}")
        if user_context.get('goals'):
            user_info.append(f"Цели: {user_context['goals']}")
        
        user_info_text = "\n".join(user_info) if user_info else "Информация о пользователе не предоставлена"
        
        prompt = f"""
Ты - эксперт по карьерному консультированию в IT-сфере. Используй информацию из предоставленных документов для формирования детальных рекомендаций по карьерному развитию.

Информация о пользователе:
{user_info_text}

Сформируй рекомендации в следующей структуре (отвечай строго в JSON формате):

{{
    "nearest_position": {{
        "title": "Название ближайшей карьерной позиции",
        "justification": "Обоснование почему эта позиция подходит на основе текущего контекста"
    }},
    "recommended_position": {{
        "title": "Название рекомендуемой карьерной позиции на основе целеполагания",
        "justification": "Обоснование почему эта позиция рекомендуется для достижения целей"
    }},
    "competency_comparison": {{
        "current_skills": ["текущие навыки пользователя"],
        "required_skills": ["необходимые навыки для целевой позиции"],
        "gap_analysis": "Анализ разрыва между текущими и необходимыми компетенциями"
    }},
    "development_plan": {{
        "timeline": "1-2 года",
        "learning_areas": ["области для изучения"],
        "projects": ["рекомендуемые проекты и активности"],
        "milestones": ["ключевые этапы развития"]
    }},
    "recommended_courses": [
        {{
            "title": "Название курса",
            "description": "Описание курса",
            "duration": "Продолжительность",
            "platform": "Платформа"
        }}
    ],
    "relevant_vacancies": [
        {{
            "title": "Название позиции",
            "company": "Компания",
            "experience_required": "Требуемый опыт",
            "key_skills": ["ключевые навыки"],
            "match_score": "Оценка соответствия (1-10)"
        }}
    ]
}}

Важно:
- Будь конкретным и практичным в рекомендациях
- Учитывай реальные требования рынка труда
- Предлагай достижимые цели с четкими шагами
- Адаптируй рекомендации под уровень пользователя
- Используй информацию из релевантных вакансий для обоснования
"""
        
        if target_position:
            prompt += f"\n\nОбрати особое внимание на позицию: {target_position}"
        
        return prompt
    
    def _parse_gpt_response(self, response: str) -> Dict:
        try:
            if "```json" in response:
                json_start = response.find("```json") + 7
                json_end = response.find("```", json_start)
                json_str = response[json_start:json_end].strip()
            elif "```" in response:
                json_start = response.find("```") + 3
                json_end = response.find("```", json_start)
                json_str = response[json_start:json_end].strip()
            else:
                json_start = response.find("{")
                json_end = response.rfind("}") + 1
                json_str = response[json_start:json_end]
            
            recommendations = json.loads(json_str)
            return recommendations
            
        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"Ошибка при парсинге ответа GPT: {e}")
            logger.error(f"Ответ GPT: {response}")
            
            return {
                "nearest_position": {
                    "title": "Не удалось определить",
                    "justification": "Ошибка при обработке ответа"
                },
                "recommended_position": {
                    "title": "Не удалось определить", 
                    "justification": "Ошибка при обработке ответа"
                },
                "competency_comparison": {
                    "current_skills": [],
                    "required_skills": [],
                    "gap_analysis": "Ошибка при анализе"
                },
                "development_plan": {
                    "timeline": "1-2 года",
                    "learning_areas": [],
                    "projects": [],
                    "milestones": []
                },
                "recommended_courses": [],
                "relevant_vacancies": []
            }
