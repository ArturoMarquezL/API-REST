DROP TABLE IF EXISTS clientes;

CREATE TABLE clientes(
    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR (50) NOT NULL,
    email VARCHAR (50) NOT NULL
);
INSERT INTO clientes (id_cliente, nombre, email) VALUES ("1","Oscar","osc@email.com");
INSERT INTO clientes (id_cliente, nombre, email) VALUES ("2","Badbuny","bad@email.com");
INSERT INTO clientes (id_cliente, nombre, email) VALUES ("3","Abisai","abi@email.com");


.headers ON
SELECT * FROM clientes;