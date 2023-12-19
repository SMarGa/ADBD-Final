from flask import Blueprint,jsonify , request

from db import  get_db_connection

vehicle_bp = Blueprint('vehicle', __name__)

@vehicle_bp.route('/', methods=["GET"])
def getVehicleByMatricula():
    try:
        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Obtener vehículo por matrícula
        cur.execute('SELECT * FROM Vehiculo;' )
        data = cur.fetchall()
        cur.close()
        conn.close()

        if not data:
            return jsonify({"error": f"No se ha encontrado un ningún vehículo"}), 404

        return jsonify(data)

    except Exception as err:
        return jsonify({"error": str(err)}), 500

@vehicle_bp.route('/<string:matricula>', methods=["GET"])
def getVehicleByMatricula(matricula):
    try:
        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Obtener vehículo por matrícula
        cur.execute('SELECT * FROM Vehiculo WHERE Matricula = %s;', (matricula,))
        data = cur.fetchall()
        cur.close()
        conn.close()

        if not data:
            return jsonify({"error": f"No se ha encontrado un vehículo con la matrícula {matricula}"}), 404

        return jsonify(data)

    except Exception as err:
        return jsonify({"error": str(err)}), 500

@vehicle_bp.route('/', methods=["POST"])
def createVehicle():
    try:
        # Obtener datos del cuerpo de la solicitud
        data = request.get_json()

        # Validar que se proporcionaron todos los campos necesarios
        if "Matricula" not in data or "Tipo" not in data:
            return jsonify({"error": "La matrícula y el tipo son campos requeridos"}), 400

        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Insertar nuevo vehículo en la base de datos
        cur.execute('INSERT INTO Vehiculo (Matricula, Tipo, Capacidad_personas, Capacidad_residuos) VALUES (%s, %s, %s, %s) RETURNING Matricula;',
                    (data["Matricula"], data["Tipo"], data.get("Capacidad_personas"), data.get("Capacidad_residuos")))
        new_vehicle_matricula = cur.fetchone()[0]
        conn.commit()

        cur.close()
        conn.close()

        return jsonify({"message": "Vehículo creado exitosamente", "Matricula": new_vehicle_matricula}), 201

    except Exception as err:
        return jsonify({"error": str(err)}), 500
    
@vehicle_bp.route('/<string:matricula>', methods=["PATCH"])
def updateVehicleByMatricula(matricula):
    try:
        # Obtener datos del cuerpo de la solicitud
        data = request.get_json()

        # Validar que se proporcionaron datos para actualizar
        if not data:
            return jsonify({"error": "No se proporcionaron datos para actualizar"}), 400

        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Verificar si el vehículo existe antes de intentar actualizarlo
        cur.execute('SELECT * FROM Vehiculo WHERE Matricula = %s;', (matricula,))
        existing_vehicle = cur.fetchone()

        if not existing_vehicle:
            cur.close()
            conn.close()
            return jsonify({"error": f"No se ha encontrado un vehículo con la matrícula {matricula}"}), 404

        # Construir la consulta de actualización
        update_query = 'UPDATE Vehiculo SET '
        values = []

        for key, value in data.items():
            update_query += f'{key} = %s, '
            values.append(value)

        # Eliminar la coma extra al final y agregar la condición WHERE
        update_query = update_query.rstrip(', ') + f' WHERE Matricula = %s;'
        values.append(matricula)

        # Ejecutar la consulta de actualización
        cur.execute(update_query, tuple(values))
        conn.commit()

        cur.close()
        conn.close()

        return jsonify({"message": f"Vehículo con matrícula {matricula} actualizado exitosamente"})

    except Exception as err:
        return jsonify({"error": str(err)}), 500
    
@vehicle_bp.route('/<string:matricula>', methods=["DELETE"])
def deleteVehicleByMatricula(matricula):
    try:
        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Verificar si el vehículo existe antes de intentar eliminarlo
        cur.execute('SELECT * FROM Vehiculo WHERE Matricula = %s;', (matricula,))
        existing_vehicle = cur.fetchone()

        if not existing_vehicle:
            cur.close()
            conn.close()
            return jsonify({"error": f"No se ha encontrado un vehículo con la matrícula {matricula}"}), 404

        # Eliminar el vehículo de la base de datos
        cur.execute('DELETE FROM Vehiculo WHERE Matricula = %s;', (matricula,))
        conn.commit()

        cur.close()
        conn.close()

        return jsonify({"message": f"Vehículo con matrícula {matricula} eliminado exitosamente"})

    except Exception as err:
        return jsonify({"error": str(err)}), 500