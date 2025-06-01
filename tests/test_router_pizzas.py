from fastapi import status
from unittest.mock import Mock
import pytest
from fastapi.exceptions import HTTPException

def test_read_pizzas(client, mock_db):
    """Test GET /pizzas/ - Liste toutes les pizzas"""
    # Arrange
    mock_pizza1 = Mock()
    mock_pizza1.id = 1
    mock_pizza1.nom = "Pizza Margherita"
    mock_pizza1.prix = 10.99
    mock_pizza1.description = "Tomate, mozzarella, basilic"
    mock_pizza1.image_url = "img url"

    mock_pizza2 = Mock()
    mock_pizza2.id = 2
    mock_pizza2.nom = "Pizza Pepperoni"
    mock_pizza2.prix = 12.99
    mock_pizza2.description = "Tomate, mozzarella, pepperoni"
    mock_pizza2.image_url = "img url"

    mock_db.query.return_value.all.return_value = [mock_pizza1, mock_pizza2]

    # Act
    response = client.get("/pizzas/")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    resultats = response.json()
    assert len(resultats) == 2
    assert resultats[0]["nom"] == "Pizza Margherita"
    assert resultats[1]["prix"] == 12.99

def test_read_pizza(client, mock_db):
    """Test GET /pizzas/{id} - Récupère une pizza spécifique"""
    # Arrange
    mock_pizza = Mock()
    mock_pizza.id = 1
    mock_pizza.nom = "Pizza Margherita"
    mock_pizza.prix = 10.99
    mock_pizza.description = "Tomate, mozzarella, basilic"
    mock_pizza.image_url = "img url"

    mock_db.query.return_value.filter.return_value.first.return_value = mock_pizza

    # Act
    response = client.get("/pizzas/1")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    resultat = response.json()
    assert resultat["id"] == 1
    assert resultat["nom"] == "Pizza Margherita"

def test_read_pizza_non_trouve(client, mock_db):
    """Test GET /pizzas/{id} - Pizza non trouvée"""
    # Arrange
    mock_db.query.return_value.filter.return_value.first.return_value = None

    # Act
    response = client.get("/pizzas/999")

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Pizza non trouvée" in response.json()["detail"]

def test_create_pizza(client, mock_db):
    """Test POST /pizzas/ - Crée une nouvelle pizza"""
    data_pizza = {
        "nom": "Nouvelle Pizza",
        "prix": 14.99,
        "description": "Une délicieuse nouvelle pizza",
        "image_url" : "img url"
    }

    class MockPizza:
        def __init__(self):
            self.id = 1
            self.nom = data_pizza["nom"]
            self.prix = data_pizza["prix"]
            self.description = data_pizza["description"]
            self.image_url = data_pizza["image_url"]

    mock_pizza = MockPizza()

    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.side_effect = lambda x: setattr(x, 'id', 1)

    # Act
    response = client.post("/pizzas/", json=data_pizza)

    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    resultat = response.json()
    assert isinstance(resultat["id"], int)
    assert resultat["nom"] == "Nouvelle Pizza"
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()

def test_update_pizza(client, mock_db):
    """Test PUT /pizzas/{id} - Met à jour une pizza existante"""
    id_pizza = 1
    data_update = {
        "nom": "Pizza Mise à Jour",
        "prix": 15.99,
        "description": "Une pizza mise à jour",
        "image_url" : "img url"
    }

    class MockPizza:
        def __init__(self):
            self.id = id_pizza
            self.nom = "Pizza Originale"
            self.prix = 13.99
            self.description = "Une pizza originale"
            self.image_url = data_update["image_url"]

    mock_pizza = MockPizza()
    mock_db.query.return_value.filter.return_value.first.return_value = mock_pizza

    # Act
    response = client.put(f"/pizzas/{id_pizza}", json=data_update)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert mock_pizza.nom == data_update["nom"]
    assert mock_pizza.prix == data_update["prix"]
    assert mock_pizza.description == data_update["description"]
    mock_db.commit.assert_called_once()

def test_update_pizza_non_trouve(client, mock_db):
    """Test PUT /pizzas/{id} - Pizza non trouvée"""
    data_update = {"nom": "Nouvelle Pizza"}
    mock_db.query.return_value.filter.return_value.first.return_value = None

    # Act
    response = client.put("/pizzas/999", json=data_update)

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_pizza(client, mock_db):
    """Test DELETE /pizzas/{id} - Supprime une pizza"""
    mock_pizza = Mock()
    mock_pizza.id = 1
    mock_db.query.return_value.filter.return_value.first.return_value = mock_pizza

    # Act
    response = client.delete("/pizzas/1")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    mock_db.delete.assert_called_once_with(mock_pizza)
    mock_db.commit.assert_called_once()

def test_delete_pizza_non_trouve(client, mock_db):
    """Test DELETE /pizzas/{id} - Pizza non trouvée"""
    mock_db.query.return_value.filter.return_value.first.return_value = None

    # Act
    response = client.delete("/pizzas/999")

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
