CREATE DATABASE pizzaTech;

CREATE TYPE role_enum AS ENUM ('client', 'admin');
CREATE TYPE statut_enum AS ENUM ('preparation', 'livraison', 'livree');

CREATE TABLE utilisateurs
(
    id           SERIAL PRIMARY KEY,
    nom          VARCHAR(255) NOT NULL,
    email        VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role         role_enum    NOT NULL
);

CREATE TABLE pizzas
(
    id          SERIAL PRIMARY KEY,
    nom         VARCHAR(255)   NOT NULL,
    description TEXT,
    prix        DECIMAL(10, 2) NOT NULL,
    image_url   VARCHAR(255)
);

CREATE TABLE commandes
(
    id             SERIAL PRIMARY KEY,
    utilisateur_id INT         NOT NULL,
    statut         statut_enum NOT NULL,
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs (id)
);

CREATE TABLE details_commande
(
    id            SERIAL PRIMARY KEY,
    commande_id   INT            NOT NULL,
    pizza_id      INT            NOT NULL,
    quantite      INT            NOT NULL,
    prix_unitaire DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (commande_id) REFERENCES commandes (id),
    FOREIGN KEY (pizza_id) REFERENCES pizzas (id)
);