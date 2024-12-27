from flask import Flask
from .views import app
from .app_models import models

#Le décorateur créé une commande que le terminal Flask comprend
@app.cli.command("init.db")
def init_db():
    models.init_db()


