from fastapi import status
from unittest.mock import Mock
import pytest
from fastapi.exceptions import HTTPException

# Tests pour les routes utilisateurs

def test_read_utilisateurs(client, mock_db):
    """Test GET /api/utilisateurs/ - Liste tous les utilisateurs"""
    # Arrange
    mock_utilisateur1 = Mock()
    mock_utilisateur1.id = 1
    mock_utilisateur1.nom = "Utilisateur 1"
    mock_utilisateur1.email = "utilisateur1@example.com"
    mock_utilisateur1.role = "client"
    mock_utilisateur1.password = "motdepasse_hashé_1"

    mock_utilisateur2 = Mock()
    mock_utilisateur2.id = 2
    mock_utilisateur2.nom = "Utilisateur 2"
    mock_utilisateur2.email = "utilisateur2@example.com"
    mock_utilisateur2.role = "client"
    mock_utilisateur2.password = "motdepasse_hashé_2"

    mock_db.query.return_value.all.return_value = [mock_utilisateur1, mock_utilisateur2]

    # Act
    response = client.get("/api/utilisateurs/")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    resultats = response.json()
    assert len(resultats) == 2
    assert resultats[0]["nom"] == "Utilisateur 1"
    assert resultats[1]["email"] == "utilisateur2@example.com"

def test_read_utilisateur(client, mock_db):
    """Test GET /api/utilisateurs/{id} - Récupère un utilisateur spécifique"""
    # Arrange
    mock_utilisateur = Mock()
    mock_utilisateur.id = 1
    mock_utilisateur.nom = "Test Utilisateur"
    mock_utilisateur.email = "test@example.com"
    mock_utilisateur.role = "admin"

    mock_db.query.return_value.filter.return_value.first.return_value = mock_utilisateur

    # Act
    response = client.get("/api/utilisateurs/1")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    resultat = response.json()
    assert resultat["id"] == 1
    assert resultat["nom"] == "Test Utilisateur"

def test_read_utilisateur_non_trouve(client, mock_db):
    """Test GET /api/utilisateurs/{id} - Utilisateur non trouvé"""
    # Arrange
    mock_db.query.return_value.filter.return_value.first.return_value = None

    # Act
    response = client.get("/api/utilisateurs/999")

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Utilisateur non trouvé" in response.json()["detail"]

def test_create_utilisateur(client, mock_db):
    """Test POST /api/utilisateurs/ - Crée un nouvel utilisateur"""
    data_utilisateur = {
        "nom": "Nouvel Utilisateur",
        "email": "nouveau@example.com",
        "password": "motdepasse123",
        "role": "client"
    }

    class MockUtilisateur:
        def __init__(self):
            self.id = 1
            self.nom = data_utilisateur["nom"]
            self.email = data_utilisateur["email"]
            self.role = data_utilisateur["role"]
            self.password = "motdepasse_hashé"

    mock_utilisateur = MockUtilisateur()

    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.side_effect = lambda x: setattr(x, 'id', 1)

    # Act
    response = client.post("/api/utilisateurs/", json=data_utilisateur)

    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    resultat = response.json()
    assert isinstance(resultat["id"], int)
    assert resultat["email"] == "nouveau@example.com"
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()

def test_update_utilisateur(client, mock_db):
    """Test PUT /api/utilisateurs/{id} - Met à jour un utilisateur existant"""
    id_utilisateur = 1
    data_update = {
        "nom": "Nom Mis à Jour",
        "email": "updated@example.com",
        "role": "admin"
    }
    class MockUtilisateur:
        def __init__(self):
            self.id = id_utilisateur
            self.nom = "Nom Original"
            self.email = "original@example.com"
            self.role = "client"

    mock_utilisateur = MockUtilisateur()
    mock_db.query.return_value.filter.return_value.first.return_value = mock_utilisateur

    # Act
    response = client.put(f"/api/utilisateurs/{id_utilisateur}", json=data_update)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert mock_utilisateur.nom == data_update["nom"]
    assert mock_utilisateur.email == data_update["email"]
    assert mock_utilisateur.role == data_update["role"]
    mock_db.commit.assert_called_once()

def test_update_utilisateur_non_trouve(client, mock_db):
    """Test PUT /api/utilisateurs/{id} - Utilisateur non trouvé"""
    data_update = {"nom": "Nouveau Nom"}
    mock_db.query.return_value.filter.return_value.first.return_value = None

    # Act
    response = client.put("/api/utilisateurs/999", json=data_update)

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_utilisateur(client, mock_db):
    """Test DELETE /api/utilisateurs/{id} - Supprime un utilisateur"""
    mock_utilisateur = Mock()
    mock_utilisateur.id = 1
    mock_db.query.return_value.filter.return_value.first.return_value = mock_utilisateur

    # Act
    response = client.delete("/api/utilisateurs/1")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    mock_db.delete.assert_called_once_with(mock_utilisateur)
    mock_db.commit.assert_called_once()

def test_delete_utilisateur_non_trouve(client, mock_db):
    """Test DELETE /api/utilisateurs/{id} - Utilisateur non trouvé"""
    mock_db.query.return_value.filter.return_value.first.return_value = None

    # Act
    response = client.delete("/api/utilisateurs/999")

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_utilisateur_validation(client):
    """Test POST /api/utilisateurs/ - Validation des données d'entrée"""
    # Arrange
    data_invalide = {
        "nom": "Nouvel Utilisateur",
        "email": "email_invalide",  # Email invalide
        "password": "123",  # Mot de passe trop court
        "role": "client"
    }

    # Act
    response = client.post("/api/utilisateurs/", json=data_invalide)

    # Assert
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
