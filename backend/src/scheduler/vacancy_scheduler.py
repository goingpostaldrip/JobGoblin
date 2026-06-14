import schedule
import time
import os
from datetime import datetime
from typing import Dict, List
import logging

from parser.hh_collector import DataCollector
from parser.skills_extractor import SkillsExtractor
from embedding.embedding_model import YandexEmbeddingModel
from db.chroma.vacancy_vector_store import VacancyVectorStore

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class VacancyScheduler:
    def __init__(self, 
                 chroma_persist_directory: str = "./chroma_persist",
                 exchange_rates: Dict = None):
        self.chroma_persist_directory = chroma_persist_directory
        self.exchange_rates = exchange_rates or {"USD": 0.01264, "EUR": 0.01083, "RUR": 1.0}
        
        self.data_collector = DataCollector(self.exchange_rates)
        self.skills_extractor = SkillsExtractor()
        self.embedding_model = YandexEmbeddingModel()
        self.vector_store = VacancyVectorStore(path=chroma_persist_directory)
        
        os.makedirs(chroma_persist_directory, exist_ok=True)
        
        logger.info(f"VacancyScheduler инициализирован. ChromaDB будет сохраняться в {chroma_persist_directory}")
    
    def parse_and_store_vacancies(self, 
                                 ml_roles: List[int] = [156, 165], 
                                 dev_roles: List[int] = [96],
                                 per_page: int = 10,
                                 num_workers: int = 3) -> None:
        logger.info("Начинаем парсинг вакансий...")
        start_time = datetime.now()
        
        try:
            ml_vacancies = []
            for role in ml_roles:
                logger.info(f"Парсим ML вакансии для роли {role}")
                vacancies = self.data_collector.collect_vacancies(
                    query={"per_page": per_page, "professional_roles": [role]},
                    num_workers=num_workers
                )
                ml_vacancies.extend(vacancies)
            
            dev_vacancies = []
            for role in dev_roles:
                logger.info(f"Парсим вакансии разработки для роли {role}")
                vacancies = self.data_collector.collect_vacancies(
                    query={"per_page": per_page, "professional_roles": [role]},
                    num_workers=num_workers
                )
                dev_vacancies.extend(vacancies)
            
            all_vacancies = ml_vacancies + dev_vacancies
            logger.info(f"Собрано {len(all_vacancies)} вакансий")
            
            if not all_vacancies:
                logger.warning("Не удалось собрать вакансии")
                return
            
            logger.info("Создаем эмбеддинги...")
            embeddings = []
            for i, vacancy in enumerate(all_vacancies):
                if i % 10 == 0:
                    logger.info(f"Обработано {i}/{len(all_vacancies)} вакансий")
                
                enhanced_text = self.skills_extractor.process_vacancy(vacancy)
                embedding = self.embedding_model.get_embedding(enhanced_text)
                embeddings.append(list(embedding))
            
            logger.info(f"Создано {len(embeddings)} эмбеддингов")
            
            logger.info("Сохраняем в ChromaDB...")
            self.vector_store.add_vacancies(all_vacancies, embeddings)

            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            logger.info(f"Парсинг завершен за {duration:.2f} секунд")
            
        except Exception as e:
            logger.error(f"Ошибка при парсинге вакансий: {e}")
            raise
    
    def search_vacancies(self, query: str, top_k: int = 5) -> Dict:
        try:
            enhanced_query = self.skills_extractor.process_query(query)
            query_embedding = list(self.embedding_model.get_embedding(enhanced_query))
            
            results = self.vector_store.query(query_embedding, top_k=top_k)
            
            logger.info(f"Найдено {len(results.get('documents', [[]])[0])} результатов для запроса: {query}")
            return results
            
        except Exception as e:
            logger.error(f"Ошибка при поиске: {e}")
            raise
    
    def setup_schedule(self, 
                      parse_time: str = "09:00",
                      parse_days: List[str] = ["monday", "wednesday", "friday"]) -> None:
        for day in parse_days:
            getattr(schedule.every(), day).at(parse_time).do(self.parse_and_store_vacancies)
        
        logger.info(f"Расписание настроено: {parse_days} в {parse_time}")
    
    def run_scheduler(self) -> None:
        logger.info("Запускаем планировщик...")
        
        logger.info("Выполняем первоначальный парсинг...")
        self.parse_and_store_vacancies()
        
        while True:
            schedule.run_pending()
            time.sleep(60)
    
    def run_once(self) -> None:
        logger.info("Выполняем разовый парсинг...")
        self.parse_and_store_vacancies()
