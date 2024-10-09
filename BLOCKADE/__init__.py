from flask import Flask
from .views import app
from .import models


def init_db():
    models.init_db()


