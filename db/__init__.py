# db/__init__.py

"""
Este archivo convierte el directorio 'db' en un paquete Python y
facilita la importación de todos los componentes esenciales de la base de datos
desde un solo lugar.
"""
from .database import init_db
from .models import User, Configuracion as Config, HistorialArchivo, RegistroImpresion
from .utils_db import create_user, get_user, save_file_history


__all__ = [
    "init_db",
    "User",
    "Config",
    "FileHistory",
    "PrintRecord",
    "create_user",
    "get_user",
    "save_file_history"
]
