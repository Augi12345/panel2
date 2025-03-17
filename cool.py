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

# Admin-Funktion zum Sperren/Entsperren
def admin_panel():
    while True:
        print("\nAdmin Panel - Funktionsverwaltung")
        print("1. Funktion sperren/entsperren")
        print("2. Zurück zum Hauptmenü")
        choice = input("Wähle eine Option: ")
        if choice == '1':
            print("Verfügbare Funktionen:")
            for i, func in enumerate(locked_functions, start=1):
                print(f"{i}. {func} (Gesperrt für: {locked_functions[func]})")
            func_choice = int(input("Wähle eine Funktion: "))
            if 1 <= func_choice <= len(locked_functions):
                func_name = list(locked_functions.keys())[func_choice - 1]
                user_to_lock = input("Benutzername zum Sperren/Entsperren: ")
                if user_to_lock in locked_functions[func_name]:
                    locked_functions[func_name].remove(user_to_lock)
                    print(f"Funktion {func_name} für {user_to_lock} entsperrt.")
                else:
                    locked_functions[func_name].append(user_to_lock)
                    print(f"Funktion {func_name} für {user_to_lock} gesperrt.")
        elif choice == '2':
            break
        else:
            print("Ungültige Auswahl!")

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
            break
        else:
            print("\033[91mFalscher Nutzername oder Passwort. Zugriff verweigert.\033[0m")

# Abmeldefunktion
def logout():
    global username
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