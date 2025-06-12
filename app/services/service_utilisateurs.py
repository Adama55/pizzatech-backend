from sqlalchemy.orm import Session
from app.models.models import Utilisateur
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app.utils.security_utils import hash_password

from app.schemas.schemas import UtilisateurUpdate


class NotFoundException(Exception):
    pass

def get_all_utilisateurs(db: Session):
    utilisateurs = db.query(Utilisateur).all()
    if not utilisateurs:
        raise NotFoundException("Aucun utilisateur trouvé dans la base.")
    return utilisateurs


def get_utilisateur_by_id(db: Session, user_id: int):
    utilisateur = db.query(Utilisateur).filter(Utilisateur.id == user_id).first()
    if not utilisateur:
        raise NotFoundException(f"Utilisateur non trouvé.")
    return utilisateur

def create_utilisateur(db: Session, utilisateur_data: dict):

    if 'password' in utilisateur_data:
        utilisateur_data['password'] = hash_password(utilisateur_data['password'])

    utilisateur = Utilisateur(**utilisateur_data)
    try:
        db.add(utilisateur)
        db.commit()
        db.refresh(utilisateur)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Un utilisateur avec cet email existe déjà."
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la création de l'utilisateur."
        )
    return utilisateur


def update_utilisateur_ser(db: Session, utilisateur_id: int, utilisateur_data: UtilisateurUpdate):
    utilisateur = db.query(Utilisateur).filter(Utilisateur.id == utilisateur_id).first()
    if not utilisateur:
        raise NotFoundException(f"Utilisateur avec non trouvé.")

    for key, value in utilisateur_data.dict(exclude_unset=True).items():
        setattr(utilisateur, key, value)

    db.commit()
    db.refresh(utilisateur)
    return utilisateur

def remove_utilisateur(db: Session, utilisateur_id: int):
    utilisateur = db.query(Utilisateur).filter(Utilisateur.id == utilisateur_id).first()
    if not utilisateur:
        raise NotFoundException(f"Utilisateur non trouvé.")

    db.delete(utilisateur)
    db.commit()
    return ("utilisateur supprimé avec succès")