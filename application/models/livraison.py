
from application.database import ExecuteQuery
def recuperer_commandes_livreur(livreur_id=None):
    """
    Récupérer les commandes selon leur statut
    
    Paramètres:
        livreur_id: Si fourni, filtre par livreur pour 'en_livraison'
    
    Retourne:
        Dict avec commandes par statut
    """
    
    # Commandes PRÊTES (visible par tous)
    query_prete = """
        SELECT 
            c.id as commande_id,
            c.date_commande,
            c.nombre_pizza,
            a.rue, a.ville, a.code_postal,
            c.instructions
        FROM commandes c
        INNER JOIN adresses a ON c.adresse_id = a.id
        WHERE c.statut_id = (SELECT id FROM statuts WHERE nom = 'prete')
        ORDER BY c.date_commande ASC
    """
    
    # Commandes EN LIVRAISON (filtrées par livreur)
    query_en_livraison = """
        SELECT 
            c.id as commande_id,
            c.date_commande,
            c.nombre_pizza,
            a.rue, a.ville, a.code_postal,
            c.instructions
        FROM commandes c
        INNER JOIN adresses a ON c.adresse_id = a.id
        WHERE c.statut_id = (SELECT id FROM statuts WHERE nom = 'en_livraison')
    """
    
    # Ajouter filtre livreur si fourni
    if livreur_id:
        query_en_livraison += " AND c.livreur_id = %s"
        commandes_en_livraison = ExecuteQuery(query_en_livraison, (livreur_id,), plusieursResultats=True)
    else:
        commandes_en_livraison = ExecuteQuery(query_en_livraison, plusieursResultats=True)
    
    commandes_prete = ExecuteQuery(query_prete, plusieursResultats=True)
    
    # Enrichir avec pizzas
    if commandes_prete:
        toutes_commandes = commandes_prete
    else:
        toutes_commandes = []
    
    if commandes_en_livraison:
        toutes_commandes = toutes_commandes + commandes_en_livraison

    for commande in toutes_commandes:
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
            
            if garnitures:
                pizza['garnitures'] = garnitures
            else:
                pizza['garnitures'] = []
        
        commande['pizzas'] = pizzas
    
    # Retourner les commandes séparées
    if commandes_prete:
        liste_prete = commandes_prete
    else:
        liste_prete = []
    
    if commandes_en_livraison:
        liste_en_livraison = commandes_en_livraison
    else:
        liste_en_livraison = []
    
    return {
        'prete': liste_prete,
        'en_livraison': liste_en_livraison
    }


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
        SET statut_id = (SELECT id FROM statuts WHERE nom = 'livree'),
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
    """Stats avec 3 compteurs"""
    
    # Prêtes
    query_prete = """
        SELECT COUNT(*) as nombre 
        FROM commandes 
        WHERE statut_id = (SELECT id FROM statuts WHERE nom = 'prete')
    """
    result_prete = ExecuteQuery(query_prete, unResultat=True)
    
    # Récupérées par ce livreur
    query_recuperees = """
        SELECT COUNT(*) as nombre 
        FROM commandes 
        WHERE livreur_id = %s 
        AND statut_id = (SELECT id FROM statuts WHERE nom = 'en_livraison')
    """
    result_recuperees = ExecuteQuery(query_recuperees, (livreur_id,), unResultat=True)
    
    # Livrées par ce livreur
    query_livrees = """
        SELECT COUNT(*) as nombre 
        FROM commandes 
        WHERE livreur_id = %s 
        AND statut_id = (SELECT id FROM statuts WHERE nom = 'livree')
    """
    result_livrees = ExecuteQuery(query_livrees, (livreur_id,), unResultat=True)
    
    # Compteur prêtes
    if result_prete:
        nombre_prete = result_prete['nombre']
    else:
        nombre_prete = 0
    
    # Compteur récupérées
    if result_recuperees:
        nombre_recuperees = result_recuperees['nombre']
    else:
        nombre_recuperees = 0
    
    # Compteur livrées
    if result_livrees:
        nombre_livrees = result_livrees['nombre']
    else:
        nombre_livrees = 0
    
    return {
        'prete': nombre_prete,
        'recuperees': nombre_recuperees,
        'livrees': nombre_livrees
    }



def recuperer_historique_livraisons(livreur_id):
    """
    Récupérer l'historique des livraisons d'un livreur
    
    Paramètres:
        livreur_id: ID du livreur
        
    Retourne:
        Liste des commandes livrées avec détails
    """
    
    query = """
        SELECT 
            c.id as commande_id,
            c.nombre_pizza,
            c.date_commande,
            c.date_livraison,
            a.rue,
            a.ville,
            a.code_postal
        FROM commandes c
        INNER JOIN adresses a ON c.adresse_id = a.id
        WHERE c.livreur_id = %s
        AND c.statut_id = (SELECT id FROM statuts WHERE nom = 'livree')
        ORDER BY c.date_livraison DESC
    """
    
    livraisons = ExecuteQuery(query, (livreur_id,), plusieursResultats=True)
    
    if not livraisons:
        return []
    
    return livraisons