-- Proyecto de Bases de Datos: Gestión del PIRS

-- Creación de tipos de datos para las tablas

CREATE TYPE tipo_residuo AS ENUM ('plástico', 'papel', 'orgánico', 'vidrio');
CREATE TYPE turno AS ENUM ('mañana', 'tarde');
CREATE TYPE ocupacion AS ENUM ('tecnico', 'guia', 'transportista');
CREATE TYPE tipo_vehiculo AS ENUM ('transporte_residuos', 'transporte_personas');
CREATE TYPE tipo_carnet AS ENUM ('B', 'C', 'D');

-- Creación de tablas

CREATE TABLE Celda (
    ID_C SERIAL PRIMARY KEY,
    Nombre VARCHAR(255),
    Capacidad NUMERIC CHECK (Capacidad > 0),
    Estado VARCHAR(50) NOT NULL
);

CREATE TABLE Instalacion (
    ID_I SERIAL PRIMARY KEY,
    Tipo tipo_residuo[] NOT NULL CHECK (array_length(Tipo, 1) <= 4),
    Nombre VARCHAR(255),
    Capacidad NUMERIC CHECK (Capacidad > 0),
    Estado_operativo BOOLEAN NOT NULL
);

CREATE TABLE Residuo (
    ID_R SERIAL PRIMARY KEY,
    Tipo tipo_residuo NOT NULL,
    Cantidad NUMERIC CHECK (Cantidad > 0),
    Origen VARCHAR(255),
    Fecha_de_recepcion DATE NOT NULL,
    ID_C INTEGER,
    ID_I INTEGER,
    FOREIGN KEY (ID_C) REFERENCES Celda(ID_C) ON DELETE CASCADE,
    FOREIGN KEY (ID_I) REFERENCES Instalacion(ID_I)
);

CREATE TABLE Maquinas (
    ID_M SERIAL PRIMARY KEY,
    Tipo VARCHAR(100) NOT NULL,
    Estado_operativo BOOLEAN NOT NULL,
    Ubicacion VARCHAR(255) NOT NULL,
    ID_I INTEGER,
    FOREIGN KEY (ID_I) REFERENCES Instalacion(ID_I) ON DELETE SET NULL
);

CREATE TABLE Empleado (
    ID_Emp SERIAL PRIMARY KEY,
    Nombre VARCHAR(255) NOT NULL,
    N_telf VARCHAR(15) CHECK (N_telf ~ '^[0-9]+$'),
    Turno turno NOT NULL,
    Ocupacion ocupacion NOT NULL
);

CREATE TABLE Tecnico (
    ID_Emp INTEGER PRIMARY KEY,
    Especialidad VARCHAR(255) NOT NULL,
    FOREIGN KEY (ID_Emp) REFERENCES Empleado(ID_Emp) ON DELETE CASCADE
);

CREATE TABLE Tecnico_Instalacion (
    ID_I INTEGER,
    ID_Emp INTEGER,
    PRIMARY KEY (ID_I, ID_Emp),
    FOREIGN KEY (ID_I) REFERENCES Instalacion(ID_I),
    FOREIGN KEY (ID_Emp) REFERENCES Tecnico(ID_Emp)
);

CREATE TABLE Transportista (
    ID_Emp INTEGER PRIMARY KEY,
    Tipo_Carnet tipo_carnet NOT NULL,
    FOREIGN KEY (ID_Emp) REFERENCES Empleado(ID_Emp) ON DELETE CASCADE
);


CREATE TABLE Vehiculo (
    Matricula VARCHAR(20) PRIMARY KEY CHECK (Matricula ~ '^[0-9]{4}[A-Z]{3}$'),
    Tipo tipo_vehiculo NOT NULL,
    Capacidad_personas INTEGER CHECK (Capacidad_personas > 0 OR Capacidad_personas IS NULL),
    Capacidad_residuos INTEGER CHECK (Capacidad_residuos > 0 OR Capacidad_residuos IS NULL),
    CHECK (
        (Tipo = 'transporte_residuos' AND Capacidad_personas IS NULL AND Capacidad_residuos IS NOT NULL) OR
        (Tipo = 'transporte_personas' AND Capacidad_residuos IS NULL AND Capacidad_personas IS NOT NULL)
    )
);

CREATE TABLE Transportista_Vehiculo (
    ID_Emp INTEGER,
    Matricula VARCHAR(20),
    PRIMARY KEY (ID_Emp, Matricula),
    FOREIGN KEY (ID_Emp) REFERENCES Transportista(ID_Emp) ON DELETE CASCADE,
    FOREIGN KEY (Matricula) REFERENCES Vehiculo(Matricula) ON DELETE CASCADE
);

CREATE TABLE Ruta (
    ID_Ruta SERIAL PRIMARY KEY,
    Duracion INTEGER CHECK (Duracion > 0 AND Duracion <= 480),
    N_paradas INTEGER CHECK (N_paradas > 0),
    T_por_parada INTEGER -- calculado con un trigger
);

CREATE TABLE Vehiculo_Ruta (
    ID_Ruta INTEGER,
    Matricula VARCHAR(20),
    PRIMARY KEY (ID_Ruta, Matricula),
    FOREIGN KEY (ID_Ruta) REFERENCES Ruta(ID_Ruta) ON DELETE CASCADE,
    FOREIGN KEY (Matricula) REFERENCES Vehiculo(Matricula) ON DELETE CASCADE
);

CREATE TABLE Visita (
    ID_Visit SERIAL PRIMARY KEY,
    Duracion INTEGER CHECK (Duracion > 0 AND Duracion <= 480),
    N_visitantes INTEGER CHECK (N_visitantes > 0)
);

CREATE TABLE Vehiculo_Visita (
    ID_Visit INTEGER,
    Matricula VARCHAR(20),
    PRIMARY KEY (ID_Visit, Matricula),
    FOREIGN KEY (ID_Visit) REFERENCES Visita(ID_Visit) ON DELETE SET NULL,
    FOREIGN KEY (Matricula) REFERENCES Vehiculo(Matricula) ON DELETE SET NULL
);

CREATE TABLE Guia (
    ID_Emp INTEGER PRIMARY KEY,
    Idiomas VARCHAR[] NOT NULL,
    FOREIGN KEY (ID_Emp) REFERENCES Empleado(ID_Emp) ON DELETE CASCADE
);

CREATE TABLE Guia_Visita (
    ID_Visit INTEGER,
    ID_Emp INTEGER,
    ID_I INTEGER,
    PRIMARY KEY (ID_Visit, ID_Emp, ID_I),
    FOREIGN KEY (ID_Visit) REFERENCES Visita(ID_Visit) ON DELETE CASCADE,
    FOREIGN KEY (ID_Emp) REFERENCES Guia(ID_Emp) ON DELETE CASCADE,
    FOREIGN KEY (ID_I) REFERENCES Instalacion(ID_I) ON DELETE CASCADE
);


-- Creación de funciones

CREATE OR REPLACE FUNCTION calcular_tiempo_por_parada()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.N_paradas > 0 THEN
        NEW.T_por_parada := NEW.Duracion / NEW.N_paradas;
    ELSE
        NEW.T_por_parada := NULL;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION verificar_compatibilidad_carnet()
RETURNS TRIGGER AS $$
DECLARE
    tipo_carnet_transportista tipo_carnet;
    capacidad_personas_vehiculo INTEGER;
BEGIN
    SELECT Tipo_Carnet INTO tipo_carnet_transportista FROM Transportista WHERE ID_Emp = NEW.ID_Emp;
    SELECT Capacidad_personas INTO capacidad_personas_vehiculo FROM Vehiculo WHERE Matricula = NEW.Matricula;
    IF tipo_carnet_transportista != 'D' AND capacidad_personas_vehiculo > 8 THEN
        RAISE EXCEPTION 'El transportista no tiene un carnet adecuado para este vehículo.';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION eliminar_duplicados_tipo()
RETURNS TRIGGER AS $$
BEGIN
    NEW.Tipo := ARRAY(SELECT DISTINCT UNNEST(NEW.Tipo));
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Creación de triggers

CREATE TRIGGER actualizar_tiempo_por_parada_trigger
BEFORE INSERT OR UPDATE ON Ruta
FOR EACH ROW EXECUTE FUNCTION calcular_tiempo_por_parada();

CREATE TRIGGER verificar_compatibilidad_carnet_trigger
BEFORE INSERT OR UPDATE ON Transportista_Vehiculo
FOR EACH ROW EXECUTE FUNCTION verificar_compatibilidad_carnet();

CREATE TRIGGER eliminar_duplicados_tipo_trigger
BEFORE INSERT OR UPDATE ON Instalacion
FOR EACH ROW EXECUTE FUNCTION eliminar_duplicados_tipo();

-- Insersiones:

INSERT INTO Celda (Nombre, Capacidad, Estado) VALUES
('Celda 1', 1000, 'Disponible'),
('Celda 2', 1500, 'Llena'),
('Celda 3', 800, 'En Mantenimiento'),
('Celda 4', 1200, 'Disponible'),
('Celda 5', 1100, 'Llena');

INSERT INTO Instalacion (Tipo, Nombre, Capacidad, Estado_operativo) VALUES
(ARRAY['plástico', 'papel']::tipo_residuo[], 'Instalacion 1', 5000, TRUE),
(ARRAY['orgánico', 'vidrio']::tipo_residuo[], 'Instalacion 2', 3000, FALSE);

INSERT INTO Residuo (Tipo, Cantidad, Origen, Fecha_de_recepcion, ID_C, ID_I) VALUES
('plástico', 100, 'Familiar', '2023-01-01', 1, 1),
('papel', 200, 'Empresas', '2023-01-02', 1, 1),
('papel', 200, 'Otros', '2023-01-02', 1, 1),
('orgánico', 150, 'Familiar', '2023-01-03', 2, 2),
('vidrio', 250, 'Empresas', '2023-01-04', 2, 2),
('plástico', 300, 'Otros', '2023-01-05', 1, 1),
('papel', 350, 'Familiar', '2023-01-06', 1, 1),
('orgánico', 400, 'Empresas', '2023-01-07', 2, 2),
('vidrio', 450, 'Otros', '2023-01-08', 2, 2),
('plástico', 500, 'Familiar', '2023-01-09', 1, 1),
('papel', 550, 'Empresas', '2023-01-10', 1, 1),
('orgánico', 600, 'Otros', '2023-01-11', 2, 2),
('vidrio', 650, 'Familiar', '2023-01-12', 2, 2),
('plástico', 700, 'Empresas', '2023-01-13', 1, 1),
('papel', 750, 'Otros', '2023-01-14', 1, 1),
('orgánico', 800, 'Familiar', '2023-01-15', 2, 2);

INSERT INTO Maquinas (Tipo, Estado_operativo, Ubicacion, ID_I) VALUES
('Trituradora', TRUE, 'Norte', 1),
('Compactadora', FALSE, 'Sure', 1),
('Separadora', TRUE, 'Este', 2),
('Incineradora', FALSE, 'Oeste', 2);

INSERT INTO Empleado (Nombre, N_telf, Turno, Ocupacion) VALUES
('Alejandro García', '612345678', 'mañana', 'tecnico'),
('Beatriz Ruiz', '623456789', 'tarde', 'tecnico'),
('Carlos Sánchez', '634567890', 'mañana', 'tecnico'),
('Diana Molina', '645678901', 'tarde', 'transportista'),
('Eduardo López', '656789012', 'mañana', 'transportista'),
('Fernanda Jiménez', '667890123', 'tarde', 'transportista'),
('Gonzalo Fernández', '678901234', 'mañana', 'guia'),
('Héctor Torres', '689012345', 'tarde', 'guia'),
('Irene Gómez', '690123456', 'mañana', 'guia');

INSERT INTO Tecnico (ID_Emp, Especialidad) VALUES
(1, 'Electrónica'),
(2, 'Mecánica'),
(3, 'Software');

INSERT INTO Tecnico_Instalacion (ID_I, ID_Emp) VALUES
(1, 1),
(1, 2),
(2, 3);

INSERT INTO Transportista (ID_Emp, Tipo_Carnet) VALUES
(4, 'B'),
(5, 'C'),
(6, 'D');

INSERT INTO Vehiculo (Matricula, Tipo, Capacidad_personas, Capacidad_residuos) VALUES
('1234BCD', 'transporte_personas', 5, NULL),
('2345CDE', 'transporte_personas', 8, NULL),
('3456DEF', 'transporte_residuos', NULL, 1000),
('4567EFG', 'transporte_residuos', NULL, 2000),
('5678FGH', 'transporte_personas', 4, NULL);

INSERT INTO Transportista_Vehiculo (ID_Emp, Matricula) VALUES
(4, '1234BCD'),
(5, '3456DEF'),
(6, '4567EFG');

INSERT INTO Ruta (Duracion, N_paradas) VALUES
(120, 5),
(180, 8),
(240, 10),
(300, 12),
(360, 15);

INSERT INTO Vehiculo_Ruta (ID_Ruta, Matricula) VALUES
(1, '1234BCD'),
(2, '2345CDE'),
(3, '3456DEF'),
(4, '4567EFG'),
(5, '5678FGH');

INSERT INTO Visita (Duracion, N_visitantes) VALUES
(60, 10),
(90, 15),
(120, 20),
(150, 25),
(180, 30);

INSERT INTO Vehiculo_Visita (ID_Visit, Matricula) VALUES
(1, '1234BCD'),
(2, '2345CDE'),
(3, '3456DEF'),
(4, '4567EFG'),
(5, '5678FGH');

INSERT INTO Guia (ID_Emp, Idiomas) VALUES
(7, ARRAY['Español', 'Inglés']),
(8, ARRAY['Español', 'Francés']),
(9, ARRAY['Español', 'Alemán']);

INSERT INTO Guia_Visita (ID_Visit, ID_Emp, ID_I) VALUES
(1, 7, 1),
(2, 8, 1),
(3, 9, 2),
(4, 7, 2),
(5, 8, 2);

-- Pruebas: probar las eliminaciones con restricciones de integridad, es decir las FK, probar los trigger y checks, operaciones de actualizacion..
