from flask import Blueprint

#Utilisation de blueprint pour les routes liées aux pizzas: https://flask.palletsprojects.com/en/stable/blueprints/
pizzas_bp = Blueprint('pizzas', __name__)

@pizzas_bp.route('/')
def index():
    return "Bienvenue à la pizzaria !"

@pizzas_bp.route('/menu')
def menu():
    return "Voici notre menu de pizzas."