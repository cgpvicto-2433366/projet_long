-- ============================================
-- Projet : Gestion de Pizzeria
-- Auteur : Ben Schalom KAMGA
-- Date : 2025-11-09
-- Description : Script d'insertion des données de départ
-- ============================================

USE pizzaria_db;

-- Insertion des croutes
INSERT INTO croutes (nom) VALUES
("Classique"), 
("Mince"), 
("Épaisse");

-- Insertion des sauces
INSERT INTO sauces (nom) VALUES 
("Tomate"), 
("Spaghetti"), 
("Alfredo");

-- Insertion des garnitures
INSERT INTO garnitures (nom) VALUES 
("Pepperoni"), 
("Champignons"), 
("Oignons"), 
("Poivrons"), 
("Olives"), 
("Anchois"), 
("Bacon"), 
("Poulet"), 
("Maïs"), 
("Fromage"), 
(" Piments forts");

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