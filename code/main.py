from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import List
import sqlite3
from pydantic import BaseModel
from typing_extensions import Self
from urllib import response
from urllib.request import Request
import os
import hashlib
from lib2to3.pytree import Base
from typing import Union


class Respuesta (BaseModel):
    message: str

class Clientes(BaseModel):
    id_cliente: int
    nombre: str
    email: str

class add_clientes(BaseModel):

    nombre: str
    email: str

class Usuarios(BaseModel):
    username: str
    level: int

app = FastAPI()

security = HTTPBasic()

DATABASE_URL = os.path.join("sql/users.sqlite")

def get_current_level(credentials: HTTPBasicCredentials = Depends(security)):
    password_b = hashlib.md5(credentials.password.encode())
    password = password_b.hexdigest()
    with sqlite3.connect(DATABASE_URL) as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT level FROM usuarios WHERE username = ? and password = ?",
            (credentials.username, password),
        )
        user = cursor.fetchone()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Basic"},
            )
    return user[0]

@app.get("/", response_model=Respuesta)
async def index ():
    return {"message": "API-REST"}

@app.get("/clientes/", response_model=List[Clientes],status_code=status.HTTP_202_ACCEPTED,summary="Regresa lista de usuarios",description="Regresa lista de usuarios")
async def clientes (level: int = Depends(get_current_level)):
    if level == 1: #Para usuario
        with sqlite3.connect('sql/clientes.sqlite') as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM clientes')
            response = cursor.fetchall()
            return response
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos",
            headers={"WWW-Authenticate": "Basic"},
        )

@app.get("/clientes/{id}", response_model=Clientes,status_code=status.HTTP_202_ACCEPTED,summary="Regresa el cliente",description="Regresa un cliente")
async def id (id: int, level: int = Depends(get_current_level)):
    if level == 1:
        with sqlite3.connect('sql/clientes.sqlite') as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute('select * from clientes where id_cliente = {};'.format(id))
            response = cursor.fetchone()
            return response
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos",
            headers={"WWW-Authenticate": "Basic"},
        )

@app.post("/clientes/", response_model=Respuesta,status_code=status.HTTP_202_ACCEPTED,summary="Agregar cliente: nombre y email",description="Agregar cliente se necesita nombre y email")
async def post_clientes (cliente: add_clientes, level: int = Depends(get_current_level)):
    if level == 1:
        with sqlite3.connect('sql/clientes.sqlite') as connection:
            cursor = connection.cursor()
            cursor.execute('INSERT INTO clientes(nombre, email) values ("{}","{}");'.format(cliente.nombre,cliente.email))
            connection.commit()
            response = {
                "message": "Cliente Agregado"
            }
            return response
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos",
            headers={"WWW-Authenticate": "Basic"},
        )
    
@app.put("/clientes/", response_model=Respuesta,status_code=status.HTTP_202_ACCEPTED,summary="Actualiza los datos",description="Actualiza los datos")
async def put_clientes (cliente: Clientes,level: int = Depends(get_current_level)):
    if level == 0: #Administrador
        with sqlite3.connect('sql/clientes.sqlite') as connection:
            cursor = connection.cursor()
            cursor.execute('UPDATE clientes SET nombre = "{}", email = "{}" WHERE id_cliente = {};'.format(cliente.nombre,cliente.email,cliente.id_cliente))
            connection.commit()
            response = {
                "message": "Cliente Actualizado"
            }
            return response
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos",
            headers={"WWW-Authenticate": "Basic"},
        )

@app.delete("/clientes/{id}",response_model=Respuesta, status_code=status.HTTP_202_ACCEPTED,summary="Borrar un cliente",description="Borrar un cliente")
async def delete_clientes (id: int,level: int = Depends(get_current_level)):
    if level == 0:
        with sqlite3.connect('sql/clientes.sqlite') as connection:
            cursor = connection.cursor()
            cursor.execute('DELETE FROM clientes WHERE id_cliente = {}'.format(id))
            connection.commit()
            response = {
                "message": "Cliente Eliminado"
            } 
            return response
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos",
            headers={"WWW-Authenticate": "Basic"},
        )