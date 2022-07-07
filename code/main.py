from fastapi import Depends, FastAPI, HTTPException, status
import sqlite3
from typing import List
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
import os
import hashlib
from lib2to3.pytree import Base
from typing import Union
from typing_extensions import Self
from urllib import response
from urllib.request import Request

class Respuesta (BaseModel):
    message: str

class Clientes(BaseModel):
    id_cliente: int
    nombre: str
    email: str

class add_cliente(BaseModel):

    nombre: str
    email: str

app = FastAPI()

@app.get ("/", response_model=Respuesta)
def index ():
    return {"message":"API-REST"}

@app.get ("/clientes/", response_model=List[Clientes])
async def clientes():
    with sqlite3.connect('sql/clientes.sqlite') as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM clientes")
        response = cursor.fetchall()
        return response
        

@app.get ("/clientes/{id}", response_model=Clientes)
async def id(id:int):
    with sqlite3.connect('sql/clientes.sqlite') as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM clientes where id_cliente={}".format(id))
        response = cursor.fetchone()
        return response



@app.post("/clientes/", response_model=Respuesta)
def post_clientes (cliente: add_cliente):
    with sqlite3.connect('sql/clientes.sqlite') as connection:
        connection.row_factory = sqlite3.Row
        cursor=connection.cursor()
        cursor.execute('INSERT INTO clientes (nombre, email) values ("{}","{}");'.format(cliente.nombre,cliente.email))
        cursor.fetchall()
        response = {"message":"Cliente Agregado"}
        return response


@app.put("/clientes/", response_model=Respuesta)
async def put_clientes (cliente: Clientes):
    with sqlite3.connect('sql/clientes.sqlite') as connection:
        connection.row_factory = sqlite3.Row
        cursor=connection.cursor()
        cursor.execute('UPDATE clientes SET nombre = "{}", email = "{}" where id_cliente = {};'.format(cliente.nombre, cliente.email, cliente.id_cliente))
        cursor.fetchall()
        response = {"message":"Cliente Actualizado"}
        return response
        

@app.delete("/clientes/{id}",response_model=Respuesta)
async def delete_clientes (id: int):
    with sqlite3.connect('sql/clientes.sqlite') as connection:
        cursor = connection.cursor()
        cursor.execute('delete from clientes where id_cliente = {}'.format(id))
        connection.commit()
        response = {"message": "Cliente Eliminado"} 
        return response