from flask import Flask
app = Flask(__name__)

@app.route('/')
def create_app():
    # register routes from routes.py
    from .routes import main
    app.register_blueprint(main)

    return app
