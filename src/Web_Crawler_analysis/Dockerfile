# Author: Maximilian Müller

# Verwende das offizielle Python-Basisimage
FROM python:3.9

# Setze das Arbeitsverzeichnis im Container
WORKDIR /app

# Kopiere die requirements.txt-Datei in das Arbeitsverzeichnis
COPY requirements.txt .

# Installiere die Python-Abhängigkeiten
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere die Anwendungsdateien in das Arbeitsverzeichnis
COPY . .

# Setze den gewünschten Port (z.B. 5000) für deine Flask-Anwendung
# EXPOSE 5000

# Setze den Befehl als den Einstiegspunkt, um deine Flask-Anwendung auszuführen
CMD ["python", "-u", "main.py"]


