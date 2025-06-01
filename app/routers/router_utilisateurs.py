from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.db.database import get_db
from app.schemas.schemas import UtilisateurRead, UtilisateurCreate, UtilisateurUpdate
from app.services.service_utilisateurs import get_all_utilisateurs, NotFoundException, get_utilisateur_by_id, \
    create_utilisateur, update_utilisateur_ser, remove_utilisateur

router = APIRouter(
    prefix='/utilisateurs',
    tags=["utilisateurs"]
)

@router.get("/", response_model=list[UtilisateurRead])
def read_utilisateurs(db: Session = Depends(get_db)):
    try:
        utilisateurs = get_all_utilisateurs(db)
        return utilisateurs
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/{utilisateur_id}", response_model=UtilisateurRead)
def read_utilisateur(utilisateur_id: int, db: Session = Depends(get_db)):
    try:
        utilisateur = get_utilisateur_by_id(db, utilisateur_id)
        return utilisateur
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/", response_model=UtilisateurRead, status_code=status.HTTP_201_CREATED)
def add_utilisateur(utilisateur: UtilisateurCreate, db: Session = Depends(get_db)):
    try:
        nouvel_utilisateur = create_utilisateur(db, utilisateur.dict())
        return nouvel_utilisateur
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{utilisateur_id}", response_model=UtilisateurRead)
def update_utilisateur(utilisateur_id: int, utilisateur_data: UtilisateurUpdate, db: Session = Depends(get_db)):
    try:
        utilisateur = update_utilisateur_ser(db, utilisateur_id, utilisateur_data)
        return utilisateur
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.delete("/{utilisateur_id}")
def delete_utilisateur(utilisateur_id: int, db: Session = Depends(get_db)):
    try:
        remove_utilisateur(db, utilisateur_id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return " Utilisateurs supprimé avec succès"
