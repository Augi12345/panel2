import os
import time  # Dieser Import fehlte
import signal
import sys
import platform
import socket
from datetime import datetime


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


# Funktion zum Schreiben von Logs für die Konsole
def log_to_console(message):
    print(f"[SERVER] {message}", flush=True)


# Signal-Handler für sauberes Herunterfahren
def signal_handler(sig, frame):
    log_to_console("Server wird beendet...")
    sys.exit(0)


# Globale Variablen
users = {}
banned_users = set()


# Hauptprogramm
def main():
    global users

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    log_to_console("Server wird gestartet...")

    # Lade Benutzer und gesperrte Benutzer
    users = load_passwords()
    load_banned_users()

    log_to_console(f"Server läuft mit {len(users)} Benutzern")
    log_action("Server gestartet")

    # Server am Leben halten
    try:
        while True:
            time.sleep(60)
            log_to_console("Server ist aktiv")
    except Exception as e:
        log_to_console(f"Fehler: {str(e)}")
        log_action(f"Serverfehler: {str(e)}")


if __name__ == "__main__":
    main()