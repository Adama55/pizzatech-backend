from sqlalchemy import Column, Integer, String, Text, DECIMAL, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

class RoleEnum(enum.Enum):
    client = "client"
    admin = "admin"


class StatutEnum(enum.Enum) :
    preparation = "preparation"
    livraison = "livraison"
    livree = "livree"


class Utilisateur(Base):
    __tablename__ = "utilisateurs"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)

    commandes = relationship("Commande", back_populates="utilisateur")


class Pizza(Base):
    __tablename__ = "pizzas"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(255), nullable=False)
    description = Column(Text)
    prix = Column(DECIMAL(10,2), nullable=False)
    image_url = Column(String(255))

    details_commandes = relationship("DetailsCommande", back_populates="pizza")


class Commande(Base):
    __tablename__ = "commandes"

    id = Column(Integer, primary_key=True, index=True)
    utilisateur_id = Column(Integer, ForeignKey("utilisateurs.id"), nullable=False)
    statut = Column(Enum(StatutEnum), nullable=False)

    utilisateur = relationship("Utilisateur", back_populates="commandes")
    details = relationship("DetailsCommande", back_populates="commande")


class DetailsCommande(Base):
    __tablename__ = "details_commande"

    id = Column(Integer, primary_key=True, index=True)
    commande_id = Column(Integer, ForeignKey("commandes.id"), nullable=False)
    pizza_id = Column(Integer, ForeignKey("pizzas.id"), nullable=False)
    quantite = Column(Integer, nullable=False)
    prix_unitaire = Column(DECIMAL(10, 2), nullable=False)

    commande = relationship("Commande", back_populates="details")
    pizza = relationship("Pizza", back_populates="details_commandes")


