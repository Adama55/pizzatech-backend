from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app.models.models import DetailsCommande
from app.schemas.schemas import DetailCommandeCreate, DetailsCommandeUpdate


class NotFoundException(Exception):
    pass


def get_all_details_commandes(db: Session):
    details = db.query(DetailsCommande).all()
    if not details:
        raise NotFoundException("Aucun détail de commande trouvé dans la base.")
    return details


def get_details_commande_by_id(db: Session, details_id: int):
    detail = db.query(DetailsCommande).filter(DetailsCommande.id == details_id).first()
    if not detail:
        raise NotFoundException("Détail commande non trouvé.")
    return detail


def create_details_commande(db: Session, details_data: DetailCommandeCreate):
    detail = DetailsCommande(**details_data.dict())
    try:
        db.add(detail)
        db.commit()
        db.refresh(detail)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erreur lors de la création du détail commande (conflit ou doublon)."
        )
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur interne lors de la création du détail commande."
        )
    return detail


def update_details_commande_sr(db: Session, details_id: int, update_data: DetailsCommandeUpdate):
    detail = db.query(DetailsCommande).filter(DetailsCommande.id == details_id).first()
    if not detail:
        raise NotFoundException("Détail commande non trouvé.")

    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(detail, key, value)
    db.commit()
    db.refresh(detail)
    return detail


def remove_details_commande(db: Session, details_id: int):
    detail = db.query(DetailsCommande).filter(DetailsCommande.id == details_id).first()
    if not detail:
        raise NotFoundException("Détail commande non trouvé.")

    db.delete(detail)
    db.commit()
    return "Détail commande supprimé avec succès"
