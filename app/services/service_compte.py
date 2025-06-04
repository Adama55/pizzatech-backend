from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.models import Utilisateur
from app.schemas.schemas import UtilisateurSignup, UtilisateurLogin
from sqlalchemy.exc import IntegrityError
from app.utils.security_utils import hash_password, verify_password

class NotFoundException(Exception):
    pass

def signup_utilisateur(db: Session, utilisateur_data: UtilisateurSignup):
    hashed_password = hash_password(utilisateur_data.password)
    utilisateur = Utilisateur(
        nom=utilisateur_data.nom,
        email=utilisateur_data.email,
        password=hashed_password,
        role=utilisateur_data.role # par defaut "client"
    )
    try:
        db.add(utilisateur)
        db.commit()
        db.refresh(utilisateur)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erreur d'intégrité lors de la création de l'utilisateur."
        )
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur serveur lors de la création de l'utilisateur."
        )
    return utilisateur

def authenticate_utilisateur(db: Session, utilisateur_data: UtilisateurLogin):
    utilisateur = db.query(Utilisateur).filter(Utilisateur.email == utilisateur_data.email).first()
    if not utilisateur or not verify_password(utilisateur_data.password, utilisateur.password):
        raise NotFoundException("Email ou mot de passe incorrect.")
    return utilisateur
