from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uvicorn
import os
from biblioteca.modelos import Base, UsuarioDB, MaterialDB, PrestamoDB
from biblioteca.GestorBiblioteca import GestorBiblioteca
app = FastAPI(title="API Бібліотеки")

# Дозволяємо CORS для всіх джерел
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Моделі Pydantic для валідації даних
class UsuarioBase(BaseModel):
    nombre: str
    apellido: str

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioResponse(UsuarioBase):
    id_usuario: str
    
    class Config:
        from_attributes = True

class MaterialBase(BaseModel):
    titulo: str
    tipo: str  # 'libro', 'revista', 'dvd'
    autor: Optional[str] = None
    isbn: Optional[str] = None
    numero_paginas: Optional[int] = None
    fecha_publicacion: Optional[str] = None
    numero_edicion: Optional[str] = None
    duracion: Optional[int] = None

class MaterialCreate(MaterialBase):
    pass

class MaterialResponse(MaterialBase):
    codigo_inventario: str
    
    class Config:
        from_attributes = True

class PrestamoBase(BaseModel):
    id_usuario: str
    id_material: str

class PrestamoCreate(PrestamoBase):
    pass

class PrestamoResponse(PrestamoBase):
    id: int
    fecha_prestamo: datetime
    fecha_devolucion: datetime
    
    class Config:
        from_attributes = True

# Ініціалізація менеджера бібліотеки
gestor = GestorBiblioteca()

# Користувачі
@app.post("/usuarios/", response_model=UsuarioResponse)
def crear_usuario(usuario: UsuarioCreate):
    nuevo_usuario = UsuarioDB(**usuario.dict())
    gestor.session.add(nuevo_usuario)
    gestor.session.commit()
    gestor.session.refresh(nuevo_usuario)
    return nuevo_usuario

@app.get("/usuarios/", response_model=List[UsuarioResponse])
def listar_usuarios():
    return gestor.session.query(UsuarioDB).all()

# Матеріали
@app.post("/materiales/", response_model=MaterialResponse)
def crear_material(material: MaterialCreate):
    try:
        # Конвертуємо Pydantic модель у словник
        material_data = material.dict()
        
        # Створюємо новий матеріал
        nuevo_material = MaterialDB(**material_data)
        
        # Додаємо та зберігаємо зміни
        gestor.session.add(nuevo_material)
        gestor.session.commit()
        gestor.session.refresh(nuevo_material)
        
        return nuevo_material
    except Exception as e:
        gestor.session.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/materiales/", response_model=List[MaterialResponse])
def listar_materiales():
    return gestor.session.query(MaterialDB).all()

# Позики
@app.post("/prestamos/", response_model=PrestamoResponse)
def crear_prestamo(prestamo: PrestamoCreate):
    nuevo_prestamo = PrestamoDB(**prestamo.dict())
    gestor.session.add(nuevo_prestamo)
    gestor.session.commit()
    gestor.session.refresh(nuevo_prestamo)
    return nuevo_prestamo

@app.get("/prestamos/", response_model=List[PrestamoResponse])
def listar_prestamos():
    return gestor.session.query(PrestamoDB).all()

# Інформація про користувача
@app.get("/usuarios/{usuario_id}/info")
def obtener_info_usuario(usuario_id: str):
    return gestor.obtener_info_usuario(usuario_id)

if __name__ == "__main__":
    uvicorn.run("aplicacion:app", host="0.0.0.0", port=8000, reload=True)