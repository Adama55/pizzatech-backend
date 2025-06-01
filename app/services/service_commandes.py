from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.models import Commande, DetailsCommande, Pizza, Utilisateur
from app.schemas.schemas import CommandeCreate, CommandeUpdate  # on ajoutera CommandeUpdate
from sqlalchemy.exc import IntegrityError

class NotFoundException(Exception):
    pass

def get_all_commandes(db: Session):
    commandes = db.query(Commande).all()
    if not commandes:
        raise NotFoundException("Aucune commande trouvée dans la base.")
    return commandes

def get_commande_by_id(db: Session, commande_id: int):
    commande = db.query(Commande).filter(Commande.id == commande_id).first()
    if not commande:
        raise NotFoundException("Commande non trouvée.")
    return commande

def create_commande(db: Session, commande_data: CommandeCreate):
    commande = Commande(
        utilisateur_id=commande_data.utilisateur_id,
        statut=commande_data.statut,
    )
    try:
        db.add(commande)
        db.commit()
        db.refresh(commande)
        # Création des détails commande
        for detail in commande_data.details:
            detail_commande = DetailsCommande(
                commande_id=commande.id,
                pizza_id=detail.pizza_id,
                quantite=detail.quantite,
                prix_unitaire=detail.prix_unitaire,
            )
            db.add(detail_commande)
        db.commit()
        db.refresh(commande)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erreur d'intégrité lors de la création de la commande."
        )
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur serveur lors de la création de la commande."
        )
    return commande

def update_commande_sr(db: Session, commande_id: int, commande_data: CommandeUpdate):
    commande = db.query(Commande).filter(Commande.id == commande_id).first()
    if not commande:
        raise NotFoundException("Commande non trouvée.")

    for key, value in commande_data.dict(exclude_unset=True).items():
        setattr(commande, key, value)

    db.commit()
    db.refresh(commande)
    return commande

def remove_commande(db: Session, commande_id: int):
    commande = db.query(Commande).filter(Commande.id == commande_id).first()
    if not commande:
        raise NotFoundException("Commande non trouvée.")

    db.query(DetailsCommande).filter(DetailsCommande.commande_id == commande_id).delete()
    db.delete(commande)
    db.commit()
    return "Commande supprimée avec succès"
