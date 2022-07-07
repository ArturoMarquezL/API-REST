from fastapi.testclient import TestClient
from code.main import app


clientes = TestClient(app)


def test_index():
	response = clientes.get('/')
	data = {"message": 'Hola Mundo'}
	assert response.status_code == 200
	assert response.json()==data


def test_limite():
	response = clientes.get('/clientes/?offeset=1&limit=3')
	data = [{"id_cliente":1,"nombre":"Oscar","email":"osc@gmail.com"},
	{"id_cliente":2,"nombre":"Badbuny":"bad@gmail.com"},
	{"id_cliente":3,"nombre":"Abisai","email":"abi@gmail.com"}]
	assert response.status_code == 200
	assert response.json()==data


def test_id():
	response = clientes.get('/consulta/3')
	data = [{"id_cliente":3,"nombre":"Abisai","email":"abi@gmail.com"}]
	assert response.status_code == 200
	assert response.json()==data



def test_insert():
	response = clientes.post('/insertar/Cliente2/cliente2@gmail.com')
	data = {"mensaje":"Cliente agregado"}
	assert response.status_code == 200
	assert response.json()==data


def test_update():
	response = clientes.put('/actulizar/4/Cliente%20Actualizado/clienteactualizado%40gmail.com')
	data = {"mensaje": "Cliente Actualizado"}
	assert response.status_code == 200
	assert response.json()==data


def test_delete():
	response = clientes.delete('/eliminar/6')
	data = {"mensaje":"Cliente borrado"}
	assert response.status_code == 200
	assert response.json()==data