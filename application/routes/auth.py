from flask import Blueprint, render_template, redirect, url_for, session, flash
from application.forms.inscription_form import InscriptionForm
from application.forms.connexion_form import ConnexionForm
from application.models.utilisateur import CreerUtilisateur, Connexion
from application.models.reference import recuperer_type_de_piece, recuperer_zone_livraison

bp = Blueprint('auth', __name__)

@bp.route('/connexion', methods=['GET', 'POST'])
def connexion():  
    form = ConnexionForm()

    if form.validate_on_submit():
        userInfo = Connexion(
            courriel=form.courriel.data,
            password=form.password.data,
            typeCompte=form.type_compte.data
        )

        if userInfo:
            # Créer les variables de session
            session['utilisateurId'] = userInfo['utilisateurId']
            session['nomutilisateur'] = userInfo['nomUtilisateur']
            session['role'] = userInfo['role']
            session['roleId'] = userInfo['roleId']
            session['nom'] = userInfo['nom']
            session['prenom'] = userInfo['prenom']
            flash('Connection réussie', 'success') 
            
            return redirect(url_for('accueil')) 
        else:
            flash('Identifiants incorrects', 'error') 
    
    return render_template('connexion.html', form=form)


@bp.route('/deconnexion')
def deconnexion():
    session.clear()
    return redirect(url_for('accueil'))



@bp.route('/inscription', methods=['GET', 'POST'])
def inscription():
    form = InscriptionForm()
    
    #charger les données depuis la BD
    form.type_piece.choices = recuperer_type_de_piece()
    form.zones.choices = recuperer_zone_livraison()

    if form.validate_on_submit():

        try:
            resultat=CreerUtilisateur(
                nomUtilisateur=form.nom_utilisateur.data,
                password=form.password.data,
                telephone=form.telephone.data,
                courriel=form.courriel.data,
                typeCompte=form.type_compte.data,
                nom=form.nom.data,
                prenom=form.prenom.data,
                ville=form.ville.data,
                rue=form.rue.data,
                codePostal=form.codePostal.data,
                typePiece=form.type_piece.data,
                numeroPiece=form.numero_piece.data,
                dateExpiration=form.date_expiration.data,
                zones=form.zones.data
            ) 

            # contrairement a la methode de connexion, dans le cas d'une inscription
            # avant utilsiateur de l'application, on utilisera directement 
            # l'ID du compte utilisateur dans les requetes`
            # ceci implique que je ferai des logique "OU" dans les routes
            session['utilisateurId'] = resultat.utilisateurId
            session['nomutilisateur'] = form.nom_utilisateur.data
            session['role'] = form.type_compte.data
            if resultat['clientId'] is not None:
                session['roleId'] = resultat['clientId']
            elif resultat['livreurId'] is not None:
                session['roleId'] = resultat['livreurId']

            session['nom'] = form.nom.data
            session['prenom'] =form.prenom.data
            
            flash('Inscription réussie', 'success')
            return redirect(url_for('accueil')) 
        
        except Exception as e:
            flash(f'Erreur: {str(e)}', 'error')
    
    return render_template('inscription.html', form=form)