DROP DATABASE IF EXISTS pizzaria_db;

CREATE DATABASE pizzaria_db;

USE pizzaria_db;

CREATE TABLE clients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(50) NOT NULL,
    prenom VARCHAR(50),
    courriel VARCHAR(250) NOT NULL UNIQUE,
    telephone CHAR(20),
    ville VARCHAR(100) NOT NULL,
    pays VARCHAR(100) NOT NULL,
    adresse VARCHAR(255) NOT NULL,

    CONSTRAINT format_courriel CHECK (REGEXP_LIKE(courriel, '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'))
);
