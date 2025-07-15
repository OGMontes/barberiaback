# database.py  (o donde tienes esa configuración)
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

MYSQL_USER = "ogmontes"
MYSQL_PASSWORD = "1019"
MYSQL_HOST = "127.0.0.1"   # ← extremo local del túnel
MYSQL_PORT = "3307"        # ← puerto que mapeaste con ssh -L
MYSQL_DB = "barberia-template"

DATABASE_URL = (
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}"
    f"@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
)

engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True     # revive la conexión si el túnel se corta un momento
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
