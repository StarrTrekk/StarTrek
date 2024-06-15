FROM python:3.9-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends mariadb-client && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /app

COPY src/requirements.txt ./
COPY src/. /app/
EXPOSE 5000

# Installation des dépendances Python
RUN pip install --no-cache-dir -r requirements.txt


CMD ["python3", "app.py"]
