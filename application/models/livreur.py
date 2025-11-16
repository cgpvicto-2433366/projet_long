from application.database import ExecuteQuery, ExecuteMany



# Fonction de creation d'un livreur
# parametres:
# idUtilisateur: l'ID de l'utilisateur dans la table Utilisateurs
# nom: le nom du livreur
# prenom: le prenom du livreur
# type_piece_id: l'ID du type de pièce d'identification
# numero_piece: le numéro de la pièce d'identification
# date_expiration: la date d'expiration de la pièce d'identification
# zones: liste des IDs des zones de livraison
def creerLivreur(idUtilisateur, nom, prenom, type_piece_id, numero_piece, date_expiration, zones):

    queryLivreur = "INSERT INTO livreurs (utilisateur_id, nom, prenom, note) VALUES (%s, %s, %s, 0)"
    paramsLivreur = (idUtilisateur, nom, prenom)
    livreurId= ExecuteQuery(queryLivreur, paramsLivreur)

    queryPiece = "INSERT INTO pieces_identification (livreur_id, types_piece_identification_id, numero, date_expiration) VALUES (%s, %s, %s, %s)"
    paramsPiece = (livreurId, type_piece_id, numero_piece, date_expiration)
    ExecuteQuery(queryPiece, paramsPiece)

    if zones and len(zones) > 0:
        queryZone = "INSERT INTO livreurs_zones (livreur_id, zone_id) VALUES (%s, %s)"
        paramsZone = [(livreurId, zone_id) for zone_id in zones]
        ExecuteMany(queryZone, paramsZone)
    
    return livreurId
