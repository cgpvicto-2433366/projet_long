# Application de livraison de pizza : Ben Schalom KAMGA 2433366

# Contexte

Dans le cadre du cours de Bases de Données 2, vous êtes chargé de développer une application Web en Python pour la gestion d'une pizzeria. L'application doit permettre de prendre des commandes de pizzas pour la livraison en utilisant une base de données MySQL.

# Objectifs

Votre programme devra permettre aux clients de fournir leur nom, numéro de téléphone, adresse de livraison et de choisir les détails de leur pizza. La personnalisation de la pizza comprend le choix de la croûte, de la sauce et des garnitures.

# Spécifications de la pizza

Types de Croûtes : Classique, Mince, Épaisse
Choix de Sauces : Tomate, Spaghetti, Alfredo
Choix de Garnitures (maximum 4) : Pepperoni, Champignons, Oignons, Poivrons, Olives, Anchois, Bacon, Poulet, Maïs, Fromage, Piments forts

# Nouveaux Rôles:

Client : Passe des commandes
Cuisinier : Voit les nouvelles commandes, marque comme "en préparation" puis "prête"
Livreur : Voit les commandes prêtes, les prend en charge et marque comme "livrée"

# Structure du projet 
PIZZARIA/
├── app.py                  # Point d’entrée principal de l’application Flask
├── config.py               # Fichier de configuration global (utilise les variables .env)
├── .env                    # Variables sensibles (clé secrète, accès MySQL)
├── .env.example            # Exemple de fichier .env pour le partage sans secrets
├── requirements.txt        # Liste des dépendances Python
├── application/            # Dossier principal de l’application
│   ├── __init__.py         # Initialise l’app Flask et enregistre les routes
│   ├── routes/             # Fichiers de routes (endpoints Flask)
│   │   └── pizzas.py       # Routes liées aux pizzas
│   ├── models/             # Modèles de données (si utilisés sans ORM)
│   ├── forms/              # Formulaires Flask-WTF (si utilisés)
│   ├── templates/          # Fichiers HTML (Jinja2)
│   │   └── tests/          # Dossier prévu pour les templates de test
│   ├── static/             # Fichiers statiques (CSS, JS, images)
│   │   ├── css/            # Feuilles de style
│   │   └── images/         # Images du site
│   ├── database/           # Scripts SQL pour la base de données
│   │   └── schemas.sql     # Script de création des tables
│   └── client.sql          # Script SQL spécifique aux clients
├── diagramme/              # Diagrammes de conception (Draw.io)
│   ├── db_classe.drawio    # Diagramme des classes
│   ├── db_entite.drawio    # Diagramme des entités
└── __pycache__/            # Dossiers de cache Python (automatiquement générés)


-------------------------------------------------------------------------------------------------------------------------------------------

# Sprint1: Fondations et Base de données avec Utilisateurs
    -- Objectif: BD fonctionnelle avec système d'authentification

    * Etape1: Modelisation de la BD [diagramme de classe et d'entité]
    * Etape2: Création des scripts



