from flask import Flask, render_template
app = Flask(__name__)
@app.route('/')
def index():
    "return index template"
    return render_template('index.html') #pas besoin du chemin vers le dossier?

@app.route('/game')
def game():
    "return game template"
    return render_template('game.html')