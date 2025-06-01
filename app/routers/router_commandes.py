from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.db.database import get_db
from app.schemas.schemas import CommandeRead, CommandeCreate, CommandeUpdate
from app.services.service_commandes import (
    get_all_commandes,
    get_commande_by_id,
    create_commande,
    update_commande_sr,
    remove_commande,
    NotFoundException
)

router = APIRouter(
    prefix="/commandes",
    tags=["commandes"]
)

@router.get("/", response_model=list[CommandeRead])
def read_commandes(db: Session = Depends(get_db)):
    try:
        commandes = get_all_commandes(db)
        return commandes
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/{commande_id}", response_model=CommandeRead)
def read_commande(commande_id: int, db: Session = Depends(get_db)):
    try:
        commande = get_commande_by_id(db, commande_id)
        return commande
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/", response_model=CommandeRead, status_code=status.HTTP_201_CREATED)
def add_commande(commande: CommandeCreate, db: Session = Depends(get_db)):
    try:
        nouvelle_commande = create_commande(db, commande)
        return nouvelle_commande
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{commande_id}", response_model=CommandeRead)
def update_commande(commande_id: int, commande_data: CommandeUpdate, db: Session = Depends(get_db)):
    try:
        commande = update_commande_sr(db, commande_id, commande_data)
        return commande
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.delete("/{commande_id}")
def delete_commande(commande_id: int, db: Session = Depends(get_db)):
    try:
        message = remove_commande(db, commande_id)
        return {"message": message}
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
