from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from application.models.admin import (
    recuperer_toutes_commandes,
    recuperer_statistiques_admin,
    modifier_statut_commande
)

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/commandesAdmin')
def commandesAdmin():
    """Afficher toutes les commandes avec filtres"""
    
    # Vérifier connexion
    if session.get('utilisateurId') is None:
        flash('Veuillez vous connecter', 'warning')
        return redirect(url_for('auth.connexion'))
    
    # Vérifier rôle admin
    if session.get('role') != 'admin':
        flash('Accès réservé aux administrateurs', 'error')
        return redirect(url_for('accueil'))
    
    # Récupérer le filtre (par défaut: toutes)
    filtre = request.args.get('filtre', 'toutes')
    
    # Récupérer les commandes selon le filtre
    commandes = recuperer_toutes_commandes(filtre)
    
    # Récupérer les statistiques
    stats = recuperer_statistiques_admin()
    
    return render_template('admin.html', 
                          commandes=commandes,
                          stats=stats,
                          filtre_actif=filtre)


@bp.route('/changer-statut/<int:commande_id>', methods=['POST'])
def changer_statut(commande_id):
    """Changer le statut d'une commande"""
    
    # Vérifier rôle admin
    if session.get('utilisateurId') is None or session.get('role') != 'admin':
        flash('Accès non autorisé', 'error')
        return redirect(url_for('accueil'))
    
    try:
        nouveau_statut = request.form.get('statut')
        
        # Modifier le statut
        modifier_statut_commande(commande_id, nouveau_statut)
        
        flash('Statut modifié avec succès!', 'success')
        
    except Exception as e:
        flash('Erreur: ' + str(e), 'error')
    
    # Retourner avec le même filtre
    filtre = request.args.get('filtre', 'toutes')
    return redirect(url_for('admin.commandesAdmin', filtre=filtre))