from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Use the service name 'postgres_db' as the host
SQLALCHEMY_DATABASE_URL = "postgresql://aetheruser:aetherpass@postgres_db/aetherchain"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)