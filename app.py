from flask import Flask, render_template  
from config import Config

## Precise l,endroit des dossiers de templates et static
app = Flask(__name__, template_folder='application/templates', static_folder='application/static') 


app.config.from_object(Config)

production = False

@app.route('/')
def connexion():
    return render_template('Accueil.html')  

if __name__ == '__main__':
    print("🍕 Serveur démarré sur http://localhost:5000")
    
    if production:
        app.run(debug=False)
    else:
        app.run(debug=True)