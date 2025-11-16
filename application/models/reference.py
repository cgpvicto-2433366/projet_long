from application.database import ExecuteQuery

# Fonction pour récupérer les types de pièces d'identification
def recuperer_type_de_piece():
    query = "SELECT id, nom FROM types_piece_identification ORDER BY nom" 
    results = ExecuteQuery(query, plusieursResultats=True)

    choices = [('', '-- Choisir --')]
    
     #Transformer le format de resultat retourné par cursor sur forme de dictionnaire en une liste de tuples pour SelectField dans mon WTF forms
    for piece in results:
        piece_id = str(piece['id'])
        piece_nom = piece['nom']
        tuple_piece = (piece_id, piece_nom)
        choices.append(tuple_piece)
    
    return choices

# Fonction pour récupérer les zones de livraison
def recuperer_zone_livraison():
    query = "SELECT id, nom FROM zones ORDER BY nom"
    results = ExecuteQuery(query, plusieursResultats=True)
    
    choices = []

    for zone in results:
        zone_id = str(zone['id'])
        zone_nom = zone['nom']
        tuple_zone = (zone_id, zone_nom)
        choices.append(tuple_zone)
    
    return choices