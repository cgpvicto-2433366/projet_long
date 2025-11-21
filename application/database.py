##########################################
# Fichier gérant la connexion à la base  #
# de données et l'exécution des requêtes #
##########################################


import mysql.connector
from mysql.connector import Error
from config import Config 


##########################################
# Connexion à la base de données MySQL ###
##########################################
def open_connection():
    try:
        connection = mysql.connector.connect(
            host=Config.DB_HOST,     
            user=Config.DB_USER,      
            password=Config.DB_PASSWORD,  
            database=Config.DB_NAME,  
            port=Config.DB_PORT      
        )
        return connection
    except Error as e:
        print(f"Erreur de connexion MySQL: {e}")
        return


#########################################################################################################
#                            Fonction pour executer un requête SQL de façon sécurisée                   #
#                                                                                                       # 
# Inspiré de: https://flask.palletsprojects.com/en/stable/patterns/sqlite3/                             #
#                                                                                                       #
#-----------------------------------------------Paramètres----------------------------------------------#
# query : la requête SQL avec des (%s)                                                                  #
# params : les paramètres à passer à la requête [pouvant être un ou plusieurs                           # 
# unResultat : booléen pour indiquer si on veut un seul résultat [dans le cas d'un select avec un id]   #
# plusieursResultats : booléen pour indiquer si on veut tous les résultats [select pour une liste]      #
#########################################################################################################
def ExecuteQuery(query, params=None, unResultat=False, plusieursResultats=False):
    connection = open_connection()
    if not connection:
        raise Exception("Impossible de se connecter à la base de données")
    
    cursor = connection.cursor(dictionary=True)
    
    try:
        connection.start_transaction()
        cursor.execute(query, params or ())
        
        if unResultat:
            result = cursor.fetchone()
        elif plusieursResultats:
            result = cursor.fetchall()
        else:
            result = cursor.lastrowid #par défaut, on retournera l'id du champ impacté 
        
        connection.commit()
        return result
        
    except Error as e:
        connection.rollback()
        raise Exception(f"Erreur lors de l'interrogation de la base de donnée")
        
    finally:
        cursor.close()
        connection.close()



##############################################################################################################
#                  Fonction pour executer une requetes Sql, avec plus d'un tuple de valeur                   #
#                                                                                                            # 
# Inspiré de: https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-executemany.html#
#   https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-rowcount.html                                                                                                         #
#-----------------------------------------------Paramètres---------------------------------------------------#
# query : la requête SQL avec des (%s)                                                                       #
# params : les paramètres à passer à la requête [pouvant être un ou plusieurs tuples]                        #
##############################################################################################################
def ExecuteMany(query, data_list):
    connection = open_connection()
    if not connection:
        raise Exception("Impossible de se connecter")
    
    cursor = connection.cursor(dictionary=True)
    
    try:
        connection.start_transaction()
        cursor.executemany(query, data_list)
        connection.commit()
        return cursor.rowcount
        
    except Error as e:
        connection.rollback()
        raise Exception(f"Erreur SQL: {e}")
        
    finally:
        cursor.close()
        connection.close()