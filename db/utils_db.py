from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from .models import Base, User,Configuracion as Config, FileHistory, PrintRecord
from pathlib import Path
import logging
import json

# Configuración de la base de datos
DB_PATH = Path("data.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Archivo de configuración y logs
CONFIG_FILE = Path("excel_printer_config.json")
LOG_FILE = Path("logs_app.log")

# ---------- Crear usuario ----------
def create_user(email, password):
    try:
        new_user = User(email=email, password=password)
        session.add(new_user)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        logging.error(f"Error creando usuario: {e}")
        return False

# ---------- Obtener usuario ----------
def get_user(email):
    try:
        user = session.query(User).filter_by(email=email).first()
        return user
    except Exception as e:
        logging.error(f"Error obteniendo usuario: {e}")
        return None

# ---------- Guardar historial de archivos ----------
def save_file_history(filename, mode):
    try:
        history = FileHistory(filename=filename, mode_used=mode)
        session.add(history)
        session.commit()
    except Exception as e:
        session.rollback()
        logging.error(f"Error guardando historial archivo: {e}")

# ---------- Guardar configuración ----------
def save_config(config_data):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config_data, f, indent=4)
        logging.info("Configuración guardada correctamente.")
    except Exception as e:
        logging.error(f"Error al guardar configuración: {e}")
