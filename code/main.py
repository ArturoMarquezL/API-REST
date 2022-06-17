from fastapi import FastAPI 
import sqlite3 
from typing import List
from pydantic import BaseModel

class Respuesta (BaseModel):
    message: str

class Clientes (BaseModel):
    id_cliente: int
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
async def read_item(id:int):
    with sqlite3.connect('sql/clientes.sqlite') as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM clientes where id_cliente={}".format(id))
        response = cursor.fetchone()
        return response