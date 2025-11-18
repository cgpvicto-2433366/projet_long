from flask import Blueprint, render_template, redirect, url_for, session, flash, request, jsonify
from application.forms.commander import Commander
from application.models.client import recuperer_adresses_clients
from application.models.reference import (
    recuperer_format_pizza,
    recuperer_croutes_pizza,
    recuperer_sauces_pizza,
    recuperer_garnitures_pizza,
    recuperer_prix
)
from application.models.commande import recuperer_historique_commandes

bp = Blueprint('pizza', __name__)

@bp.route('/creerPizza', methods=['GET', 'POST'])
def creerPizza():
    # Vérifier connexion
    if session.get('utilisateurId') is None:
        flash('Veuillez vous connecter pour commander', 'warning')
        return redirect(url_for('auth.connexion'))
    
    # Vérifier rôle
    if session.get('role') != 'client':
        flash('Seuls les clients peuvent commander', 'error')
        return redirect(url_for('accueil'))
    
    form = Commander()

    # Charger choix depuis BD
    form.taille.choices = recuperer_format_pizza()
    form.sauce.choices = recuperer_sauces_pizza()
    form.croute.choices = recuperer_croutes_pizza()
    form.garnitures.choices = recuperer_garnitures_pizza()
    
    adresses_client= recuperer_adresses_clients(session.get('roleId'))

    if form.validate_on_submit():
        taille_id = form.taille.data
        sauce_id = form.sauce.data
        croute_id = form.croute.data
        garnitures_ids = form.garnitures.data
        
        # Vérifier max 4 garnitures
        if len(garnitures_ids) > 4:
            flash('Maximum 4 garnitures par pizza', 'error')
            panier= session.get('panier', [])
            return render_template('commander.html', form=form, panier=panier)
        
        prix_total = 0
        prix_total += recuperer_prix('tailles', taille_id)
        prix_total += recuperer_prix('sauces', sauce_id)
        prix_total += recuperer_prix('croutes', croute_id)

        for garniture_id in garnitures_ids:
            prix_total += recuperer_prix('garnitures', garniture_id)

        #Creer la pizza composer par l'utilisateur
        pizza = {
            'nom': 'Pizza',  # Nom générique
            'taille_id': taille_id,
            'sauce_id': sauce_id,
            'croute_id': croute_id,
            'garnitures': garnitures_ids,
            'prix': float(prix_total)
        }

        if 'panier' not in session:
            session['panier'] = []
        
        session['panier'].append(pizza)

        flash('Pizza ajoutée au panier!', 'success')
        return redirect(url_for('pizza.creerPizza'))

    panier = session.get('panier', [])

    return render_template('commander.html', form=form, panier=panier, adresses=adresses_client)



# Supprimer une pizza du panier
@bp.route('/supprimerPizza/<int:index>', methods=['POST']) #inspirer de https://pythonbasics.org/flask-tutorial-routes/
def supprimerPizza(index):

    panier = session.get('panier', [])
    
    if (index >= 0) and (index < len(panier)):
        # Supprimer la pizza
        panier.pop(index)
        
        # Mettre à jour la session
        session['panier'] = panier
        session.modified = True
        
        flash('Pizza supprimée du panier', 'success')
    else:
        flash('Pizza introuvable', 'error')
    
    return redirect(url_for('pizza.creerPizza'))

#vider le panier
@bp.route('/viderPanier',  methods=['POST']) 
def viderPanier():
    session.pop('panier', None)
    session.modified = True
    flash('Panier vidé', 'success')
    return redirect(url_for('pizza.creerPizza'))


#historique de commande
@bp.route('/historique')
def historique():

    
    # Vérifier connexion
    if session.get('utilisateurId') is None:
        flash('Veuillez vous connecter', 'warning')
        return redirect(url_for('auth.connexion'))
    
    # Vérifier rôle
    if session.get('role') != 'client':
        flash('Seuls les clients peuvent voir leur historique', 'error')
        return redirect(url_for('accueil'))
    
    # Récupérer l'ID du client
    client_id = session.get('roleId')
    
    # Récupérer les commandes
    commandes = recuperer_historique_commandes(client_id)
    
    return render_template('historique.html', commandes=commandes)