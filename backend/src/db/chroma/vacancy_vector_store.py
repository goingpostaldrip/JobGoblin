import json
import chromadb
from parser.skills_extractor import SkillsExtractor
import logging


class VacancyVectorStore:
    def __init__(self, path="./chroma"):
        self.client = chromadb.PersistentClient(path=path)
        self.collection = self.client.get_or_create_collection("vacancies")
        self.skills_extractor = SkillsExtractor()
        self.logger = logging.getLogger(__name__)

    def add_vacancies(self, vacancies, embeddings):
        # Удаляем дубликаты вакансий по ID внутри текущего пакета
        unique_vacancies = {}
        unique_embeddings = {}
        for i, v in enumerate(vacancies):
            vid = v["id"]
            unique_vacancies[vid] = v
            unique_embeddings[vid] = embeddings[i]

        ids = list(unique_vacancies.keys())
        vacancies_list = list(unique_vacancies.values())
        embeddings_list = [unique_embeddings[vid] for vid in ids]

        texts = []
        for v in vacancies_list:
            enhanced_text = self.skills_extractor.process_vacancy(v)
            texts.append(enhanced_text)

        metadatas = []
        for v in vacancies_list:
            v_copy = {}
            for key, val in v.items():
                if isinstance(val, (list, dict)):
                    v_copy[key] = json.dumps(val, ensure_ascii=False)
                else:
                    v_copy[key] = val
            metadatas.append(v_copy)

        try:
            # Пытаемся добавить все элементы
            self.collection.add(
                ids=ids,
                documents=texts,
                embeddings=embeddings_list,
                metadatas=metadatas
            )
        except Exception as e:
            if "duplicate" in str(e).lower():
                # Получаем существующие ID
                try:
                    existing_ids = set(self.collection.get()['ids'])
                except Exception as inner_e:
                    self.logger.error(f"Ошибка при получении существующих ID: {inner_e}")
                    existing_ids = set()

                # Фильтруем только новые вакансии
                new_ids = []
                new_embeddings = []
                new_texts = []
                new_metadatas = []

                for i, vid in enumerate(ids):
                    if vid not in existing_ids:
                        new_ids.append(vid)
                        new_embeddings.append(embeddings_list[i])
                        new_texts.append(texts[i])
                        new_metadatas.append(metadatas[i])

                if new_ids:
                    # Добавляем только новые вакансии
                    self.collection.add(
                        ids=new_ids,
                        documents=new_texts,
                        embeddings=new_embeddings,
                        metadatas=new_metadatas
                    )
                    self.logger.info(
                        f"Добавлено {len(new_ids)} новых вакансий. Пропущено {len(ids) - len(new_ids)} дубликатов.")
                else:
                    self.logger.info("Все вакансии уже существуют в коллекции.")
            else:
                raise e

    def query(self, query_embedding, top_k=5):
        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

    def clear_collection(self):
        try:
            self.client.delete_collection("vacancies")
            self.collection = self.client.get_or_create_collection("vacancies")
        except Exception as e:
            self.logger.error(f"Ошибка при очистке коллекции: {e}")
