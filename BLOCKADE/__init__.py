from flask import Flask
from .views import app
from .app_models import models

@app.cli.command("init.db")
def init_db():
    models.init_db()


