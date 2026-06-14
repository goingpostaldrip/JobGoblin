import threading
import time
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional
import logging

from scheduler.vacancy_scheduler import VacancyScheduler
from services.recommendation_service import RecommendationService
from models.recommendation_models import RecommendationRequest, RecommendationResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="JobGoblin API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

scheduler = None
scheduler_thread = None
recommendation_service = None

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5

class SearchResponse(BaseModel):
    results: List[Dict]
    total: int

class TopVacancyResponse(BaseModel):
    id: str
    employer: str
    specialization: str
    experience: str
    description: str
    skills: List[str]

@app.on_event("startup")
async def startup_event():
    global scheduler, scheduler_thread, recommendation_service
    
    logger.info("Запускаем JobGoblin API...")
    
    scheduler = VacancyScheduler(chroma_persist_directory="./chroma_persist")
    recommendation_service = RecommendationService(scheduler)
    
    def run_scheduler():
        logger.info("Запускаем парсер в фоне...")
        scheduler.setup_schedule(
            parse_time="09:00",
            parse_days=["monday", "wednesday", "friday"]
        )
        
        logger.info("Выполняем первоначальный парсинг...")
        try:
            scheduler.parse_and_store_vacancies()
        except Exception as e:
            logger.error(f"Ошибка при первоначальном парсинге: {e}")
        
        logger.info("Парсер запущен в фоне")
        while True:
            try:
                scheduler.parse_and_store_vacancies()
            except Exception as e:
                logger.error(f"Ошибка при парсинге: {e}")
            time.sleep(3600)
    
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    
    logger.info("API готов к работе")

@app.get("/")
async def root():
    return {"message": "JobGoblin API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "scheduler_running": scheduler_thread.is_alive() if scheduler_thread else False}

@app.post("/search", response_model=SearchResponse)
async def search_vacancies(request: SearchRequest):
    if not scheduler:
        raise HTTPException(status_code=503, detail="Scheduler not initialized")
    
    try:
        results = scheduler.search_vacancies(request.query, top_k=request.top_k)
        
        if not results.get('documents') or not results['documents'][0]:
            return SearchResponse(results=[], total=0)
        
        documents = results['documents'][0]
        distances = results['distances'][0]
        metadatas = results.get('metadatas', [[]])[0]
        
        formatted_results = []
        for doc, distance, metadata in zip(documents, distances, metadatas):
            formatted_results.append({
                "employer": metadata.get('Работодатель', 'Неизвестно'),
                "specialization": metadata.get('Специализация', 'Не указано'),
                "experience": metadata.get('Требования по опыту', 'Не указано'),
                "distance": round(distance, 4),
                "description": doc[:200] + "..." if len(doc) > 200 else doc,
                "skills": metadata.get('Hard компетенции', [])
            })
        
        return SearchResponse(results=formatted_results, total=len(formatted_results))
    except Exception as e:
        logger.error(f"Ошибка при поиске: {e}")
        raise HTTPException(status_code=500, detail=str(e))
@app.get("/top_vacancy", response_model=TopVacancyResponse)
async def get_top_vacancy():
    if not scheduler:
        raise HTTPException(status_code=503, detail="Scheduler not initialized")
    results = scheduler.search_vacancies("", top_k=1)
    if not results.get('documents') or not results['documents'][0]:
        raise HTTPException(status_code=404, detail="No vacancies found")
    doc = results['documents'][0][0]
    metadata = results.get('metadatas', [[{}]])[0][0]
    vid = results.get('ids', [[None]])[0][0]
    return TopVacancyResponse(
        id=str(vid or metadata.get('id', '')),
        employer=metadata.get('Работодатель', 'Неизвестно'),
        specialization=metadata.get('Специализация', 'Не указано'),
        experience=metadata.get('Требования по опыту', 'Не указано'),
        description=doc,
        skills=metadata.get('Hard компетенции', [])
    )

@app.post("/parse")
async def trigger_parse():
    if not scheduler:
        raise HTTPException(status_code=503, detail="Scheduler not initialized")
    
    try:
        def run_parse():
            scheduler.parse_and_store_vacancies()
        
        parse_thread = threading.Thread(target=run_parse, daemon=True)
        parse_thread.start()
        
        return {"message": "Парсинг запущен в фоне"}
        
    except Exception as e:
        logger.error(f"Ошибка при запуске парсинга: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/recommendations", response_model=RecommendationResponse)
async def get_career_recommendations(request: RecommendationRequest):
    if not recommendation_service:
        raise HTTPException(status_code=503, detail="Recommendation service not initialized")
    
    try:
        logger.info(f"Получен запрос рекомендаций: user_context={request.user_context}, target_position={request.target_position}")
        
        recommendations = recommendation_service.get_career_recommendations(
            user_context=request.user_context,
            target_position=request.target_position,
            top_k_vacancies=request.top_k_vacancies
        )
        
        logger.info(f"Сформированы рекомендации: {recommendations}")
        
        return RecommendationResponse(
            recommendations=recommendations,
            status="success",
            message="Рекомендации успешно сформированы"
        )
        
    except Exception as e:
        logger.error(f"Ошибка при получении рекомендаций: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
