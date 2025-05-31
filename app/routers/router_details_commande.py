from fastapi import APIRouter


router = APIRouter(
    prefix='/details_commandes',
    tags=["details_commandes"]
)

@router.get("/")
async def getDetailsCommandes():
    return {"details_commandes": "Bienvenue sur PizzaTech API"}