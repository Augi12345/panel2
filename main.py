from fastapi import FastAPI
import no_name_menu
import admin

# Haupt-App erstellen
main_app = FastAPI()

# Admin-Panel unter /admin mounten
main_app.mount("/admin", admin.app)

# No-Name-Menu unter /menu mounten
main_app.mount("/menu", no_name_menu.app)

# Falls du Root-Endpunkt brauchst, z.B. für Healthchecks
@main_app.get("/")
def read_root():
    return {"message": "Main API is running!"}
