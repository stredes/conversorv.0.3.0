# db/models.py

from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Configuracion(Base):
    __tablename__ = 'configuraciones'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    config_json = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class HistorialArchivo(Base):
    __tablename__ = 'historial_archivos'
    id = Column(Integer, primary_key=True)
    filename = Column(String(255), nullable=False)
    processed_at = Column(DateTime, default=datetime.utcnow)
    mode_used = Column(String(50))

class RegistroImpresion(Base):
    __tablename__ = 'registros_impresion'
    id = Column(Integer, primary_key=True)
    file_id = Column(Integer, nullable=False)
    printer_name = Column(String(100))
    printed_at = Column(DateTime, default=datetime.utcnow)
