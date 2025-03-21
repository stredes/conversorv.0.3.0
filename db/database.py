from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Definición base para los modelos
Base = declarative_base()

# URL de la base de datos SQLite (puedes cambiarla a MySQL/PostgreSQL si deseas)
DATABASE_URL = "sqlite:///excel_printer.db"

# Crear motor de conexión
engine = create_engine(DATABASE_URL, echo=False)

# Crear sesión
SessionLocal = sessionmaker(bind=engine)

# Función para inicializar la BD
def init_db():
    from models import User, Configuracion, HistorialArchivo, RegistroImpresion
    Base.metadata.create_all(bind=engine)
