from application.database import ExecuteQuery, ExecuteMany

def creer_commande_complete(client_id, panier, livraison):

    total = sum([pizza['prix'] for pizza in panier]) * 1.14975
    compteur = len(panier)


    # 1. Créer la commande 
    queryCommande = "INSERT INTO commandes (client_id, nombre_pizza, date_commande, statut_id, prix, adresse_id ,instructions) VALUES (%s, %s, NOW(), 1,%s, %s, %s)"
    paramsCommande = (client_id, compteur, total, livraison['adresseId'], livraison['instruction'])
    
    commande_id = ExecuteQuery(queryCommande, paramsCommande)
    
    # 2. Pour chaque pizza dans le panier
    for pizza in panier:

        queryPizza = "INSERT INTO pizzas (nom, commande_id, taille_id, croute_id, sauce_id)  VALUES (%s, %s, %s, %s, %s)"
        paramsPizza= (
            pizza['nom'],
            commande_id,
            pizza['taille_id'],
            pizza['croute_id'],
            pizza['sauce_id']
        )

        pizza_id = ExecuteQuery( queryPizza,paramsPizza)
        
 
        if pizza.get('garnitures'):
            queryGarnitures = "INSERT INTO pizzas_garnitures (pizza_id, garniture_id) VALUES (%s, %s) "
            paramsGarnitures = [(pizza_id, g_id) for g_id in pizza['garnitures']]
            ExecuteMany(queryGarnitures, paramsGarnitures)
    
    return commande_id



# historique de commande du client
def recuperer_historique_commandes(client_id):
    """
    Récupérer l'historique des commandes d'un client
    
    Paramètres:
        client_id: ID du client
        
    Retourne:
        Liste de commandes avec leurs pizzas
    """
    
    # Récupérer les commandes
    query_commandes = """
        SELECT 
            c.id as commande_id,
            c.date_commande,
            c.date_livraison,
            c.prix,
            c.nombre_pizza,
            s.nom as statut,
            a.rue,
            a.ville,
            a.code_postal
        FROM commandes c
        LEFT JOIN statuts s ON c.statut_id = s.id
        LEFT JOIN adresses a ON c.adresse_id = a.id
        WHERE c.client_id = %s
        ORDER BY c.date_commande DESC
    """
    
    commandes = ExecuteQuery(query_commandes, (client_id,), plusieursResultats=True)
    
    if not commandes:
        return []
    
    # Pour chaque commande, récupérer ses pizzas
    for commande in commandes:
        commande_id = commande['commande_id']
        
        # Récupérer les pizzas de cette commande
        query_pizzas = """
            SELECT 
                p.id as pizza_id,
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
        
        # Pour chaque pizza, récupérer ses garnitures
        for pizza in pizzas:
            pizza_id = pizza['pizza_id']
            
            query_garnitures = """
                SELECT g.nom
                FROM pizzas_garnitures pg
                JOIN garnitures g ON pg.garniture_id = g.id
                WHERE pg.pizza_id = %s
            """
            
            garnitures = ExecuteQuery(query_garnitures, (pizza_id,), plusieursResultats=True)
            
            # Ajouter les garnitures à la pizza
            pizza['garnitures'] = garnitures if garnitures else []
        
        # Ajouter les pizzas à la commande
        commande['pizzas'] = pizzas
    
    return commandes