import os
import time
import platform
try:
    import psutil
except ModuleNotFoundError:
    os.system('pip install psutil')
    import psutil
import requests
from datetime import datetime
import socket
import sys

# Logo
logo = r"""
    ________  ________  ________  ___  ___  ________  ________  ________ 
    |\   __  \|\   __  \|\   __  \|\  \|\  \|\   __  \|\   __  \|\   __  \ 
    \ \  \|\  \ \  \|\  \ \  \|\  \ \  \\\  \ \  \|\  \ \  \|\  \ \  \|\  \ 
     \ \  \\\  \ \   ____\ \   ____\ \   __  \ \   __  \ \   __  \ \   __  \ 
      \ \  \\\  \ \  \___|\ \  \___|\ \  \ \  \ \  \ \  \ \  \ \  \ \  \ \  \ 
       \ \_______\ \__\    \ \__\    \ \__\ \__\ \__\ \__\ \__\ \__\ \__\ \__\ 
        \|_______|\|__|     \|__|     \|__|\|__|\|__|\|__|\|__|\|__|\|__|\|__|
"""

# Admin Panel
def admin_panel():
    while True:
        print("\n--- Admin Panel ---")
        print("1. Benutzer hinzufügen")
        print("2. Benutzer löschen")
        print("3. Zurück zum Hauptmenü")
        admin_choice = input("Wähle eine Option: ")

        if admin_choice == '1':
            add_user()
        elif admin_choice == '2':
            delete_user()
        elif admin_choice == '3':
            break
        else:
            print("Ungültige Auswahl, bitte erneut versuchen.")

# Systeminformationen anzeigen
def show_system_info():
    if is_locked('show_system_info'):
        print("Zugriff verweigert.")
        return
    print("Systeminformationen:")
    print(f"System: {platform.system()}")
    print(f"Version: {platform.version()}")
    print(f"Architektur: {platform.architecture()}")
    log_action("Systeminformationen angezeigt")

# Uhr anzeigen
def show_clock():
    if is_locked('show_clock'):
        print("Zugriff verweigert.")
        return
    print("Aktuelle Zeit:", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    log_action("Uhr angezeigt")

# IP-Adressen anzeigen
def get_ip_info():
    if is_locked('get_ip_info'):
        print("Zugriff verweigert.")
        return
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    print(f"Hostname: {hostname}")
    print(f"IP-Adresse: {ip_address}")
    log_action("IP-Informationen angezeigt")

# Timer setzen
def set_timer():
    if is_locked('set_timer'):
        print("Zugriff verweigert.")
        return
    seconds = int(input("Timer in Sekunden: "))
    time.sleep(seconds)
    print("Timer abgelaufen!")
    log_action("Timer gesetzt")

# Farbe ändern
def change_color():
    if is_locked('change_color'):
        print("Zugriff verweigert.")
        return
    global current_color
    print("1. Grün")
    print("2. Rot")
    print("3. Blau")
    choice = input("Farbe wählen: ")
    colors = {"1": "\033[92m", "2": "\033[91m", "3": "\033[94m"}
    current_color = colors.get(choice, "\033[92m")
    log_action("Farbe geändert")

# Protokollfunktion
def log_action(action):
    with open("action_log.txt", "a") as log_file:
        log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {username} - {action}\n")

# Benutzerverwaltung
def add_user():
    new_user = input("Neuen Benutzernamen: ")
    new_password = input("Passwort: ")
    users[new_user] = new_password
    with open("passwords.txt", "a") as file:
        file.write(f"{new_user}:{new_password}\n")
    print(f"Benutzer {new_user} hinzugefügt.")
    log_action(f"Benutzer hinzugefügt: {new_user}")

def delete_user():
    del_user = input("Benutzername zum Löschen: ")
    if del_user in users:
        del users[del_user]
        with open("passwords.txt", "w") as file:
            for user, password in users.items():
                file.write(f"{user}:{password}\n")
        print(f"Benutzer {del_user} gelöscht.")
        log_action(f"Benutzer gelöscht: {del_user}")
    else:
        print("Benutzer nicht gefunden.")

# Passwortdatei laden
def load_passwords():
    passwords = {}
    try:
        with open("passwords.txt", "r") as file:
            for line in file:
                username, password = line.strip().split(":")
                passwords[username] = password
    except FileNotFoundError:
        print("Fehler: 'passwords.txt' Datei nicht gefunden!")
        sys.exit()
    return passwords

users = load_passwords()
username = None
current_color = "\033[92m"  # Grün als Standardfarbe

# Gesperrte Funktionen
locked_functions = {
    'show_system_info': [],
    'show_clock': [],
    'get_ip_info': [],
    'set_timer': [],
    'change_color': []
}

# Überprüft, ob eine Funktion gesperrt ist
def is_locked(func_name):
    return username in locked_functions.get(func_name, [])

# Anmeldefunktion
def login():
    global username
    while True:
        username = input("Benutzername: ")
        password = input("Passwort: ")
        if username in users and users[username] == password:
            print(f"Willkommen, {username}!")
            log_action("Anmeldung")
            break
        else:
            print("\033[91mFalscher Nutzername oder Passwort. Zugriff verweigert.\033[0m")

# Abmeldefunktion
def logout():
    global username
    log_action("Abmeldung")
    print("\033[91mAbgemeldet.\033[0m")
    username = None
    login()

login()

# Hauptmenü
while True:
    os.system('cls' if os.name == 'nt' else 'clear')
    print(current_color + logo + "\033[0m")
    print(current_color + "--- Menü ---\033[0m")
    print("1. Systeminformationen anzeigen")
    print("2. Uhr anzeigen")
    print("3. IP-Adressen anzeigen")
    print("4. Timer setzen")
    print("5. Farbe ändern")
    print("6. Admin Panel") if username == 'admin' else None
    print("7. Abmelden")
    choice = input("Wähle eine Option: ")

    if choice == '1':
        show_system_info()
    elif choice == '2':
        show_clock()
    elif choice == '3':
        get_ip_info()
    elif choice == '4':
        set_timer()
    elif choice == '5':
        change_color()
    elif choice == '6' and username == 'admin':
        admin_panel()
    elif choice == '7':
        logout()
    else:
        print("\033[91mUngültige Auswahl, bitte erneut versuchen.\033[0m")
    input("Drücke Enter, um fortzufahren...")

def app():
    return None