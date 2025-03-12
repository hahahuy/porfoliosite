from flask import Flask

def create_app():
    app = Flask(__name__)

    # Import and register blueprint before handling any request
    from .routes import main
    app.register_blueprint(main)

    return app

# For simple deployment using a global app variable, you can create one instance:
app = create_app()
