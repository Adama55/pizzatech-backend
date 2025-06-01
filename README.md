
# PizzaTech Backend

PizzaTech Backend est une API RESTful développée avec FastAPI pour gérer les commandes de pizza. Elle permet de créer, lire, mettre à jour et supprimer des commandes, des pizzas et des détails de commande.

## Fonctionnalités

- Gestion des utilisateurs
- Gestion des pizzas
- Gestion des commandes
- Gestion des détails de commande

## Prérequis

Avant de commencer, assure-toi d'avoir installé les éléments suivants :

- Python 3.8 ou supérieur
- FastAPI
- Uvicorn
- SQLAlchemy
- Une base de données (par exemple, PostgreSQL, MySQL, SQLite)

## Installation

1. Clone le dépôt :

   ```bash
   git clone https://github.com/Adama55/pizzatech-backend.git
   cd pizzatech-backend
2. Crée un environnement virtuel et active-le :

    ```bash
       python -m venv venv
       source venv/bin/activate  # Sur Linux/MacOS
       .\venv\Scripts\activate  # Sur Windows
3. Installe les dépendances :
    ```bash
   pip install -r requirements.txt

4. Configure les variables d'environnement :
   Crée un fichier .env dans le répertoire racine du projet et ajoute les variables d'environnement nécessaires, par exemple :
    ```bash
   DATABASE_URL : url de votre db

## Utilisation

1. Lance le serveur de développement :

   ```bash
   uvicorn app.main\:app --reload

2. Ouvre ton navigateur et accède à la documentation de l'API à l'adresse suivante :

    ```bash
       http://localhost:8000/docs

## Tests

Pour exécuter les tests, utilise la commande suivante :

   ```bash
   pytest

