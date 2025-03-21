from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    correo = Column(String, unique=True, nullable=False)
    clave = Column(String, nullable=False)
    modo_favorito = Column(String, default='listados')
    ultima_carpeta = Column(String, nullable=True)

    configuraciones = relationship("Configuracion", back_populates="usuario")
    historial = relationship("HistorialArchivo", back_populates="usuario")
    registros_impresion = relationship("RegistroImpresion", back_populates="usuario")


class Configuracion(Base):
    __tablename__ = 'configuraciones'
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    nombre_columna = Column(String)
    eliminar = Column(String)  # Guardar en formato JSON string
    mantener = Column(String)  # Guardar en formato JSON string

    usuario = relationship("Usuario", back_populates="configuraciones")


class HistorialArchivo(Base):
    __tablename__ = 'historial_archivos'
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    nombre_archivo = Column(String)
    fecha_procesado = Column(DateTime, default=datetime.utcnow)
    modo_utilizado = Column(String)

    usuario = relationship("Usuario", back_populates="historial")


class RegistroImpresion(Base):
    __tablename__ = 'registros_impresion'
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    archivo_impreso = Column(String)
    fecha_impresion = Column(DateTime, default=datetime.utcnow)
    impresora = Column(String)

    usuario = relationship("Usuario", back_populates="registros_impresion")
