from fastapi import status
from unittest.mock import Mock
import pytest
from fastapi.exceptions import HTTPException

def test_read_commande(client, mock_db):
    """Test GET /commandes/{id} - Récupère une commande spécifique avec détails imbriqués"""
    # Arrange
    mock_utilisateur = Mock()
    mock_utilisateur.id = 4
    mock_utilisateur.nom = "Fofana"
    mock_utilisateur.email = "adama2@example.com"
    mock_utilisateur.role = "client"

    mock_detail = Mock()
    mock_detail.id = 1
    mock_detail.pizza_id = 1
    mock_detail.quantite = 10
    mock_detail.prix_unitaire = 8.5

    mock_commande = Mock()
    mock_commande.id = 1
    mock_commande.utilisateur_id = 4
    mock_commande.statut = "livraison"
    mock_commande.utilisateur = mock_utilisateur
    mock_commande.details = [mock_detail]

    mock_db.query.return_value.filter.return_value.first.return_value = mock_commande

    # Act
    response = client.get("/commandes/1")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    resultat = response.json()
    assert resultat["id"] == 1
    assert resultat["statut"] == "livraison"
    assert resultat["utilisateur"]["nom"] == "Fofana"
    assert len(resultat["details"]) == 1
    assert resultat["details"][0]["quantite"] == 10

def test_create_commande(client, mock_db):
    """Test POST /commandes/ - Crée une nouvelle commande avec utilisateur et pizza existants"""

    # Arrange: Crée un utilisateur et une pizza

    # Mock pour l'utilisateur
    mock_utilisateur = Mock()
    mock_utilisateur.id = 4
    mock_utilisateur.nom = "Fofana"
    mock_utilisateur.email = "adama2@example.com"
    mock_utilisateur.role = "client"

    # Mock pour la pizza
    mock_pizza = Mock()
    mock_pizza.id = 1
    mock_pizza.nom = "Margherita"
    mock_pizza.prix = 8.5
    mock_pizza.description = "Tomate, mozzarella, basilic"
    mock_pizza.image_url = "img url"

    # Mock pour le détail de la commande
    mock_detail = Mock()
    mock_detail.id = 1
    mock_detail.pizza_id = mock_pizza.id
    mock_detail.quantite = 10
    mock_detail.prix_unitaire = mock_pizza.prix

    # Mock pour la commande
    mock_commande = Mock()
    mock_commande.id = 1
    mock_commande.utilisateur_id = mock_utilisateur.id
    mock_commande.statut = "preparation"
    mock_commande.utilisateur = mock_utilisateur
    mock_commande.details = [mock_detail]

    # Configure les mocks pour simuler la récupération de l'utilisateur et de la pizza
    mock_db.query.return_value.filter.return_value.first.side_effect = [
        mock_utilisateur,  # Pour la récupération de l'utilisateur
        mock_pizza,  # Pour la récupération de la pizza
        mock_commande  # Pour la récupération de la commande
    ]

    # Configure le mock pour retourner la commande avec les détails
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.side_effect = lambda x: setattr(x, 'id', 1)

    # Données de la commande
    data_commande = {
        "utilisateur_id": mock_utilisateur.id,
        "statut": "preparation",
        "details": [
            {
                "pizza_id": mock_pizza.id,
                "quantite": 10,
                "prix_unitaire": mock_pizza.prix
            }
        ]
    }

    # Act: Crée la commande
    response = client.post("/commandes/", json=data_commande)

    # Assert: Vérifie que la commande a été créée correctement
    assert response.status_code == status.HTTP_201_CREATED
    resultat = response.json()
    assert isinstance(resultat["id"], int)
    assert resultat["statut"] == "preparation"
    assert len(resultat) == 5
from fastapi import status
from unittest.mock import Mock
import pytest
from fastapi.exceptions import HTTPException

def test_update_commande(client, mock_db):
    """Test PUT /commandes/{id} - Met à jour une commande existante"""
    # Arrange
    mock_utilisateur = Mock()
    mock_utilisateur.id = 4
    mock_utilisateur.nom = "Fofana"
    mock_utilisateur.email = "adama2@example.com"
    mock_utilisateur.role = "client"

    mock_detail = Mock()
    mock_detail.id = 1
    mock_detail.pizza_id = 1
    mock_detail.quantite = 10
    mock_detail.prix_unitaire = 8.5

    mock_commande = Mock()
    mock_commande.id = 1
    mock_commande.utilisateur_id = 4
    mock_commande.statut = "livraison"
    mock_commande.utilisateur = mock_utilisateur
    mock_commande.details = [mock_detail]

    mock_db.query.return_value.filter.return_value.first.return_value = mock_commande

    # Données pour la mise à jour
    data_update = {
        "statut": "livraison",
        "details": [
            {
                "pizza_id": 1,
                "quantite": 5,
                "prix_unitaire": 8.5
            }
        ]
    }

    # Act
    response = client.put("/commandes/1", json=data_update)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    resultat = response.json()
    assert resultat["statut"] == "livraison"
    assert len(resultat["details"]) == 1

def test_delete_commande(client, mock_db):
    """Test DELETE /commandes/{id} - Supprime une commande"""
    # Arrange
    mock_commande = Mock()
    mock_commande.id = 1

    mock_db.query.return_value.filter.return_value.first.return_value = mock_commande

    # Act
    response = client.delete("/commandes/1")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Commande supprimée avec succès"}


def test_delete_commande_non_trouve(client, mock_db):
    """Test DELETE /commandes/{id} - Commande non trouvée"""
    # Arrange
    mock_db.query.return_value.filter.return_value.first.return_value = None

    # Act
    response = client.delete("/commandes/999")

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
