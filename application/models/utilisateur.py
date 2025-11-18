#########################################
# Fichier contenant les methodes liées  #
# aux utilisateurs (modèle Utilisateur) #
# - Inscription                         #
# - Connexion                           #
# - Déconnexion                         #
#########################################


from application.database import ExecuteQuery
from application.models.client import CreerClient
from application.models.livreur import creerLivreur
import hashlib # Pour le hachage des mots de passe


def CreerUtilisateur(nomUtilisateur, password, telephone, courriel, typeCompte, nom, prenom, typePiece=None, numeroPiece=None, dateExpiration=None, zones=None, ville=None, rue=None, codePostal=None):
    # Hachage du mot de passe
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    query = "INSERT INTO Utilisateurs (nom_utilisateur, mot_de_passe, telephone, courriel) VALUES (%s, %s, %s, %s)"
    params = (nomUtilisateur, hashed_password, telephone, courriel)
    
    utilisateur_id = ExecuteQuery(query, params) # dans ce cas utilisateur ID contiendra l'ID du nouvel utilisateur

    clientId= None
    livreurId= None
    
    if(typeCompte == 'client'):
        clientId= CreerClient(utilisateur_id, nom, prenom, ville, rue, codePostal)
    elif(typeCompte == 'livreur'):
        livreurId= creerLivreur(utilisateur_id, nom, prenom, typePiece, numeroPiece, dateExpiration, zones)
    else:
        raise ValueError("Type de compte inconnu.")

    resultat= {
        "utilisateurId": utilisateur_id,
        "clientId": clientId,
        "livreurId": livreurId
    }

    return resultat



# Fonction pour vérifier les identifiants de connexion
## parametres:
# courriel: le courriel de l'utilisateur
# password: le mot de passe de l'utilisateur
# typeCompte: le type de compte choisi (client ou livreur)
# retourne: un dictionnaire avec les informations de l'utilisateur si la connexion est réussie, sinon None
def Connexion(courriel, password, typeCompte):

    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    # Vérifier dans utilisateurs
    query = "SELECT id, nom_utilisateur, courriel, est_admin FROM utilisateurs WHERE courriel = %s AND mot_de_passe = %s"
    paramsUtilisateur = (courriel, hashed_password)
    user = ExecuteQuery(query, paramsUtilisateur, unResultat=True)
    
    if not user:
        return None  # utilisateur non trouvé ou mot de passe incorrect
    
    
    # Vérifier le rôle selon le type de compte choisi
    if typeCompte == 'client':
        queryClient = "SELECT id, nom, prenom FROM clients WHERE utilisateur_id = %s "
        client = ExecuteQuery(queryClient, (user['id'],), unResultat=True)
        
        # Si un client est trouvé, retourner les informations
        if client:
            return {
                'utilisateurId': user['id'],
                'nomUtilisateur': user['nom_utilisateur'],
                'roleId': client['id'],
                'role': 'client',
                'nom': client['nom'],
                'prenom': client['prenom']
            }
        else:
            return None
    
    elif typeCompte == 'livreur':
        query_livreur = "SELECT id, nom, prenom FROM livreurs WHERE utilisateur_id = %s"
        livreur = ExecuteQuery(query_livreur, (user['id'],), unResultat=True)
        
        if livreur:
            return {
                'utilisateurId': user['id'],
                'nomUtilisateur': user['nom_utilisateur'],
                'role': 'livreur',
                'roleId': livreur['id'],
                'nom': livreur['nom'],
                'prenom': livreur['prenom']
            }
        else:
            return None
    
    return None  # Type de compte incorrect pour cet utilisateur