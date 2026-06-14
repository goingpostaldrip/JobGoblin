import logging
from typing import Dict, List, Optional
from models.recommendation_models import UserContext, CareerRecommendations
from yandex_module.yandex_gpt import YandexGPTService
from scheduler.vacancy_scheduler import VacancyScheduler

logger = logging.getLogger(__name__)

class RecommendationService:
    def __init__(self, vacancy_scheduler: VacancyScheduler):
        self.vacancy_scheduler = vacancy_scheduler
        self.gpt_service = YandexGPTService()
    
    def get_career_recommendations(self, 
                                 user_context: UserContext,
                                 target_position: Optional[str] = None,
                                 top_k_vacancies: int = 5) -> CareerRecommendations:
        """
        Получает рекомендации по карьерному развитию на основе контекста пользователя
        
        Args:
            user_context: Контекст пользователя
            target_position: Целевая позиция (опционально)
            top_k_vacancies: Количество релевантных вакансий для анализа
        
        Returns:
            CareerRecommendations: Структурированные рекомендации
        """
        
        try:
            search_query = self._build_search_query(user_context, target_position)
            
            rag_results = self.vacancy_scheduler.search_vacancies(
                query=search_query, 
                top_k=top_k_vacancies
            )
            
            rag_context = self._format_rag_results(rag_results)

            
            user_context_dict = user_context.dict()
            
            gpt_recommendations = self.gpt_service.generate_recommendations(
                user_context=user_context_dict,
                rag_context=rag_context,
                target_position=target_position
            )
            
            recommendations = self._convert_to_pydantic_models(gpt_recommendations)
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Ошибка при получении рекомендаций: {e}")
            raise
    
    def _build_search_query(self, user_context: UserContext, target_position: Optional[str]) -> str:
        """Формирует поисковый запрос на основе контекста пользователя"""
        
        query_parts = []
        
        if target_position:
            query_parts.append(target_position)
        elif user_context.current_position:
            query_parts.append(user_context.current_position)
        
        if user_context.current_skills:
            query_parts.extend(user_context.current_skills[:3])
        
        if user_context.interests:
            query_parts.extend(user_context.interests[:2])
        
        if not query_parts:
            query_parts = ["разработчик", "программист"]
        
        return " ".join(query_parts)
    
    def _format_rag_results(self, rag_results: Dict) -> List[Dict]:
        """Преобразует результаты RAG в формат для GPT"""
        
        if not rag_results.get('documents') or not rag_results['documents'][0]:
            return []
        
        documents = rag_results['documents'][0]
        metadatas = rag_results.get('metadatas', [[]])[0]
        distances = rag_results.get('distances', [[]])[0]
        
        formatted_vacancies = []
        
        for doc, metadata, distance in zip(documents, metadatas, distances):
            if isinstance(metadata, str):
                try:
                    import json
                    metadata = json.loads(metadata)
                except:
                    pass
            
            vacancy = {
                "Специализация": metadata.get('Специализация', 'Не указано'),
                "Работодатель": metadata.get('Работодатель', 'Не указано'),
                "Требования по опыту": metadata.get('Требования по опыту', 'Не указано'),
                "Hard компетенции": metadata.get('Hard компетенции', []),
                "Soft компетенции": metadata.get('Soft компетенции', []),
                "Инструменты": metadata.get('Инструменты', []),
                "Технологический стек": metadata.get('Технологический стек', []),
                "Описание": doc,
                "relevance_score": round(1 - distance, 3)
            }
            
            formatted_vacancies.append(vacancy)
        
        return formatted_vacancies
    
    def _convert_to_pydantic_models(self, gpt_recommendations: Dict) -> CareerRecommendations:
        """Конвертирует ответ GPT в Pydantic модели"""
        
        from models.recommendation_models import (
            PositionRecommendation, 
            CompetencyComparison, 
            DevelopmentPlan,
            CourseRecommendation,
            VacancyRecommendation
        )
        
        nearest_position = PositionRecommendation(
            title=gpt_recommendations.get('nearest_position', {}).get('title', 'ML Engineer'),
            justification=gpt_recommendations.get('nearest_position', {}).get('justification', 'На основе ваших навыков и опыта')
        )
        
        recommended_position = PositionRecommendation(
            title=gpt_recommendations.get('recommended_position', {}).get('title', 'Senior ML Engineer'),
            justification=gpt_recommendations.get('recommended_position', {}).get('justification', 'Целевая позиция для развития карьеры')
        )
        
        competency_comparison = CompetencyComparison(
            current_skills=gpt_recommendations.get('competency_comparison', {}).get('current_skills', []),
            required_skills=gpt_recommendations.get('competency_comparison', {}).get('required_skills', []),
            gap_analysis=gpt_recommendations.get('competency_comparison', {}).get('gap_analysis', 'Не определено')
        )
        
        development_plan = DevelopmentPlan(
            timeline=gpt_recommendations.get('development_plan', {}).get('timeline', '1-2 года'),
            learning_areas=gpt_recommendations.get('development_plan', {}).get('learning_areas', []),
            projects=gpt_recommendations.get('development_plan', {}).get('projects', []),
            milestones=gpt_recommendations.get('development_plan', {}).get('milestones', [])
        )
        
        recommended_courses = []
        for course_data in gpt_recommendations.get('recommended_courses', []):
            course = CourseRecommendation(
                title=course_data.get('title', 'Не указано'),
                description=course_data.get('description', 'Не указано'),
                duration=course_data.get('duration', 'Не указано'),
                platform=course_data.get('platform', 'Не указано')
            )
            recommended_courses.append(course)
        
        relevant_vacancies = []
        for vacancy_data in gpt_recommendations.get('relevant_vacancies', []):
            vacancy = VacancyRecommendation(
                title=vacancy_data.get('title', 'Не указано'),
                company=vacancy_data.get('company', 'Не указано'),
                experience_required=vacancy_data.get('experience_required', 'Не указано'),
                key_skills=vacancy_data.get('key_skills', []),
                match_score=vacancy_data.get('match_score', 0)
            )
            relevant_vacancies.append(vacancy)
        
        career_recommendations = CareerRecommendations(
            nearest_position=nearest_position,
            recommended_position=recommended_position,
            competency_comparison=competency_comparison,
            development_plan=development_plan,
            recommended_courses=recommended_courses,
            relevant_vacancies=relevant_vacancies
        )
        
        career_recommendations.user_stats = gpt_recommendations.get('user_stats', {
            "current_level": "Middle+",
            "market_average": "Middle", 
            "salary_range": "180-220K ₽",
            "market_salary": "150-190K ₽",
            "overall_progress": 42,
            "activity_level": 78,
            "months_to_goal": 8
        })
        
        career_recommendations.skills_data = gpt_recommendations.get('skills_data', {
            "soft_skills": {
                "Рациональность": 70,
                "Открытость": 85,
                "Упорство": 90,
                "Гибкость": 75,
                "Ответственность": 95,
                "Креативность": 80,
                "Коммуникабельность": 75
            },
            "hard_skills": {
                "Python": 85,
                "ML Algorithms": 78,
                "Deep Learning": 70,
                "Data Processing": 65,
                "MLOps": 60,
                "Cloud Services": 45,
                "Statistics": 75
            }
        })
        
        career_recommendations.roadmap_data = gpt_recommendations.get('roadmap_data', {
            "milestones": [
                {
                    "title": "Основы ML",
                    "duration": "2 месяца",
                    "courses": 3,
                    "skills": ["Python", "Statistics"],
                    "completed": True
                },
                {
                    "title": "Алгоритмы ML", 
                    "duration": "3 месяца",
                    "courses": 4,
                    "skills": ["ML Algorithms", "Data Processing"],
                    "completed": True
                },
                {
                    "title": "Deep Learning",
                    "duration": "3 месяца", 
                    "courses": 4,
                    "skills": ["Deep Learning", "Computer Vision"],
                    "completed": False
                },
                {
                    "title": "MLOps & Cloud",
                    "duration": "2 месяца",
                    "courses": 3, 
                    "skills": ["MLOps", "Cloud Services"],
                    "completed": False
                },
                {
                    "title": "Продвинутые темы",
                    "duration": "2 месяца",
                    "courses": 3,
                    "skills": ["NLP", "Reinforcement Learning"],
                    "completed": False
                }
            ]
        })
        
        return career_recommendations
