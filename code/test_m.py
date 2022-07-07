from urllib import response
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_message():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API-REST"}

def test_clientes():
    response = client.get("/clientes/")
    assert response.status_code == 200
    assert response.json() == [{"id_cliente":1,"nombre":"Oscar","email":"osc@email.com"},{"id_cliente":2,"nombre":"Badbuny","email":"bad@email.com"},{"id_cliente":3,"nombre":"Abisai","email":"abi@email.com"}]
                            
def test_clientes_id():
    response = client.get("/clientes/1")
    assert response.status_code == 200
    assert response.json() == {"id_cliente":1,"nombre":"Oscar","email":"osc@email.com"}

def test_agregar():
    data = {"nombre":"test","email":"test@test.com"}
    response = client.post("/clientes/", json=data)
    assert response.status_code == 200
    assert response.json() == {"message":"Cliente Agregado"}

def test_actualizar():
    data = {"id_cliente": 12,"nombre":"changed","email":"changed@changed.com"}
    response = client.put("/clientes/", json=data)
    assert response.status_code == 200
    assert response.json() == {"message":"Cliente Actualizado"}

def test_eliminar():
    response = client.delete("/clientes/12")
    assert response.status_code == 200
    assert response.json() == {"message": "Cliente Eliminado"} 