-- ============================================
-- Projet : Gestion de Pizzeria
-- Auteur : Ben Schalom KAMGA
-- Date : 2025-11-09
-- Description : Script d'insertion des données de départ
-- ============================================

USE pizzaria_db;

-- Insertion des croutes
INSERT INTO croutes (nom, prix) VALUES
("Classique", 3.50), 
("Mince", 4.00), 
("Épaisse", 6.50);

-- Insertion des sauces
INSERT INTO sauces (nom, prix) VALUES 
("Tomate", 5.10), 
("Spaghetti", 4.50), 
("Alfredo",9.00);

-- Insertion des garnitures
INSERT INTO garnitures (nom, prix) VALUES 
("Pepperoni", 1.50), 
("Jambon", 1.80), 
("Saucisson", 2.00),
("Saucisse",3.00), 
("Ananas", 1.20),
("Champagne", 2.50),
("Champignons", 1.00), 
("Oignons", 0.80), 
("Poivrons", 0.90), 
("Olives",4.00), 
("Anchois", 2.20), 
("Bacon", 2.30), 
("Poulet", 3.50), 
("Maïs",2.00), 
("Fromage", 2.50), 
(" Piments forts", 1.70);

-- Insérer les statuts des commandes
INSERT INTO statuts (nom) VALUES
("nouvelle"),
("en_preparation"),
("prete"),
("en_livraison"),
("livree");

-- Insérer les taxes
INSERT INTO taxes (nom, taux) VALUES
("TPS", 0.05),      
("TVQ", 0.09975); 

-- taille de pizza 
INSERT INTO tailles (nom, prix) VALUES
("petite", 5),      
("moyenne", 7.5), 
("grande", 10);

-- Insérer les types de pièces d'identification
INSERT INTO types_piece_identification (nom) VALUES
("Permis de conduire"),
("Carte d'identité"),
("Passeport");

-- Insérer les zones de livraison
INSERT INTO zones (nom) VALUES
("Victoriaville"),
("Trois-Rivières"),
("Drummondville"),
("Shawinigan"),
("Bécancour");