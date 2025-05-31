from fastapi import APIRouter


router = APIRouter(
    prefix='/pizzas',
    tags=["pizzas"]
)

@router.get("/")
async def getPizzas():
    return {"pizzas": "Bienvenue sur PizzaTech API"}