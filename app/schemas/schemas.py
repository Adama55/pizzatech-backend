from pydantic import BaseModel, EmailStr
from typing import List, Optional
from enum import Enum
from typing import Optional


# === ENUMS ===

class RoleEnum(str, Enum):
    client = "client"
    admin = "admin"

class StatutEnum(str, Enum):
    preparation = "preparation"
    livraison = "livraison"
    livree = "livree"


# === UTILISATEUR ===

class UtilisateurBase(BaseModel):
    nom: str
    email: EmailStr
    role: RoleEnum

class UtilisateurCreate(UtilisateurBase):
    password: str

class UtilisateurRead(UtilisateurBase):
    id: int

class UtilisateurUpdate(BaseModel):
    nom: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[RoleEnum] = None

    class Config:
        orm_mode = True


# === PIZZA ===

class PizzaBase(BaseModel):
    nom: str
    description: Optional[str] = None
    prix: float
    image_url: Optional[str] = None

class PizzaCreate(PizzaBase):
    pass

class PizzaRead(PizzaBase):
    id: int

class PizzaUpdate(BaseModel):
    nom: Optional[str] = None
    description: Optional[str] = None
    prix: Optional[float] = None
    image_url: Optional[str] = None

    class Config:
        orm_mode = True


# === DETAILS DE COMMANDE ===

class DetailCommandeBase(BaseModel):
    commande_id : int
    pizza_id: int
    quantite: int
    prix_unitaire: float

class DetailCommandeCreate(DetailCommandeBase):
    pass

class DetailCommandeRead(DetailCommandeBase):
    id: int

class DetailsCommandeUpdate(BaseModel):
    quantite: Optional[int] = None

    class Config:
        orm_mode = True


# === COMMANDE ===

class CommandeBase(BaseModel):
    utilisateur_id: int
    statut: StatutEnum

class CommandeCreate(CommandeBase):
    details: List[DetailCommandeCreate]

class CommandeRead(CommandeBase):
    id: int
    utilisateur: Optional[UtilisateurRead]
    details: List[DetailCommandeRead] = []

class CommandeUpdate(BaseModel):
    utilisateur_id: Optional[int] = None
    statut: Optional[StatutEnum] = None

    class Config:
        orm_mode = True

class CommandeDelete(CommandeBase):
    id: int