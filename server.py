from flask import Flask, render_template
from app.routes import main

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

# Register the blueprint
app.register_blueprint(main)

@app.route('/')
def hello():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
