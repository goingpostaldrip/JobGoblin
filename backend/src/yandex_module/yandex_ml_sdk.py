from yandex_cloud_ml_sdk import YCloudML
import os 

sdk = YCloudML(folder_id=os.environ.get("FOLDER_ID"), auth = os.environ.get("YANDEX_OAUTH_TOKEN"))