from flask import Flask, render_template  
from config import Config
from application.forms.inscription_form import InscriptionForm
from application.forms.connexion_form import ConnexionForm
from flask import flash, redirect, url_for

## Précise l'endroit des dossiers de templates et static
app = Flask(__name__, 
            template_folder='application/templates', 
            static_folder='application/static') 

app.config.from_object(Config)

# J'utilise Flask-WTF, donc j'ai besoin d'une clé secrète, afin de sécuriser les formulaires
app.config['SECRET_KEY'] = 'pizzeria-secret-key-dev-2025'

production = False

@app.route('/')
def accueil():                          
    return render_template('Accueil.html')  

@app.route('/connexion', methods=['GET', 'POST'])
def connexion():  
    form = ConnexionForm()

    courriel = form.courriel.data
    password = form.password.data
    type_compte = form.type_compte.data

    return render_template('connexion.html')

@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    form = InscriptionForm()
    
    if form.validate_on_submit():

        nom_utilisateur = form.nom_utilisateur.data
        password = form.password.data
        nom = form.nom.data
        prenom = form.prenom.data
        telephone = form.telephone.data
        courriel = form.courriel.data
        type_compte = form.type_compte.data
        
        if type_compte == 'livreur':
            type_piece = form.type_piece.data
            numero_piece = form.numero_piece.data
            date_expiration = form.date_expiration.data
            zones = form.zones.data  
        
        flash(f'Inscription réussie pour {nom_utilisateur}!', 'success')
        return redirect(url_for('connexion'))
    
    return render_template('inscription.html', form=form)

if __name__ == '__main__':
    print("🍕 Serveur démarré sur http://localhost:5000")
    
    if production:
        app.run(debug=False)
    else:
        app.run(debug=True)