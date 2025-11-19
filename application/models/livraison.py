"""
Fichier: livraison.py
Description: Fonctions pour la gestion des livraisons
Auteur: [Ton nom]
Date: [Date]
"""

from application.database import ExecuteQuery


def recuperer_commandes_en_attente_de_livraison():
    """
    Récupérer toutes les commandes en attente de livraison 
    
    Retourne:
        Liste de commandes avec pizzas et adresses
    """
    
    # Récupérer les commandes avec statut "En attente de livraison"
    #source ou j'ai appris a utilisé le mot clés "IN" en sql https://www.w3schools.com/Sql/sql_in.asp
    query_commandes = """
        SELECT 
            c.id as commande_id,
            c.date_commande,
            c.nombre_pizza,
            a.rue,
            a.ville,
            a.code_postal,
            c.instructions
        FROM commandes c
        LEFT JOIN adresses a ON c.adresse_id = a.id
        WHERE c.statut_id IN (SELECT id FROM statuts WHERE nom IN ('prete', 'en_livraison'))
        ORDER BY c.date_commande ASC
    """
    
    commandes = ExecuteQuery(query_commandes, plusieursResultats=True)
    
    if not commandes:
        return []
    
    # Pour chaque commande, récupérer les pizzas
    for commande in commandes:
        commande_id = commande['commande_id']
        
        # Récupérer les pizzas
        query_pizzas = """
            SELECT 
                p.id as pizza_id,
                p.nom,
                t.nom as taille,
                c.nom as croute,
                s.nom as sauce
            FROM pizzas p
            JOIN tailles t ON p.taille_id = t.id
            JOIN croutes c ON p.croute_id = c.id
            JOIN sauces s ON p.sauce_id = s.id
            WHERE p.commande_id = %s
        """
        
        pizzas = ExecuteQuery(query_pizzas, (commande_id,), plusieursResultats=True)
        
        # Pour chaque pizza, récupérer les garnitures
        for pizza in pizzas:
            pizza_id = pizza['pizza_id']
            
            query_garnitures = """
                SELECT g.nom
                FROM pizzas_garnitures pg
                JOIN garnitures g ON pg.garniture_id = g.id
                WHERE pg.pizza_id = %s
            """
            
            garnitures = ExecuteQuery(query_garnitures, (pizza_id,), plusieursResultats=True)
            pizza['garnitures'] = garnitures if garnitures else []
        
        commande['pizzas'] = pizzas
    
    return commandes


def marquer_commande_livree(commande_id, livreur_id):
    """
    Marquer une commande comme livrée
    
    Paramètres:
        commande_id: ID de la commande
        livreur_id: ID du livreur
    """
    
    # Mettre à jour le statut et enregistrer le livreur
    query = """
        UPDATE commandes 
        SET statut_id = (SELECT id FROM statuts WHERE nom = 'Livree'),
            date_livraison = NOW(),
            livreur_id = %s
        WHERE id = %s
    """
    
    ExecuteQuery(query, (livreur_id, commande_id))


def marquer_commande_recuperer(commande_id, livreur_id):
    """
    Marquer une commande comme livrée
    
    Paramètres:
        commande_id: ID de la commande
        livreur_id: ID du livreur
    """
    
    # Mettre à jour le statut et enregistrer le livreur
    query = """
        UPDATE commandes 
        SET statut_id = (SELECT id FROM statuts WHERE nom = 'en_livraison'),
            date_livraison = NOW(),
            livreur_id = %s
        WHERE id = %s
    """
    
    ExecuteQuery(query, (livreur_id, commande_id))


def recuperer_statistiques_livreur(livreur_id):
    """
    Récupérer les statistiques d'un livreur
    """
    
    # 1. Compter les commandes en attente (toutes)
    query_prete = """
        SELECT COUNT(*) as nombre
        FROM commandes
        WHERE statut_id IN (SELECT id FROM statuts WHERE nom IN ('prete', 'en_livraison'))
    """
    
    result_prete = ExecuteQuery(query_prete, unResultat=True)
    
    # 2. Compter les commandes livrées par ce livreur
    query_livrees = """
        SELECT COUNT(*) as nombre
        FROM commandes
        WHERE livreur_id = %s
        AND statut_id IN (SELECT id FROM statuts WHERE nom IN ('prete', 'en_livraison'))
    """
    
    result_livrees = ExecuteQuery(query_livrees, (livreur_id,), unResultat=True)
    
    # 3. Créer le dictionnaire de résultat
    statistiques = {}
    
    # Si result_attente existe, prendre son nombre, sinon 0
    if result_prete:
        statistiques['en_attente'] = result_prete['nombre']
    else:
        statistiques['en_attente'] = 0
    
    # Si result_livrees existe, prendre son nombre, sinon 0
    if result_livrees:
        statistiques['livrees'] = result_livrees['nombre']
    else:
        statistiques['livrees'] = 0
    
    return statistiques