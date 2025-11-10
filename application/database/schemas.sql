-- ============================================
-- Projet : Gestion de Pizzeria
-- Auteur : Ben Schalom KAMGA
-- Date : 2025-11-09
-- Description : Script de création de la base de données
-- ============================================

DROP DATABASE IF EXISTS pizzeria_db;

CREATE DATABASE pizzeria_db;

USE pizzeria_db;

-- ============================================
-- GROUPE 1 : Tables de référence: [types_piece_identification, zones,  croutes, sauces, garnitures, statuts, taxes ]
-- ============================================

-- type de pièce d'identification des livreurs
CREATE TABLE types_piece_identification (
    id  INT AUTO_INCREMENT  PRIMARY KEY,
    nom VARCHAR(255) NOT NULL UNIQUE
);

-- Zone où le restaurant permet de faire des livraisons
CREATE TABLE zones (
    id  INT AUTO_INCREMENT  PRIMARY KEY,
    nom VARCHAR(255) NOT NULL UNIQUE
);

-- type de croutes de pizza possible 
CREATE TABLE croutes (
    id  INT AUTO_INCREMENT  PRIMARY KEY,
    nom VARCHAR(50) NOT NULL UNIQUE
);

-- type de sauces de pizza possible 
CREATE TABLE sauces (
    id  INT AUTO_INCREMENT  PRIMARY KEY,
    nom VARCHAR(50) NOT NULL UNIQUE
);

-- type de garnitures de pizza possible 
CREATE TABLE garnitures (
    id  INT AUTO_INCREMENT  PRIMARY KEY,
    nom VARCHAR(50) NOT NULL UNIQUE
);

-- type d'une commande: [envoye a la pizzaria, en cours de préparation, prêt a être livré, en cours de livraison, proche de vous, commande livré]
CREATE TABLE statuts (
    id  INT AUTO_INCREMENT  PRIMARY KEY,
    nom VARCHAR(50) NOT NULL UNIQUE
);

-- Les differentes taxes pouvant être appliquées sur une commande de pizza
CREATE TABLE taxes (
    id  INT AUTO_INCREMENT  PRIMARY KEY,
    nom VARCHAR(50) NOT NULL UNIQUE,
    taux DECIMAL(10,2) NOT NULL,
    CONSTRAINT check_taux_positif CHECK (taux>=0 AND taux<=1)
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
    points_fidelite INT DEFAULT 0,
    utilisateur_id INT NOT NULL,

    FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id) ON DELETE CASCADE -- si l'utilisateur est supprimé, alors on le supprime de la table client dans le cas où il s'agissait d'un client
);

-- Les utilisateurs de type livreurs
CREATE TABLE livreurs (
    id  INT AUTO_INCREMENT  PRIMARY KEY,
    nom VARCHAR(50) NOT NULL,
    prenom VARCHAR(50) NOT NULL,
    note DECIMAL(10,2) NOT NULL DEFAULT 0,
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
    instructions TEXT DEFAULT "Merci de votre service.",
    client_id INT NOT NULL,

    FOREIGN KEY (client_id) REFERENCES clients(id),
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
    livreur_id INT, --- au moment de la commande on a pas de livreur associé
    adresse_id  INT NOT NULL,

    FOREIGN KEY (statut_id) REFERENCES statuts(id),
    FOREIGN KEY (client_id) REFERENCES clients(id),
    FOREIGN KEY (livreur_id) REFERENCES livreurs(id),
    FOREIGN KEY (adresse_id) REFERENCES adresses(id)
);


-- taxes s'appliquant sur une commande
CREATE TABLE commandes_taxes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    taxe_id INT NOT NULL,
    commande_id INT NOT NULL,

    FOREIGN KEY (taxe_id) REFERENCES taxes(id),
    FOREIGN KEY (commande_id) REFERENCES commandes(id),
    UNIQUE(taxe_id, commande_id)
);

-- Liste des commandes en attente (uniquement les nouvelles commandes)
CREATE TABLE commandes_en_attente (
    id INT AUTO_INCREMENT PRIMARY KEY,
    commande_id INT NOT NULL,

    FOREIGN KEY (commande_id) REFERENCES commandes(id)
);



-- ====================================================================
-- GROUPE 6 : Tables de gestions des pizzas [pizzas, pizzas_garnitures]
-- ====================================================================

-- information sur la pizza commande par le client
CREATE TABLE pizzas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(50) NOT NULL,
    taille INT NOT NULL,
    sauce_id INT NOT NULL,
    croute_id INT NOT NULL,
    commande_id INT NOT NULL,

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

