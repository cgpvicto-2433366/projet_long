import mysql.connector
from mysql.connector import Error
from config import Config 

#Fonction pour creer une connection a ma base de données
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


def execute_query(query, params=None, fetch_one=False, fetch_all=False):
    """
    Exécuter une requête SQL avec gestion de transaction
    """
    connection = open_connection()
    if not connection:
        raise Exception("Impossible de se connecter à la base de données")
    
    cursor = connection.cursor(dictionary=True)
    
    try:
        connection.start_transaction()
        cursor.execute(query, params or ())
        
        if fetch_one:
            result = cursor.fetchone()
        elif fetch_all:
            result = cursor.fetchall()
        else:
            result = cursor.lastrowid
        
        connection.commit()
        return result
        
    except Error as e:
        connection.rollback()
        raise Exception(f"Erreur SQL: {e}")
        
    finally:
        cursor.close()
        connection.close()