from flask import Flask
from BLOCKADE.models import db, init_db  # Importer votre base de données et la fonction init_db
from BLOCKADE.views import app           # Importer votre application Flask
import config

if __name__ == "__main__":
    # Contexte de l'application Flask (car en dehors de blockade)
    with app.app_context():
        # Appel à la fonction init_db() pour initialiser la base de données
        init_db()