# GestorBiblioteca.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modelos import Base, UsuarioDB, MaterialDB, PrestamoDB
from datetime import datetime, timedelta
import uuid
import os

class GestorBiblioteca:
    def __init__(self):
        # Визначаємо шлях до бази даних у поточній папці
        db_path = os.path.join(os.path.dirname(__file__), 'biblioteca.db')
        db_uri = f'sqlite:///{db_path}'
        
        print(f"Підключення до бази даних: {db_path}")
        
        # Створюємо рушій та підключаємось до бази даних
        self.engine = create_engine(db_uri)
        
        # Створюємо фабрику сесій
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        
        # Створюємо всі таблиці, якщо вони ще не існують
        Base.metadata.create_all(self.engine)
        print("Підключення до бази даних успішне")

    def agregar_usuario(self, nombre, apellido):
        usuario = UsuarioDB(nombre=nombre, apellido=apellido)
        self.session.add(usuario)
        self.session.commit()
        return usuario.id_usuario

    def listar_usuarios(self):
        return self.session.query(UsuarioDB).all()

    def agregar_material(self, tipo, titulo, **kwargs):
        codigo = uuid.uuid4().hex[:6].upper()
        material = MaterialDB(codigo_inventario=codigo, titulo=titulo, tipo=tipo, disponible=True)

        if tipo == "libro":
            material.autor = kwargs.get("autor")
            material.numero_paginas = kwargs.get("numero_paginas")
            material.isbn = kwargs.get("isbn")
        elif tipo == "revista":
            material.fecha_publicacion = kwargs.get("fecha_publicacion")
            material.numero_edicion = kwargs.get("numero_edicion")
        elif tipo == "dvd":
            material.duracion = kwargs.get("duracion")
            material.director = kwargs.get("director")
        else:
            raise ValueError("Tipo de material no válido.")

        self.session.add(material)
        self.session.commit()
        return codigo

    def listar_materiales(self):
        return self.session.query(MaterialDB).all()

    def buscar_material(self, codigo):
        return self.session.query(MaterialDB).filter_by(codigo_inventario=codigo).first()

    def borrar_material(self, codigo):
        material = self.buscar_material(codigo)
        if material:
            self.session.delete(material)
            self.session.commit()
            return True
        return False

    def agregar_prestamo(self, id_usuario, id_material):
        usuario = self.session.query(UsuarioDB).filter_by(id_usuario=id_usuario).first()
        material = self.session.query(MaterialDB).filter_by(codigo_inventario=id_material).first()

        if not usuario or not material or not material.disponible:
            return False

        prestamo = PrestamoDB(
            id_usuario=id_usuario,
            id_material=id_material,
            fecha_prestamo=datetime.now(),
            fecha_devolucion=datetime.now() + timedelta(days=14)
        )
        material.disponible = False
        self.session.add(prestamo)
        self.session.commit()
        return True

    def listar_prestamos(self):
        return self.session.query(PrestamoDB).all()


    def info_usuario(self, id_usuario):
        usuario = self.session.query(UsuarioDB).filter_by(id_usuario=id_usuario).first()
        if not usuario:
            return None
        if usuario.prestamos:
            prestamos = [(prestamo.id_material, prestamo.material.titulo, prestamo.fecha_devolucion) for prestamo in usuario.prestamos]
        else:
            prestamos = []
        return {
            "nombre": usuario.nombre,
            "apellido": usuario.apellido,
            "prestamos": prestamos
        }

    def __del__(self):
        # Закриваємо сесію при знищенні об'єкта
        if hasattr(self, 'session'):
            self.session.close()
            print("З'єднання з базою даних закрито")