from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# URL de connexion PostgreSQL
DATABASE_URL = "postgresql://postgres:@localhost:5432/pizzatech"

# Créer l'engine SQLAlchemy
engine = create_engine(DATABASE_URL)

# Créer une session locale
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour les modèles ORM
Base = declarative_base()
