from yandex_cloud_ml_sdk import YCloudML
import os

class YandexEmbeddingModel:
    def __init__(self):
        self.sdk = YCloudML(
            folder_id=os.environ.get("FOLDER_ID"), 
            auth=os.environ.get("YANDEX_OAUTH_TOKEN")
        )
        self.model = self.sdk.models.text_embeddings(model_name="text-search-query", model_version="latest")

    def get_embedding(self, text: str):
        return self.model.run(text).embedding
