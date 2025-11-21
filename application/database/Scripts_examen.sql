-- ================================================================================================================
-- Projet : Gestion de Pizzeria
-- Auteur : Ben Schalom KAMGA
-- Date : 2025-11-09
-- Description : Script d'execution pour l'examen
-- ================================================================================================================



-- ================================================================================================================
-- Scripts de création
-- ================================================================================================================

DROP DATABASE IF EXISTS pizzeria_db;

CREATE DATABASE pizzaria_db;

USE pizzaria_db;

-- ============================================
-- GROUPE 1 : Tables de référence: 
-- [types_piece_identification, zones,  
-- croutes, sauces, garnitures, statuts, 
-- taxes ]
-- ============================================

-- type de pièce d'identification des livreurs
CREATE TABLE types_piece_identification (
    id  INT AUTO_INCREMENT  PRIMARY KEY,
    nom VARCHAR(255) NOT NULL UNIQUE
);

-- Zone où le restaurant permet de faire des livraisons 
-- [Dans l'amélioration de mon projet, j'utiliserai cette table
-- afin de pouvoir organisé les commandes dans l'espace des livreurs en
-- fonction de leur zone de livraison]
CREATE TABLE zones (
    id  INT AUTO_INCREMENT  PRIMARY KEY,
    nom VARCHAR(255) NOT NULL UNIQUE
);

-- taille de pizza possible
CREATE TABLE tailles(
    id  INT AUTO_INCREMENT  PRIMARY KEY,
    nom VARCHAR(50) NOT NULL UNIQUE,
    prix DECIMAL(10,2) NOT NULL
);

-- type de croutes de pizza possible 
CREATE TABLE croutes (
    id  INT AUTO_INCREMENT  PRIMARY KEY,
    nom VARCHAR(50) NOT NULL UNIQUE,
    prix DECIMAL(10,2) NOT NULL
);

-- type de sauces de pizza possible 
CREATE TABLE sauces (
    id  INT AUTO_INCREMENT  PRIMARY KEY,
    nom VARCHAR(50) NOT NULL UNIQUE,
    prix DECIMAL(10,2) NOT NULL
);

-- type de garnitures de pizza possible 
CREATE TABLE garnitures (
    id  INT AUTO_INCREMENT  PRIMARY KEY,
    nom VARCHAR(50) NOT NULL UNIQUE,
    prix DECIMAL(10,2) NOT NULL
);

-- type d'une commande: [envoye a la pizzaria, en cours de préparation, prêt a être livré, en cours de livraison, proche de vous, commande livré]
CREATE TABLE statuts (
    id  INT AUTO_INCREMENT  PRIMARY KEY,
    nom VARCHAR(50) NOT NULL UNIQUE
);

-- ============================================
-- GROUPE 2 : Tables utilisateurs
-- ============================================

-- les utilisateurs de l'application [clients, livreurs]
CREATE TABLE utilisateurs(
    id  INT AUTO_INCREMENT  PRIMARY KEY,
    nom_utilisateur VARCHAR(50) NOT NULL UNIQUE,
    mot_de_passe VARCHAR(255) NOT NULL,
    telephone CHAR(20)  NOT NULL UNIQUE,
    courriel VARCHAR(255) NOT NULL UNIQUE,
    date_creation DATETIME DEFAULT NOW(),  
    est_admin BOOLEAN DEFAULT FALSE, -- permet de distinguer si l'utilisateur est un admin ou pas, ainsi il pourra faire des actions précises que les autres ne pourront pas faire.

    CONSTRAINT check_regex_courriel CHECK (courriel REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$') 
);

-- ================================================
-- GROUPE 3 : Tables de rôles [clients, livreurs]
-- ================================================

-- Les utilisateurs de type clients
CREATE TABLE clients (
    id  INT AUTO_INCREMENT  PRIMARY KEY,
    nom VARCHAR(50) NOT NULL,
    prenom VARCHAR(50) NOT NULL,
    est_invite BOOLEAN DEFAULT FALSE,
    utilisateur_id INT NOT NULL,

    FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id) ON DELETE CASCADE -- si l'utilisateur est supprimé, alors on le supprime de la table client dans le cas où il s'agissait d'un client
);

-- Les utilisateurs de type livreurs
CREATE TABLE livreurs (
    id  INT AUTO_INCREMENT  PRIMARY KEY,
    nom VARCHAR(50) NOT NULL,
    prenom VARCHAR(50) NOT NULL,
    nombre_livraison INT,
    utilisateur_id INT NOT NULL,

    FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id) ON DELETE CASCADE -- si l'utilisateur est supprimé, alors on le supprime de la table livreurs dans le cas où il s'agissait d'un livreur
);


-- ======================================================================================
-- GROUPE 4 : Tables des détails sur les livreurs [pieces_identification, zone_livraison]
-- ======================================================================================

-- Informations sur la pièce d'identification
CREATE TABLE pieces_identification (
    id  INT AUTO_INCREMENT  PRIMARY KEY,
    numero VARCHAR(255) NOT NULL UNIQUE,
    date_expiration DATE NOT NULL,
    types_piece_identification_id INT NOT NULL,
    livreur_id INT NOT NULL,
    
    FOREIGN KEY (livreur_id) REFERENCES livreurs(id) ON DELETE CASCADE, -- si le livreur est supprimé on supprime ces pieces d'identification
    FOREIGN KEY (types_piece_identification_id) REFERENCES types_piece_identification(id),
    UNIQUE(types_piece_identification_id, livreur_id)
);

-- Zones de livraisons couvertes par chaque livreur
CREATE TABLE livreurs_zones (
    id  INT AUTO_INCREMENT  PRIMARY KEY,
    zone_id INT NOT NULL,
    livreur_id INT NOT NULL,

    FOREIGN KEY (zone_id) REFERENCES zones(id),
    FOREIGN KEY (livreur_id) REFERENCES livreurs(id) ON DELETE CASCADE,
    UNIQUE(zone_id, livreur_id)
);

-- ================================================
-- GROUPE 5 : adreses des clients [adresses]
-- ================================================

-- adresses de chaque clients
CREATE TABLE adresses(
    id INT AUTO_INCREMENT PRIMARY KEY,
    ville VARCHAR(50) NOT NULL,
    rue VARCHAR(50) NOT NULL,
    code_postal CHAR(7) NOT NULL,
    client_id INT NOT NULL,

    FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE CASCADE,
    UNIQUE(client_id, code_postal)
);


-- ================================================
-- GROUPE 6 : Tables de gestions des commandes [commandes, commandes_taxes, commandes_en_attente]
-- ================================================

-- les commandes 
CREATE TABLE commandes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date_commande DATETIME NOT NULL DEFAULT NOW(),
    date_prise_en_charge DATETIME, -- lorsque on commence a la préparer
    date_commande_prete DATETIME, -- La commande est prête et en attente d'être ramassé par un livreur
    date_recuperation_livreur DATETIME, -- le livreur a recupérer la commande
    date_livraison DATETIME, -- la commande a été livrée
    prix DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    statut_id INT NOT NULL, 
    client_id INT NOT NULL,
    livreur_id INT, -- au moment de la commande on a pas de livreur associé
    adresse_id  INT NOT NULL,
    instructions TEXT,
    nombre_pizza INT,

    FOREIGN KEY (statut_id) REFERENCES statuts(id),
    FOREIGN KEY (client_id) REFERENCES clients(id),
    FOREIGN KEY (livreur_id) REFERENCES livreurs(id),
    FOREIGN KEY (adresse_id) REFERENCES adresses(id)
);


-- Liste des commandes en attente (uniquement les nouvelles commandes)
CREATE TABLE commandes_en_attente (
    id INT AUTO_INCREMENT PRIMARY KEY,
    commande_id INT NOT NULL,
    date_ajout DATETIME,

    FOREIGN KEY (commande_id) REFERENCES commandes(id)
);



-- ====================================================================
-- GROUPE 6 : Tables de gestions des pizzas [pizzas, pizzas_garnitures]
-- ====================================================================

-- information sur la pizza commande par le client
CREATE TABLE pizzas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(50) NOT NULL,
    sauce_id INT NOT NULL,
    croute_id INT NOT NULL,
    commande_id INT NOT NULL,
    taille_id INT NOT NULL,

    FOREIGN KEY (taille_id) REFERENCES tailles(id),
    FOREIGN KEY (sauce_id) REFERENCES sauces(id),
    FOREIGN KEY (croute_id) REFERENCES croutes(id),
    FOREIGN KEY (commande_id) REFERENCES commandes(id)
);

-- Les garnitures choisit par le client [max 4]
CREATE TABLE pizzas_garnitures(
    id INT AUTO_INCREMENT PRIMARY KEY,
    garniture_id INT NOT NULL,
    pizza_id INT NOT NULL,

    FOREIGN KEY (garniture_id) REFERENCES garnitures(id),
    FOREIGN KEY (pizza_id) REFERENCES pizzas(id)
);


-- ================================================================================================================
-- Scripts de création des triggers
-- ================================================================================================================

USE pizzaria_db;

DELIMITER $$

-- ============================================
-- TRIGGER 1 : Ajouter automatiquement les nouvelles commandes à la file d'attente
-- ============================================

CREATE TRIGGER nouvelle_commande
AFTER INSERT ON commandes
FOR EACH ROW
BEGIN
    -- Gestion d'erreur
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Erreur lors de l\'ajout de la commande à la file d\'attente';
    END;

    -- action
    INSERT INTO commandes_en_attente (commande_id, date_ajout) VALUES (NEW.id, NOW());

END$$

DELIMITER ;

-- ============================================
-- TRIGGER 2 : Retirer les commandes prêtes de la file d'attente
-- ============================================

DELIMITER $$

CREATE TRIGGER retirer_commande_file_attente
AFTER UPDATE ON commandes
FOR EACH ROW
BEGIN
    DECLARE id_prete INT;
    -- Gestion d'erreur
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Erreur lors de la mise à jour du statut de la commande';
    END;

    -- action:
    -- si le statut de la commande change et devient "prete"
    -- on la retire de la file d'attente
    SELECT (id) INTO id_prete FROM statuts  WHERE nom= 'prete';

    IF((NEW.statut_id = id_prete) AND (OLD.statut_id != NEW.statut_id)) THEN
        DELETE FROM commandes_en_attente WHERE commande_id = NEW.id;
    END IF;
END$$

DELIMITER ;


-- ================================================================================================================
-- Scripts d'insertion des données par défaut
-- ================================================================================================================
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


-- ================================================================================================================
-- Scripts d'insertion des données test
-- ================================================================================================================


-- 3 utilisateurs  test

-- Jean Tremblay - Client régulier
-- Marie Dubois - Cliente avec points de fidélité
-- Pierre Gagnon - Nouveau client

-- 2 Livreurs :

-- François Leblanc - Livreur en voiture (avec permis)
-- Sophie Martin - Livreuse à vélo (avec carte d'identité)

-- 1 Admin (Pizzeria) :

-- Admin Pizzeria - Compte administrateur


USE pizzaria_db;


-- ADMIN (Pizzeria)
INSERT INTO utilisateurs (nom_utilisateur, mot_de_passe, telephone, courriel, est_admin) VALUES
('admin', SHA2('password123', 256), '819-555-0000', 'admin@pizzeria.com', TRUE);

-- Utilisateurs
INSERT INTO utilisateurs (nom_utilisateur, mot_de_passe, telephone, courriel, est_admin) VALUES
('jean_t', SHA2('password123', 256), '819-555-0001', 'jean.tremblay@email.com', FALSE),
('marie_d', SHA2('password123', 256), '819-555-0002', 'marie.dubois@email.com', FALSE),
('pierre_g', SHA2('password123', 256), '819-555-0003', 'pierre.gagnon@email.com', FALSE),
('francois_l', SHA2('password123', 256), '819-555-0004', 'francois.leblanc@email.com', FALSE),
('sophie_m', SHA2('password123', 256), '819-555-0005', 'sophie.martin@email.com', FALSE);

-- ============================================
-- Profils clients
-- ============================================

INSERT INTO clients (nom, prenom, points_fidelite, utilisateur_id) VALUES
('Tremblay', 'Jean', 0, (SELECT id FROM utilisateurs WHERE nom_utilisateur = 'jean_t')),
('Dubois', 'Marie', 50, (SELECT id FROM utilisateurs WHERE nom_utilisateur = 'marie_d')),
('Gagnon', 'Pierre', 0, (SELECT id FROM utilisateurs WHERE nom_utilisateur = 'pierre_g'));

-- ============================================
-- Adresses des clients
-- ============================================

INSERT INTO adresses (ville, rue, code_postal, client_id) VALUES
('Victoriaville', '123 Rue Principale', 'G6P 1A1', 
 (SELECT id FROM clients WHERE nom = 'Tremblay' AND prenom = 'Jean')),
 
('Victoriaville', '456 Avenue des Érables', 'G6P 2B2',  
 (SELECT id FROM clients WHERE nom = 'Dubois' AND prenom = 'Marie')),
 
('Trois-Rivières', '789 Boulevard des Forges', 'G8Z 3C3',
 (SELECT id FROM clients WHERE nom = 'Gagnon' AND prenom = 'Pierre'));

-- ============================================
-- Profils livreurs
-- ============================================

INSERT INTO livreurs (nom, prenom, note, utilisateur_id) VALUES
('Leblanc', 'François', 4.8, (SELECT id FROM utilisateurs WHERE nom_utilisateur = 'francois_l')),
('Martin', 'Sophie', 4.9, (SELECT id FROM utilisateurs WHERE nom_utilisateur = 'sophie_m'));

-- ============================================
-- Pièces d'identification des livreurs
-- ============================================

-- François Leblanc - Permis de conduire + Carte d'identité
INSERT INTO pieces_identification (numero, date_expiration, types_piece_identification_id, livreur_id) VALUES
('L1234-567890-12345', '2027-12-31', 
 (SELECT id FROM types_piece_identification WHERE nom = "Permis de conduire"),
 (SELECT id FROM livreurs WHERE nom = "Leblanc" AND prenom = "François")),

("AB-123456", "2026-06-30", 
 (SELECT id FROM types_piece_identification WHERE nom = "Carte d'identité"),
 (SELECT id FROM livreurs WHERE nom = "Leblanc" AND prenom = "François"));

-- Sophie Martin - Carte d'identité
INSERT INTO pieces_identification (numero, date_expiration, types_piece_identification_id, livreur_id) VALUES
("CD-789012", "2028-03-15", 
 (SELECT id FROM types_piece_identification WHERE nom = "Carte d'identité"),
 (SELECT id FROM livreurs WHERE nom = "Martin" AND prenom = "Sophie"));

-- ============================================
-- Zones de livraison des livreurs
-- ============================================

-- François Leblanc livre en voiture (3 zones)
INSERT INTO livreurs_zones (zone_id, livreur_id) VALUES
((SELECT id FROM zones WHERE nom = "Victoriaville"), 
 (SELECT id FROM livreurs WHERE nom = "Leblanc" AND prenom = "François")),
 
((SELECT id FROM zones WHERE nom = "Drummondville"), 
 (SELECT id FROM livreurs WHERE nom = "Leblanc" AND prenom = "François")),
 
((SELECT id FROM zones WHERE nom = "Bécancour"), 
 (SELECT id FROM livreurs WHERE nom = "Leblanc" AND prenom = "François"));

-- Sophie Martin livre à vélo (2 zones locales)
INSERT INTO livreurs_zones (zone_id, livreur_id) VALUES
((SELECT id FROM zones WHERE nom = "Victoriaville"), 
 (SELECT id FROM livreurs WHERE nom = "Martin" AND prenom = "Sophie")),
 
((SELECT id FROM zones WHERE nom = "Trois-Rivières"), 
 (SELECT id FROM livreurs WHERE nom = "Martin" AND prenom = "Sophie"));
