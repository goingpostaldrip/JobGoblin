FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN pip install yandexcloud

COPY . .

RUN mkdir -p /app/chroma_persist

CMD ["python", "src/app.py"]