from flask import Flask, render_template
app = Flask(__name__)
@app.route('/')
def index():
    "return index template"
    return render_template('index.html')

@app.route('/game')
def game():
    "return game template"
    return render_template('game.html')

@app.route('/app.css')
def send_css():
    return render_template('app.css')