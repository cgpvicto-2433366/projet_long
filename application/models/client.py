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


def recuperer_adresses_clients(idclient):
    lesAdresse = []  

    if idclient:
        queryAdresse = " SELECT id, rue, ville, code_postal FROM adresses WHERE client_id = %s"
        param = (idclient,)
        lesAdresse = ExecuteQuery(queryAdresse, param, plusieursResultats=True)

    return lesAdresse


def creer_nouvelle_adresse(idClient, rue , ville , codePostal):
    if idClient:
        queryAdresse = " INSERT INTO adresses(rue, ville, code_postal, client_id) VALUES (%s, %s, %s, %s)"
        param = (rue, ville, codePostal, idClient)
        adresseId = ExecuteQuery(queryAdresse, param)
        
    return adresseId



def creer_client_invite(nom, prenom, telephone, rue, ville, code_postal):
    """
    Créer un client invité (sans compte utilisateur)
    
    Paramètres:
        nom, prenom, telephone, rue, ville, code_postal
        
    Retourne:
        dict avec client_id et adresse_id
    """
    
    # 1. Créer un utilisateur temporaire
    nom_utilisateur_temp = f"invite_{telephone}"
    courriel_temp = f"{nom_utilisateur_temp}@invite.local"
    
    query_user = """
        INSERT INTO utilisateurs (nom_utilisateur, mot_de_passe, telephone, courriel)
        VALUES (%s, %s, %s, %s)
    """
    utilisateur_id = ExecuteQuery(
        query_user, 
        (nom_utilisateur_temp, '', telephone, courriel_temp)
    )
    
    # 2. Créer le client invité
    query_client = """
        INSERT INTO clients (utilisateur_id, nom, prenom, est_invite)
        VALUES (%s, %s, %s, TRUE)
    """
    client_id = ExecuteQuery(query_client, (utilisateur_id, nom, prenom))
    
    # 3. Créer l'adresse
    query_adresse = """
        INSERT INTO adresses (client_id, rue, ville, code_postal)
        VALUES (%s, %s, %s, %s)
    """
    adresse_id = ExecuteQuery(query_adresse, (client_id, rue, ville, code_postal))
    
    return {
        'client_id': client_id,
        'adresse_id': adresse_id
    }