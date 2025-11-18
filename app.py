from flask import Flask, render_template  
from config import Config
from application.routes.auth import bp as auth_bp
from application.routes.pizza import bp as pizza_bp
from application.routes.commande import bp as commande_bp

## Précise l'endroit des dossiers de templates et static
app = Flask(__name__, 
            template_folder='application/templates', 
            static_folder='application/static') 

app.config.from_object(Config)

# J'utilise Flask-WTF, donc j'ai besoin d'une clé secrète, afin de sécuriser les formulaires
app.config['SECRET_KEY'] = 'pizzeria-secret-key-dev-2025'

production = False

# Enregistrement des blueprints
#Authentification
app.register_blueprint(auth_bp)
app.register_blueprint(pizza_bp)
app.register_blueprint(commande_bp)

#Page d'accueil
@app.route('/')
def accueil():                          
    return render_template('Accueil.html')  

if __name__ == '__main__':
    print("🍕 Serveur démarré sur http://localhost:5000")
    
    if production:
        app.run(debug=False)
    else:
        app.run(debug=True)