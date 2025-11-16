from application.database import ExecuteQuery



# Fonction de creation d'un client
# parametres:
# idUtilisateur: l'ID de l'utilisateur dans la table Utilisateurs
# nom: le nom du client
# prenom: le prenom du client
# ville: la ville du client
# adresse: l'adresse du client
# codePostal: le code postal du client
# retourne: l'ID du client créé
def CreerClient(idUtilisateur, nom, prenom, ville, rue, codePostal):

    queryClient = "INSERT INTO Clients (utilisateur_id, nom, prenom, points_fidelite) VALUES (%s, %s, %s, 0)"
    paramsClient = (idUtilisateur, nom, prenom)
    clientId= ExecuteQuery(queryClient, paramsClient)

    query="INSERT INTO adresses(client_id, ville, rue, code_postal) VALUES (%s, %s, %s, %s)"
    paramsAdresse = (clientId, ville, rue, codePostal)
    ExecuteQuery(query, paramsAdresse)

    return clientId