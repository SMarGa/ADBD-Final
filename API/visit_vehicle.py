from flask import Blueprint,jsonify , request

from db import  get_db_connection

visit_vehicle_bp = Blueprint('visit_vehicle', __name__)


@visit_vehicle_bp.route('/', methods=["GET"])
def getVehicleVisit():
    try:
        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Obtener vehículo_visita por ID_Visit 
        cur.execute('SELECT * FROM Vehiculo_Visita;')
        data = cur.fetchall()
        cur.close()
        conn.close()

        if not data:
            return jsonify({"error": f"No se ha encontrado una relación Vehiculo_Visita"}), 404

        return jsonify(data)

    except Exception as err:
        return jsonify({"error": str(err)}), 500


@visit_vehicle_bp.route('/<int:id_visit>', methods=["GET"])
def getVehicleVisitByVisit(id_visit):
    try:
        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Obtener vehículo_visita por ID_Visit 
        cur.execute('SELECT * FROM Vehiculo_Visita WHERE ID_Visit = %s;', (id_visit,))
        data = cur.fetchall()
        cur.close()
        conn.close()

        if not data:
            return jsonify({"error": f"No se ha encontrado una relación Vehiculo_Visita con ID_Visit {id_visit}"}), 404

        return jsonify(data)

    except Exception as err:
        return jsonify({"error": str(err)}), 500
    

@visit_vehicle_bp.route('/<string:matricula>', methods=["GET"])
def getVehicleVisitByMat( matricula):
    try:
        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Obtener vehículo_visita por Matricula
        cur.execute('SELECT * FROM Vehiculo_Visita WHERE Matricula = %s;', (matricula,))
        data = cur.fetchall()
        cur.close()
        conn.close()

        if not data:
            return jsonify({"error": f"No se ha encontrado una relación Vehiculo_Visita con Matricula {matricula}"}), 404

        return jsonify(data)

    except Exception as err:
        return jsonify({"error": str(err)}), 500


@visit_vehicle_bp.route('/<int:id_visit>/<string:matricula>', methods=["DELETE"])
def deleteVehicleVisit(id_visit, matricula):
    try:
        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Verificar si la relación Vehiculo_Visita existe antes de intentar eliminarla
        cur.execute('SELECT * FROM Vehiculo_Visita WHERE ID_Visit = %s AND Matricula = %s;', (id_visit, matricula))
        existing_relationship = cur.fetchall()

        if not existing_relationship:
            cur.close()
            conn.close()
            return jsonify({"error": f"No se ha encontrado una relación Vehiculo_Visita con ID_Visit {id_visit} y Matricula {matricula}"}), 404

        # Eliminar la relación Vehiculo_Visita de la base de datos
        cur.execute('DELETE FROM Vehiculo_Visita WHERE ID_Visit = %s AND Matricula = %s;', (id_visit, matricula))
        conn.commit()

        cur.close()
        conn.close()

        return jsonify({"message": f"Relación Vehiculo_Visita con ID_Visit {id_visit} y Matricula {matricula} eliminada exitosamente"})

    except Exception as err:
        return jsonify({"error": str(err)}), 500
    

@visit_vehicle_bp.route('/', methods=["POST"])
def createVehicleVisit():
    try:
        # Obtener datos del cuerpo de la solicitud
        data = request.get_json()

        # Validar que se proporcionaron todos los campos necesarios
        if "ID_Visit" not in data or "Matricula" not in data:
            return jsonify({"error": "ID_Visit y Matricula son campos requeridos"}), 400

        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Verificar si la visita existe
        cur.execute('SELECT * FROM Visita WHERE ID_Visit = %s;', (data["ID_Visit"],))
        existing_visit = cur.fetchone()

        if not existing_visit:
            cur.close()
            conn.close()
            return jsonify({"error": f"No se ha encontrado una visita con ID_Visit {data['ID_Visit']}"}), 404

        # Verificar si el vehículo existe
        cur.execute('SELECT * FROM Vehiculo WHERE Matricula = %s;', (data["Matricula"],))
        existing_vehicle = cur.fetchone()

        if not existing_vehicle:
            cur.close()
            conn.close()
            return jsonify({"error": f"No se ha encontrado un vehículo con Matricula {data['Matricula']}"}), 404

        # Insertar nueva relación Vehiculo_Visita en la base de datos
        cur.execute('INSERT INTO Vehiculo_Visita (ID_Visit, Matricula) VALUES (%s, %s);',
                    (data["ID_Visit"], data["Matricula"]))
        conn.commit()

        cur.close()
        conn.close()

        return jsonify({"message": "Relación Vehiculo_Visita creada exitosamente"}), 201

    except Exception as err:
        return jsonify({"error": str(err)}), 500
    

@visit_vehicle_bp.route('/vehiculo_visita/<int:id_visit>/<string:matricula>', methods=["PATCH"])
def updateVehicleVisit(id_visit, matricula):
    try:
        # Obtener datos del cuerpo de la solicitud
        data = request.get_json()

        # Validar que se proporcionaron datos para actualizar
        if not data:
            return jsonify({"error": "No se proporcionaron datos para actualizar"}), 400

        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Verificar si la relación Vehiculo_Visita existe antes de intentar actualizarla
        cur.execute('SELECT * FROM Vehiculo_Visita WHERE ID_Visit = %s AND Matricula = %s;', (id_visit, matricula))
        existing_relationship = cur.fetchall()

        if not existing_relationship:
            cur.close()
            conn.close()
            return jsonify({"error": f"No se ha encontrado una relación Vehiculo_Visita con ID_Visit {id_visit} y Matricula {matricula}"}), 404

        # Verificar si la visita existe
        if "ID_Visit" in data:
            cur.execute('SELECT * FROM Visita WHERE ID_Visit = %s;', (data["ID_Visit"],))
            existing_visit = cur.fetchone()

            if not existing_visit:
                cur.close()
                conn.close()
                return jsonify({"error": f"No se ha encontrado una visita con ID_Visit {data['ID_Visit']}"}), 404

        # Verificar si el vehículo existe
        if "Matricula" in data:
            cur.execute('SELECT * FROM Vehiculo WHERE Matricula = %s;', (data["Matricula"],))
            existing_vehicle = cur.fetchone()

            if not existing_vehicle:
                cur.close()
                conn.close()
                return jsonify({"error": f"No se ha encontrado un vehículo con Matricula {data['Matricula']}"}), 404

        # Construir la consulta de actualización
        update_query = 'UPDATE Vehiculo_Visita SET '
        values = []

        for key, value in data.items():
            update_query += f'{key} = %s, '
            values.append(value)

        # Eliminar la coma extra al final y agregar la condición WHERE
        update_query = update_query.rstrip(', ') + f' WHERE ID_Visit = %s AND Matricula = %s;'
        values.extend([id_visit, matricula])

        # Ejecutar la consulta de actualización
        cur.execute(update_query, tuple(values))
        conn.commit()

        cur.close()
        conn.close()

        return jsonify({"message": f"Relación Vehiculo_Visita con ID_Visit {id_visit} y Matricula {matricula} actualizada exitosamente"})

    except Exception as err:
        return jsonify({"error": str(err)}), 500