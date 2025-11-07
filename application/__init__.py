from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    from .routes.pizzas import pizzas_bp
    app.register_blueprint(pizzas_bp)

    return app