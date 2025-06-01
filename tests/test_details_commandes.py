from fastapi import status
from unittest.mock import Mock
import pytest
from fastapi.exceptions import HTTPException


def test_read_details_commande_non_trouve(client, mock_db):
    """Test GET /api/details-commandes/{id} - Détail de commande non trouvé"""
    # Arrange
    mock_db.query.return_value.filter.return_value.first.return_value = None

    # Act
    response = client.get("/api/details-commandes/999")

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_details_commande_non_trouve(client, mock_db):
    """Test PUT /api/details-commandes/{id} - Détail de commande non trouvé"""
    # Arrange
    mock_db.query.return_value.filter.return_value.first.return_value = None

    data_update = {"quantite": 5}

    # Act
    response = client.put("/api/details-commandes/999", json=data_update)

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_details_commande_non_trouve(client, mock_db):
    """Test DELETE /api/details-commandes/{id} - Détail de commande non trouvé"""
    # Arrange
    mock_db.query.return_value.filter.return_value.first.return_value = None

    # Act
    response = client.delete("/api/details-commandes/999")

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
