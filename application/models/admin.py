from application.database import ExecuteQuery


def recuperer_toutes_commandes(filtre='toutes'):
    """
    Récupérer les commandes selon le filtre
    
    Paramètres:
        filtre: 'toutes', 'nouvelles', 'livrees'
        
    Retourne:
        Liste de commandes avec détails
    """
    
    # Base de la requête
    query = """
        SELECT 
            c.id as commande_id,
            c.date_commande,
            c.date_livraison,
            c.nombre_pizza,
            c.prix,
            s.nom as statut,
            s.id as statut_id,
            cl.nom as client_nom,
            cl.prenom as client_prenom,
            l.nom as livreur_nom,
            l.prenom as livreur_prenom,
            a.rue,
            a.ville,
            a.code_postal
        FROM commandes c
        INNER JOIN statuts s ON c.statut_id = s.id
        INNER JOIN clients cl ON c.client_id = cl.id
        LEFT JOIN livreurs l ON c.livreur_id = l.id
        INNER JOIN adresses a ON c.adresse_id = a.id
    """
    
    # Ajouter filtre
    if filtre == 'nouvelles':
        query += " WHERE s.nom = 'nouvelle'"
    elif filtre == 'livrees':
        query += " WHERE s.nom = 'livree'"
    
    query += " ORDER BY c.date_commande DESC"
    
    commandes = ExecuteQuery(query, plusieursResultats=True)
    
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
            
            if garnitures:
                pizza['garnitures'] = garnitures
            else:
                pizza['garnitures'] = []
        
        commande['pizzas'] = pizzas
    
    return commandes


def recuperer_statistiques_admin():
    """
    Récupérer les statistiques globales
    
    Retourne:
        Dict avec statistiques
    """
    
    # Nouvelles commandes
    query_nouvelles = """
        SELECT COUNT(*) as nombre 
        FROM commandes 
        WHERE statut_id = (SELECT id FROM statuts WHERE nom = 'nouvelle')
    """
    result_nouvelles = ExecuteQuery(query_nouvelles, unResultat=True)
    
    # En cours (préparation + prête + en livraison)
    query_en_cours = """
        SELECT COUNT(*) as nombre 
        FROM commandes 
        WHERE statut_id IN (
            SELECT id FROM statuts 
            WHERE nom IN ('en_preparation', 'prete', 'en_livraison')
        )
    """
    result_en_cours = ExecuteQuery(query_en_cours, unResultat=True)
    
    # Livrées
    query_livrees = """
        SELECT COUNT(*) as nombre 
        FROM commandes 
        WHERE statut_id = (SELECT id FROM statuts WHERE nom = 'livree')
    """
    result_livrees = ExecuteQuery(query_livrees, unResultat=True)
    
    if result_nouvelles:
        nb_nouvelles = result_nouvelles['nombre']
    else:
        nb_nouvelles = 0
    
    if result_en_cours:
        nb_en_cours = result_en_cours['nombre']
    else:
        nb_en_cours = 0
    
    if result_livrees:
        nb_livrees = result_livrees['nombre']
    else:
        nb_livrees = 0
    
    return {
        'nouvelles': nb_nouvelles,
        'en_cours': nb_en_cours,
        'livrees': nb_livrees
    }


def modifier_statut_commande(commande_id, nouveau_statut):
    """
    Modifier le statut d'une commande et mettre à jour les dates
    
    Paramètres:
        commande_id: ID de la commande
        nouveau_statut: Nom du nouveau statut
    """
    
    # Récupérer l'ID du statut
    query_statut = "SELECT id FROM statuts WHERE nom = %s"
    statut = ExecuteQuery(query_statut, (nouveau_statut,), unResultat=True)
    
    if not statut:
        raise ValueError("Statut invalide")
    
    statut_id = statut['id']
    
    # Mettre à jour selon le statut
    if nouveau_statut == 'livree':
        # Marquer comme livrée avec date
        query = """
            UPDATE commandes 
            SET statut_id = %s, date_livraison = NOW()
            WHERE id = %s
        """
        ExecuteQuery(query, (statut_id, commande_id))
    else:
        # Juste changer le statut
        query = "UPDATE commandes SET statut_id = %s WHERE id = %s"
        ExecuteQuery(query, (statut_id, commande_id))