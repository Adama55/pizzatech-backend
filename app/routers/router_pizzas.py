from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.db.database import get_db
from app.schemas.schemas import PizzaRead, PizzaCreate, PizzaBase, PizzaUpdate
from app.services.service_piazza import (
    get_all_pizzas,
    NotFoundException,
    get_pizza_by_id,
    create_pizza,
    update_pizza_sr,
    remove_pizza
)

router = APIRouter(
    prefix="/api/pizzas",
    tags=["pizzas"]
)

@router.get("/", response_model=list[PizzaRead])
def read_pizzas(db: Session = Depends(get_db)):
    try:
        pizzas = get_all_pizzas(db)
        return pizzas
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/{pizza_id}", response_model=PizzaRead)
def read_pizza(pizza_id: int, db: Session = Depends(get_db)):
    try:
        pizza = get_pizza_by_id(db, pizza_id)
        return pizza
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/", response_model=PizzaRead, status_code=status.HTTP_201_CREATED)
def add_pizza(pizza: PizzaCreate, db: Session = Depends(get_db)):
    try:
        nouvelle_pizza = create_pizza(db, pizza)
        return nouvelle_pizza
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{pizza_id}", response_model=PizzaRead)
def update_pizza(pizza_id: int, pizza_data: PizzaUpdate, db: Session = Depends(get_db)):
    try:
        pizza = update_pizza_sr(db, pizza_id, pizza_data)
        return pizza
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.delete("/{pizza_id}")
def delete_pizza(pizza_id: int, db: Session = Depends(get_db)):
    try:
        message = remove_pizza(db, pizza_id)
        return {"detail": message}
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
