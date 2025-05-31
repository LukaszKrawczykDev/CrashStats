FROM python:3.11-slim

WORKDIR /app

# Kopiujemy tylko requirements
COPY requirements.txt .
COPY ./alembic.ini .
COPY ./alembic ./alembic
# Instalacja zależności
RUN pip install --no-cache-dir -r requirements.txt

# Kopiujemy tylko kod aplikacji
COPY ./app ./app

# Ustawiamy ścieżkę do importów (dla Alembica)
ENV PYTHONPATH=/app