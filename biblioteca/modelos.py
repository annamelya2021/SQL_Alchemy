# modelos.py
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship
import uuid
import os
from datetime import datetime, timedelta

Base = declarative_base()



class UsuarioDB(Base):
    __tablename__ = 'usuarios'
    id_usuario = Column(String, primary_key=True, default=lambda: uuid.uuid4().hex[:6].upper())
    nombre = Column(String)
    apellido = Column(String)
    
    prestamos = relationship("PrestamoDB", back_populates="usuario")

class MaterialDB(Base):
    __tablename__ = 'materiales'
    codigo_inventario = Column(String, primary_key=True)
    titulo = Column(String)
    tipo = Column(String)  # 'libro', 'revista', 'dvd'
    autor = Column(String, nullable=True)
    isbn = Column(String, nullable=True)
    numero_paginas = Column(Integer, nullable=True)
    fecha_publicacion = Column(String, nullable=True)
    numero_edicion = Column(String, nullable=True)
    duracion = Column(Integer, nullable=True)
    director = Column(String, nullable=True)
    disponible = Column(Boolean, default=True)
    
    prestamos = relationship("PrestamoDB", back_populates="material")

class PrestamoDB(Base):
    __tablename__ = 'prestamos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(String, ForeignKey('usuarios.id_usuario'))
    id_material = Column(String, ForeignKey('materiales.codigo_inventario'))
    fecha_prestamo = Column(DateTime, default=datetime.now)
    fecha_devolucion = Column(DateTime, default=lambda: datetime.now() + timedelta(days=14))

    usuario = relationship("UsuarioDB", back_populates="prestamos")
    material = relationship("MaterialDB", back_populates="prestamos")

if __name__ == "__main__":
    # Шлях до бази даних у поточній папці
    db_path = 'biblioteca.db'
    db_uri = f'sqlite:///{db_path}'
    
    print(f"Спроба створити базу даних: {os.path.abspath(db_path)}")
    
    # Видаляємо існуючу базу даних, якщо вона є
    if os.path.exists(db_path):
        os.remove(db_path)
        print("Стара база даних видалена")
    
    try:
        engine = create_engine(db_uri)
        Base.metadata.create_all(engine)
        print("Базу даних успішно створено!")
        print(f"Розташування: {os.path.abspath(db_path)}")
    except Exception as e:
        print(f"Помилка при створенні бази даних: {e}")