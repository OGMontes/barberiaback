from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

MYSQL_USER = "ogmontes"
MYSQL_PASSWORD = "1019"
MYSQL_HOST = "172.17.0.1"  # ✅ Acceso al host desde el contenedor
MYSQL_PORT = "3306"
MYSQL_DB = "barberia-template"

DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
