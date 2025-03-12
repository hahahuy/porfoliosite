from flask import Flask, render_template

app = Flask(__name__, template_folder='app/templates')

@app.route('/')
def hello():
    return render_template('index.html')
