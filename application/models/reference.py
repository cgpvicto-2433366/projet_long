from application.database import ExecuteQuery


def recuperer_type_de_piece():
    query = "SELECT id, nom FROM types_piece_identification ORDER BY nom" 
    results = ExecuteQuery(query, plusieursResultats=True)

    # Liste avec option vide au debut
    choices = [('', '-- Choisir --')]
    
    # Ajouter chaque piece
    for piece in results:
        piece_id = str(piece['id'])
        piece_nom = piece['nom']
        choices.append((piece_id, piece_nom))
    
    return choices


def recuperer_zone_livraison():
    query = "SELECT id, nom FROM zones ORDER BY nom"
    results = ExecuteQuery(query, plusieursResultats=True)
    
    choices = []
    for zone in results:
        zone_id = str(zone['id'])
        zone_nom = zone['nom']
        choices.append((zone_id, zone_nom))
    
    return choices


def recuperer_format_pizza():
    query = "SELECT id, nom, prix FROM tailles ORDER BY prix"
    results = ExecuteQuery(query, plusieursResultats=True)
    
    choices = []
    for taille in results:
        taille_id = str(taille['id'])
        label = taille['nom'] + " - " + str(taille['prix']) + "$"
        choices.append((taille_id, label))
    
    return choices


def recuperer_croutes_pizza():
    query = "SELECT id, nom, prix FROM croutes ORDER BY nom"
    results = ExecuteQuery(query, plusieursResultats=True)
    
    choices = []
    for croute in results:
        croute_id = str(croute['id'])
        label = croute['nom'] + " - " + str(croute['prix']) + "$"
        choices.append((croute_id, label))
    
    return choices


def recuperer_sauces_pizza():
    query = "SELECT id, nom, prix FROM sauces ORDER BY nom"
    results = ExecuteQuery(query, plusieursResultats=True)
    
    choices = []
    for sauce in results:
        sauce_id = str(sauce['id'])
        label = sauce['nom'] + " - " + str(sauce['prix']) + "$"
        choices.append((sauce_id, label))
    
    return choices


def recuperer_garnitures_pizza():
    query = "SELECT id, nom, prix FROM garnitures ORDER BY nom"
    results = ExecuteQuery(query, plusieursResultats=True)
    
    choices = []
    for garniture in results:
        garniture_id = str(garniture['id'])
        label = garniture['nom'] + " (+" + str(garniture['prix']) + "$)"
        choices.append((garniture_id, label))
    
    return choices


# ==================== FONCTIONS POUR CALCULER LES PRIX ====================

def recuperer_prix(table, element_id):
    
    query = "SELECT prix FROM " + table + " WHERE id = %s"
    resultat = ExecuteQuery(query, (element_id,), unResultat=True)
    
    # Si l'element existe, retourner son prix
    if resultat:
        return float(resultat['prix'])
    else:
        return 0.0


def recuperer_info_complete(table, element_id):
    
    query = "SELECT * FROM " + table + " WHERE id = %s"
    return ExecuteQuery(query, (element_id,), unResultat=True)


def recuperer_taxes():
    query = "SELECT id, nom, taux FROM taxes ORDER BY nom"
    return ExecuteQuery(query, plusieursResultats=True)


def enrichir_panier(panier):
    
    panier_avec_noms = []
    
    # Pour chaque pizza dans le panier
    for pizza in panier:
        # Recuperer les informations de chaque ingredient
        info_taille = recuperer_info_complete('tailles', pizza['taille_id'])
        info_sauce = recuperer_info_complete('sauces', pizza['sauce_id'])
        info_croute = recuperer_info_complete('croutes', pizza['croute_id'])
        
        # Recuperer les noms des garnitures
        noms_garnitures = []
        for garniture_id in pizza['garnitures']:
            info_garniture = recuperer_info_complete('garnitures', garniture_id)
            if info_garniture:
                noms_garnitures.append(info_garniture['nom'])
        
        # Calculer le prix total de la pizza
        prix_total = 0
        
        # Ajouter le prix de la taille
        if info_taille:
            prix_total = prix_total + float(info_taille['prix'])
        
        # Ajouter le prix de la sauce
        if info_sauce:
            prix_total = prix_total + float(info_sauce['prix'])
        
        # Ajouter le prix de la croute
        if info_croute:
            prix_total = prix_total + float(info_croute['prix'])
        
        # Ajouter le prix de chaque garniture
        for garniture_id in pizza['garnitures']:
            prix_garniture = recuperer_prix('garnitures', garniture_id)
            prix_total = prix_total + prix_garniture
        
        # Creer la pizza avec les noms et le prix
        pizza_complete = {
            'taille': info_taille['nom'] if info_taille else 'Inconnue',
            'sauce': info_sauce['nom'] if info_sauce else 'Inconnue',
            'croute': info_croute['nom'] if info_croute else 'Inconnue',
            'garnitures': noms_garnitures,
            'prix': prix_total,
            # Garder les IDs pour l'enregistrement
            'taille_id': pizza['taille_id'],
            'sauce_id': pizza['sauce_id'],
            'croute_id': pizza['croute_id'],
            'garnitures_ids': pizza['garnitures']
        }
        
        panier_avec_noms.append(pizza_complete)
    
    return panier_avec_noms