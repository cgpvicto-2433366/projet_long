"""
Fichier: livreur.py
Description: Routes pour la gestion des livraisons
Auteur: [Ton nom]
Date: [Date]
"""

from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from application.models.livraison import (
    recuperer_commandes_en_attente_de_livraison,
    marquer_commande_livree,
    recuperer_statistiques_livreur,
    marquer_commande_recuperer
)

bp = Blueprint('livreur', __name__)


@bp.route('/livraisons')
def livraisons():
    """Afficher les commandes en attente de livraison"""
    
    # Vérifier connexion
    if session.get('utilisateurId') is None:
        flash('Veuillez vous connecter', 'warning')
        return redirect(url_for('auth.connexion'))
    
    # Vérifier rôle
    if session.get('role') != 'livreur':
        flash('Accès réservé aux livreurs', 'error')
        return redirect(url_for('accueil'))
    
    # Récupérer l'ID du livreur
    livreur_id = session.get('roleId')
    
    # Récupérer les commandes en attente
    commandes = recuperer_commandes_en_attente_de_livraison()
    
    # Récupérer les statistiques
    stats = recuperer_statistiques_livreur(livreur_id)
    
    return render_template('livraisons.html', 
                          commandes=commandes,
                          stats=stats)


@bp.route('/livrer/<int:commande_id>', methods=['POST'])
def livrer_commande(commande_id):
    """Marquer une commande comme livrée"""
    
    # Vérifier connexion et rôle
    if session.get('utilisateurId') is None or session.get('role') != 'livreur':
        flash('Accès non autorisé', 'error')
        return redirect(url_for('accueil'))
    
    try:
        livreur_id = session.get('roleId')
        
        # Marquer comme livrée
        marquer_commande_livree(commande_id, livreur_id)
        
        flash('Commande marquée comme livrée!', 'success')
        
    except Exception as e:
        flash('Erreur: ' + str(e), 'error')
    
    return redirect(url_for('livreur.livraisons'))


@bp.route('/recuperer/<int:commande_id>', methods=['POST'])
def recuperer_commande(commande_id):

    
    # Vérifier connexion et rôle
    if session.get('utilisateurId') is None or session.get('role') != 'livreur':
        flash('Accès non autorisé', 'error')
        return redirect(url_for('accueil'))
    
    try:
        livreur_id = session.get('roleId')
        
        # Marquer comme livrée
        marquer_commande_recuperer(commande_id, livreur_id)
        
        flash('Commande marquée comme récupéré!', 'success')
        
    except Exception as e:
        flash('Erreur: ' + str(e), 'error')
    
    return redirect(url_for('livreur.livraisons'))