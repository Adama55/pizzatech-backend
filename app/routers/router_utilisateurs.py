from fastapi import APIRouter


router = APIRouter(
    prefix='/utilisateurs',
    tags=["utilisateurs"]
)

@router.get("/")
async def getUtilisateurs():
    return {"utilisateurs": "Bienvenue sur PizzaTech API"}