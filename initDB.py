from flask import Flask
from BLOCKADE.app_models.models import db, init_db 
from BLOCKADE.views import app           
import config

if __name__ == "__main__":

    with app.app_context():
        init_db()