from application.database import get_db_connection

# Tester la connexion
connection = get_db_connection()

if connection:
    print("Connexion à MySQL réussie!")
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) as total FROM utilisateurs")
    result = cursor.fetchone()
    print(f"📊 Nombre d'utilisateurs: {result[0]}")
    connection.close()
else:
    print(" Connexion échouée")