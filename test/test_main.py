from fastapi.testclient import TestClient
from code.main import app
clientes = TestClient(app)

def test_index():
    response = clientes.get("/")
    data = {"mensaje":"Hola mundo"}
    assert response.status_code == 200
    assert response.json() == data