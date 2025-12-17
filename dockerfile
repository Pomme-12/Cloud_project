FROM python:3.12-slim

# Installation des dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Copier le script converti
COPY Data_scrapping.py .

# Exécuter le script au démarrage
CMD ["python", "Data_scrapping.py"]