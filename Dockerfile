FROM python:3.9-slim

WORKDIR /app

# Kopiere Abhängigkeiten und installiere sie
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere den restlichen Code
COPY . .

# Erstelle leere Dateien für die erste Ausführung
RUN touch passwords.txt banned_users.txt logs.txt

# Setze Environment-Variablen
ENV PYTHONUNBUFFERED=1

# Starte den Worker
CMD ["python", "server.py"]