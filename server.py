import os
import time
import platform
import sys
import socket
from datetime import datetime
import threading
from flask import Flask, request, jsonify, render_template_string

# Flask App initialisieren
app = Flask(__name__)

# Globale Variablen
users = {}
banned_users = set()

# Basis-Template für das Web-Interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Server Management</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .container { max-width: 800px; margin: 0 auto; }
        h1 { color: #333; }
        .info { background-color: #f5f5f5; padding: 15px; border-radius: 5px; }
        .button { padding: 8px 12px; background: #4CAF50; color: white; border: none; cursor: pointer; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Server Management System</h1>
        <div class="info">
            <p>Server ist aktiv. Systemzeit: {{ current_time }}</p>
            <p>Benutzer: {{ user_count }}</p>
        </div>
        <div>
            <h2>Login</h2>
            <form action="/login" method="post">
                <input type="text" name="username" placeholder="Benutzername"><br>
                <input type="password" name="password" placeholder="Passwort"><br>
                <button type="submit" class="button">Anmelden</button>
            </form>
        </div>
    </div>
</body>
</html>
"""


# Funktion zum Laden der Passwörter
def load_passwords():
    passwords = {}
    try:
        with open("passwords.txt", "r") as file:
            for line in file:
                if ":" in line:
                    username, password = line.strip().split(":")
                    passwords[username] = password
    except FileNotFoundError:
        with open("passwords.txt", "w") as file:
            file.write("admin:admin\n")
        passwords = {"admin": "admin"}
        print("Neue passwords.txt Datei erstellt mit Standard-Admin-Konto.")
    return passwords


# Funktion zum Laden gesperrter Benutzer
def load_banned_users():
    global banned_users
    try:
        with open("banned_users.txt", "r") as file:
            banned_users = set(file.read().splitlines())
    except FileNotFoundError:
        banned_users = set()
        with open("banned_users.txt", "w") as file:
            pass


# Protokollfunktion
def log_action(action):
    with open("logs.txt", "a") as log_file:
        log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {action}\n")


# Web-Routes

@app.route('/')
def home():
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template_string(HTML_TEMPLATE, current_time=current_time, user_count=len(users))


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if username in banned_users:
        return "Dieser Account wurde gesperrt. Kontaktiere den Administrator."

    if username in users and users[username] == password:
        log_action(f"Anmeldung: {username}")
        return f"Willkommen, {username}! Login erfolgreich."
    else:
        return "Falscher Benutzername oder Passwort."


@app.route('/api/system-info', methods=['GET'])
def system_info():
    info = {
        "system": platform.system(),
        "version": platform.version(),
        "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "users": len(users)
    }
    return jsonify(info)


@app.route('/api/ban-user', methods=['POST'])
def api_ban_user():
    auth = request.headers.get('Authorization')
    if not auth or auth != "Bearer admin-token":  # Einfache Auth - in Produktion besser sichern!
        return jsonify({"error": "Nicht autorisiert"}), 401

    data = request.json
    user_to_ban = data.get('username')

    if not user_to_ban:
        return jsonify({"error": "Benutzername fehlt"}), 400

    banned_users.add(user_to_ban)
    with open("banned_users.txt", "a") as file:
        file.write(f"{user_to_ban}\n")

    log_action(f"Benutzer gesperrt: {user_to_ban} via API")
    return jsonify({"success": True, "message": f"Benutzer {user_to_ban} wurde gesperrt"})


# Hintergrund-Thread für Server-Aufgaben
def background_tasks():
    while True:
        # Periodische Aufgaben hier
        print("Hintergrundprozess ist aktiv")
        time.sleep(60)


# Hauptprogramm
if __name__ == "__main__":
    # Lade Konfigurationen
    users = load_passwords()
    load_banned_users()

    # Starte Hintergrundprozess
    bg_thread = threading.Thread(target=background_tasks)
    bg_thread.daemon = True
    bg_thread.start()

    # Starte Web-Server
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)