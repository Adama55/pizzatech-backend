from sqlalchemy.orm import Session
from app.models.models import Pizza
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app.schemas.schemas import PizzaCreate, PizzaBase, PizzaUpdate


class NotFoundException(Exception):
    pass


def get_all_pizzas(db: Session):
    pizzas = db.query(Pizza).all()
    if not pizzas:
        raise NotFoundException("Aucune pizza trouvée dans la base.")
    return pizzas


def get_pizza_by_id(db: Session, pizza_id: int):
    pizza = db.query(Pizza).filter(Pizza.id == pizza_id).first()
    if not pizza:
        raise NotFoundException("Pizza non trouvée.")
    return pizza


def create_pizza(db: Session, pizza_data: PizzaCreate):
    pizza = Pizza(**pizza_data.dict())
    try:
        db.add(pizza)
        db.commit()
        db.refresh(pizza)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erreur lors de la création de la pizza (peut-être doublon)."
        )
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur interne lors de la création de la pizza."
        )
    return pizza


def update_pizza_sr(db: Session, pizza_id: int, pizza_data: PizzaUpdate):
    pizza = db.query(Pizza).filter(Pizza.id == pizza_id).first()
    if not pizza:
        raise NotFoundException("Pizza non trouvée.")

    for key, value in pizza_data.dict(exclude_unset=True).items():
        setattr(pizza, key, value)
    db.commit()
    db.refresh(pizza)
    return pizza


def remove_pizza(db: Session, pizza_id: int):
    pizza = db.query(Pizza).filter(Pizza.id == pizza_id).first()
    if not pizza:
        raise NotFoundException("Pizza non trouvée.")

    db.delete(pizza)
    db.commit()
    return "Pizza supprimée avec succès"
