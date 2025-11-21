from flask import Blueprint, render_template, redirect, url_for, session, flash, request, jsonify
from application.models.commande import creer_commande_complete
from application.models.client import creer_nouvelle_adresse, creer_client_invite

bp = Blueprint('commande', __name__)

# Valider la pizza
@bp.route('/validerPizza', methods=['POST'])
def validerPizza():
 
    
    # Vérifier panier
    panier = session.get('panier')
    
    if not panier:
        flash('Votre panier est vide!', 'error')
        return redirect(url_for('pizza.creerPizza'))
    
    try:
        est_connecte= session.get('utilisateurId') is not None

        if(est_connecte):
            client_id = session.get('roleId')
            
            # RÉCUPÉRER L'ADRESSE SÉLECTIONNÉE OU NOUVELLE
            adresse_id_existante = request.form.get('adresse_id')
            
            # Vérifier si nouvelle adresse
            rue = request.form.get('rue')
            ville = request.form.get('ville')
            code_postal = request.form.get('code_postal')

            # Déterminer quelle adresse utiliser
            if  rue and ville and code_postal:
                #  CRÉER UNE NOUVELLE ADRESSE
                adresse_id = creer_nouvelle_adresse(
                    client_id,
                    rue,
                    ville,
                    code_postal
                )
            elif adresse_id_existante:
                adresse_id = int(adresse_id_existante)
            else:
                flash('Veuillez sélectionner ou ajouter une adresse', 'error')
                return redirect(url_for('pizza.creerPizza'))
        else:    
            nom = request.form.get('nom_invite')
            prenom = request.form.get('prenom_invite')
            telephone = request.form.get('telephone_invite')
            rue = request.form.get('rue_invite')
            ville = request.form.get('ville_invite')
            code_postal = request.form.get('code_postal_invite')
            
            # Validation
            if not all([nom, prenom, telephone, rue, ville, code_postal]):
                flash('Veuillez remplir tous les champs', 'error')
                return redirect(url_for('pizza.creerPizza'))
            
            # Créer client invité
            invite = creer_client_invite(nom, prenom, telephone, rue, ville, code_postal)
            client_id = invite['client_id']
            adresse_id = invite['adresse_id']
             

        instructions = request.form.get('instructions', '').strip()

        livraison= session['livraison'] = {
            'adresseId': adresse_id,
            'instruction': instructions,
        }
        
        commande_id = creer_commande_complete(client_id, panier, livraison)
        
        # Vider le panier
        session.pop('panier', None)
        session.modified = True
        
        flash('Commande passée avec succes!', 'success')
        return redirect(url_for('pizza.creerPizza'))
        
    except Exception as e:
        flash(f'Erreur: {str(e)}', 'error')
        return redirect(url_for('pizza.creerPizza'))