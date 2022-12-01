from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from shopping_cart.settings import SQLALCHEMY_DATABASE_URI

engine = create_engine(SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
