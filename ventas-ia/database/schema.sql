CREATE DATABASE ventas_db;

USE ventas_db;

CREATE TABLE clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    limite_credito DECIMAL(10,2) NOT NULL
);

CREATE TABLE ventas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT,
    monto DECIMAL(10,2),
    fecha DATE,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);

CREATE TABLE cobranzas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT,
    monto DECIMAL(10,2),
    fecha DATE,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);
