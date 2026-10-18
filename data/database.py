# Crear el motor de conexión a Supabase
from sqlalchemy import create_engine
from config import DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)