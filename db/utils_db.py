from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from pathlib import Path
import json
import logging

from .models import Base, User, Configuracion, HistorialArchivo, RegistroImpresion

# Archivo configuración y logs
CONFIG_FILE = Path("excel_printer_config.json")
LOG_FILE = Path("logs_app.log")

# ----------------- Conexión -----------------
DB_PATH = "sqlite:///excel_printer.db"
engine = create_engine(DB_PATH)
Session = sessionmaker(bind=engine)

# ----------------- Configuración -----------------
def load_config():
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Error al cargar configuración: {e}")
            return {}
    return {}

def save_config(config_data):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config_data, f, indent=4)
        logging.info("Configuración guardada correctamente.")
    except Exception as e:
        logging.error(f"Error al guardar configuración: {e}")

# ----------------- Usuarios -----------------
def create_user(username, password):
    session = Session()
    try:
        user = User(username=username, password=password)
        session.add(user)
        session.commit()
        logging.info(f"Usuario '{username}' creado.")
    except Exception as e:
        session.rollback()
        logging.error(f"Error al crear usuario: {e}")
    finally:
        session.close()

def get_user(username):
    session = Session()
    try:
        user = session.query(User).filter_by(username=username).first()
        return user
    except Exception as e:
        logging.error(f"Error al obtener usuario: {e}")
        return None
    finally:
        session.close()

# ----------------- Historial Archivos -----------------
def save_file_history(filename, mode):
    session = Session()
    try:
        record = HistorialArchivo(filename=filename, mode=mode)
        session.add(record)
        session.commit()
        logging.info(f"Historial guardado para archivo '{filename}'")
    except Exception as e:
        session.rollback()
        logging.error(f"Error al guardar historial: {e}")
    finally:
        session.close()

# ----------------- Logging -----------------
def setup_logging():
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
