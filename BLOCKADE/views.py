from flask import Flask, render_template
app = Flask(__name__)
@app.route('/')
def index():
    "return index template"
    return render_template('index.html')