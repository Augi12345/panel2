import os
import sys
import time

banned_users = set()

# Funktion zum Laden gesperrter Benutzer
def load_banned_users():
    global banned_users
    try:
        with open("banned_users.txt", "r") as file:
            banned_users = set(file.read().splitlines())
    except FileNotFoundError:
        banned_users = set()

# Funktion zum Sperren eines Benutzers
def ban_user():
    user_to_ban = input("Benutzernamen zum Sperren: ")
    banned_users.add(user_to_ban)
    with open("banned_users.txt", "w") as file:
        file.write('\n'.join(banned_users))
    log_action(f"Benutzer {user_to_ban} gesperrt")
    print(f"Benutzer {user_to_ban} wurde gesperrt.")

# Funktion zum Entsperren eines Benutzers
def unban_user():
    user_to_unban = input("Benutzernamen zum Entsperren: ")
    if user_to_unban in banned_users:
        banned_users.remove(user_to_unban)
        with open("banned_users.txt", "w") as file:
            file.write('\n'.join(banned_users))
        log_action(f"Benutzer {user_to_unban} entsperrt")
        print(f"Benutzer {user_to_unban} wurde entsperrt.")
    else:
        print("Benutzer nicht gefunden oder nicht gesperrt.")

# Funktion zum Anzeigen gesperrter Benutzer
def view_banned_users():
    print("--- Gesperrte Benutzer ---")
    if banned_users:
        for user in banned_users:
            print(user)
    else:
        print("Keine Benutzer gesperrt.")

# Funktion zum Loggen von Aktionen
def log_action(action):
    with open("logs.txt", "a") as file:
        file.write(f"{action}\n")

# Funktion zum Laden von Passwörtern
def load_passwords():
    return {}

# Dummy-Funktionen für Admin-Panel
def add_user(users):
    pass

def delete_user(users):
    pass

def change_password(users):
    pass

def view_logs():
    pass

def show_system_info():
    pass

def show_statistics():
    pass

def main_menu():
    admin_panel()

# Lade gesperrte Benutzer beim Start
load_banned_users()

# Füge Optionen im Admin Panel hinzu
def admin_panel():
    users = load_passwords()
    while True:
        print("\n--- Admin Panel ---")
        print("1. Benutzer hinzufügen")
        print("2. Benutzer löschen")
        print("3. Passwort ändern")
        print("4. System-Logs anzeigen")
        print("5. Systeminformationen abrufen")
        print("6. Statistiken anzeigen")
        print("7. Benutzer sperren")
        print("8. Benutzer entsperren")
        print("9. Gesperrte Benutzer anzeigen")
        print("10. Zurück")
        admin_choice = input("Wähle eine Option: ")
        if admin_choice == '1':
            add_user(users)
        elif admin_choice == '2':
            delete_user(users)
        elif admin_choice == '3':
            change_password(users)
        elif admin_choice == '4':
            view_logs()
        elif admin_choice == '5':
            show_system_info()
        elif admin_choice == '6':
            show_statistics()
        elif admin_choice == '7':
            ban_user()
        elif admin_choice == '8':
            unban_user()
        elif admin_choice == '9':
            view_banned_users()
        elif admin_choice == '10':
            break
        else:
            print("Ungültige Auswahl, bitte erneut versuchen.")

if __name__ == "__main__":
    main_menu()
