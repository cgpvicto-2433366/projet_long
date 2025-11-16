-- ============================================
-- Projet : Gestion de Pizzeria
-- Auteur : Ben Schalom KAMGA
-- Date : 2025-11-09
-- Description : Script d'insertion des données de base et utilisateurs de test
-- ============================================



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

INSERT INTO adresses (ville, rue, code_postal, instructions, client_id) VALUES
('Victoriaville', '123 Rue Principale', 'G6P 1A1', 'Sonner 2 fois', 
 (SELECT id FROM clients WHERE nom = 'Tremblay' AND prenom = 'Jean')),
 
('Victoriaville', '456 Avenue des Érables', 'G6P 2B2', 'Appartement 5, 2e étage', 
 (SELECT id FROM clients WHERE nom = 'Dubois' AND prenom = 'Marie')),
 
('Trois-Rivières', '789 Boulevard des Forges', 'G8Z 3C3', 'Maison bleue', 
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
