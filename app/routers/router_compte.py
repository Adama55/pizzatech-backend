from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.db.database import get_db
from app.schemas.schemas import UtilisateurSignup, UtilisateurLogin, UtilisateurInDB
from app.services.service_compte import (
    signup_utilisateur,
    authenticate_utilisateur,
    NotFoundException
)

router = APIRouter(
    prefix="/api",
    tags=["Signup - Login"]
)

@router.post("/signup", response_model=UtilisateurInDB, status_code=status.HTTP_201_CREATED)
def signup(utilisateur: UtilisateurSignup, db: Session = Depends(get_db)):
    try:
        new_utilisateur = signup_utilisateur(db, utilisateur)
        return new_utilisateur
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def login(utilisateur: UtilisateurLogin, db: Session = Depends(get_db)):
    try:
        authenticated_utilisateur = authenticate_utilisateur(db, utilisateur)
        return {"message": "Connexion réussie"}
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
