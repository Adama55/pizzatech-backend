from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.db.database import get_db
from app.schemas.schemas import DetailCommandeCreate, DetailsCommandeUpdate, DetailCommandeRead
from app.services.service_details_commandes import (
    get_all_details_commandes,
    get_details_commande_by_id,
    create_details_commande,
    update_details_commande_sr,
    remove_details_commande,
    NotFoundException
)

router = APIRouter(
    prefix="/details-commandes",
    tags=["details-commandes"]
)

@router.get("/", response_model=list[DetailCommandeRead])
def read_details_commandes(db: Session = Depends(get_db)):
    try:
        return get_all_details_commandes(db)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/{details_id}", response_model=DetailCommandeRead)
def read_details_commande(details_id: int, db: Session = Depends(get_db)):
    try:
        return get_details_commande_by_id(db, details_id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/", response_model=DetailCommandeRead, status_code=status.HTTP_201_CREATED)
def add_details_commande(details_data: DetailCommandeCreate, db: Session = Depends(get_db)):
    try:
        return create_details_commande(db, details_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{details_id}", response_model=DetailCommandeRead)
def update_details_commande(details_id: int, update_data: DetailsCommandeUpdate, db: Session = Depends(get_db)):
    try:
        return update_details_commande_sr(db, details_id, update_data)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{details_id}")
def delete_details_commande(details_id: int, db: Session = Depends(get_db)):
    try:
        message = remove_details_commande(db, details_id)
        return {"detail": message}
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
