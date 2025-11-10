-- ============================================
-- Projet : Gestion de Pizzeria
-- Auteur : Ben Schalom KAMGA
-- Date : 2025-11-09
-- Description : Script des triggers
-- ============================================

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

