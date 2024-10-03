from flask import Flask, render_template
import config

app = Flask(__name__)

app.config.from_object(config)

print("BOARD_SIZE:", app.config['BOARD_SIZE']) #test

@app.route('/')
def index():
    "return index template"
    return render_template('index.html')

@app.route('/game')
def game():
    "return game template"
    return render_template('game.html', size=config.BOARD_SIZE);

@app.route('/app.css')
def send_css():
    return render_template('app.css')