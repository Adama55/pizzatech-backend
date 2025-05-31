from fastapi import APIRouter


router = APIRouter(
    prefix='/commandes',
    tags=["commandes"]
)

@router.get("/")
async def getCommandes():
    return {"commandes": "Bienvenue sur PizzaTech API"}