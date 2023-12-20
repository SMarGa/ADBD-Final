from flask import Blueprint,jsonify , request

from db import  get_db_connection

trans_vehicle_bp = Blueprint('trans_vehicle', __name__)


@trans_vehicle_bp.route('/', methods=["GET"])
def getTransporterVehicle():
    try:
        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Obtener Transportista_Vehiculo 
        cur.execute('SELECT * FROM Transportista_Vehiculo;')
        data = cur.fetchone()
        cur.close()
        conn.close()

        if not data:
            return jsonify({"error": f"No se ha encontrado ninguna relación Transportista_Vehiculo"}), 404
        
        return jsonify(data)

    except Exception as err:
        return jsonify({"error": str(err)}), 500
    


@trans_vehicle_bp.route('/trans/<int:id_emp>/', methods=["GET"])
def getTransporterVehicleByEmpId(id_emp):
    try:
        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Obtener Transportista_Vehiculo por ID_Emp
        cur.execute('SELECT * FROM Transportista_Vehiculo WHERE ID_Emp = %s;', (id_emp,))
        data = cur.fetchone()
        cur.close()
        conn.close()

        if not data:
            return jsonify({"error": f"No se ha encontrado una relación Transportista_Vehiculo con ID_Emp {id_emp}"}), 404
        
        return jsonify(data)

    except Exception as err:
        return jsonify({"error": str(err)}), 500
    
@trans_vehicle_bp.route('/vehi/<string:matricula>/', methods=["GET"])
def getTransporterVehicleByVehMat(matricula):
    try:
        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Obtener Transportista_Vehiculo por Matricula
        cur.execute('SELECT * FROM Transportista_Vehiculo WHERE Matricula = %s;', (matricula,))
        data = cur.fetchone()
        cur.close()
        conn.close()

        if not data:
            return jsonify({"error": f"No se ha encontrado una relación Transportista_Vehiculo con Matricula {matricula}"}), 404
        
        return jsonify(data)

    except Exception as err:
        return jsonify({"error": str(err)}), 500



@trans_vehicle_bp.route('/', methods=["POST"])
def createTransporterVehicle():
    try:
        # Obtener datos del cuerpo de la solicitud
        data = request.get_json()

        # Validar que se proporcionaron todos los campos necesarios
        if "ID_Emp" not in data or "Matricula" not in data:
            return jsonify({"error": "ID_Emp y Matricula son campos requeridos"}), 400

        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Verificar si el transportista existe
        cur.execute('SELECT * FROM Transportista WHERE ID_Emp = %s;', (data["ID_Emp"],))
        existing_transporter = cur.fetchone()

        if not existing_transporter:
            cur.close()
            conn.close()
            return jsonify({"error": f"No se ha encontrado un transportista con ID_Emp {data['ID_Emp']}"}), 404

        # Verificar si el vehículo existe
        cur.execute('SELECT * FROM Vehiculo WHERE Matricula = %s;', (data["Matricula"],))
        existing_vehicle = cur.fetchone()

        if not existing_vehicle:
            cur.close()
            conn.close()
            return jsonify({"error": f"No se ha encontrado un vehículo con Matricula {data['Matricula']}"}), 404

        # Insertar nueva relación Transportista_Vehiculo en la base de datos
        cur.execute('INSERT INTO Transportista_Vehiculo (ID_Emp, Matricula) VALUES (%s, %s);', (data["ID_Emp"], data["Matricula"]))
        conn.commit()

        cur.close()
        conn.close()

        return jsonify({"message": "Relación Transportista_Vehiculo creada exitosamente"}), 201

    except Exception as err:
        return jsonify({"error": str(err)}), 500




@trans_vehicle_bp.route('/<int:id_emp>/<string:matricula>', methods=["PATCH"])
def updateTransporterVehicleById(id_emp, matricula):
    try:
        # Obtener datos del cuerpo de la solicitud
        data = request.get_json()

        # Validar que se proporcionaron datos para actualizar
        if not data:
            return jsonify({"error": "No se proporcionaron datos para actualizar"}), 400

        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Verificar si la relación Transportista_Vehiculo existe antes de intentar actualizarla
        cur.execute('SELECT * FROM Transportista_Vehiculo WHERE ID_Emp = %s AND Matricula = %s;', (id_emp, matricula))
        existing_relationship = cur.fetchall()

        if not existing_relationship:
            cur.close()
            conn.close()
            return jsonify({"error": f"No se ha encontrado una relación Transportista_Vehiculo con ID_Emp {id_emp} y Matricula {matricula}"}), 404

        # Construir la consulta de actualización
        update_query = 'UPDATE Transportista_Vehiculo SET '
        values = []

        for key, value in data.items():
            update_query += f'{key} = %s, '
            values.append(value)

        # Eliminar la coma extra al final y agregar la condición WHERE
        update_query = update_query.rstrip(', ') + f' WHERE ID_Emp = %s AND Matricula = %s;'
        values.extend([id_emp, matricula])

        # Ejecutar la consulta de actualización
        cur.execute(update_query, tuple(values))
        conn.commit()

        cur.close()
        conn.close()

        return jsonify({"message": f"Relación Transportista_Vehiculo con ID_Emp {id_emp} y Matricula {matricula} actualizada exitosamente"})

    except Exception as err:
        return jsonify({"error": str(err)}), 500
    


@trans_vehicle_bp.route('/<int:id_emp>/<string:matricula>', methods=["DELETE"])
def deleteTransporterVehicleById(id_emp, matricula):
    try:
        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Verificar si la relación Transportista_Vehiculo existe antes de intentar eliminarla
        cur.execute('SELECT * FROM Transportista_Vehiculo WHERE ID_Emp = %s AND Matricula = %s;', (id_emp, matricula))
        existing_relationship = cur.fetchall()

        if not existing_relationship:
            cur.close()
            conn.close()
            return jsonify({"error": f"No se ha encontrado una relación Transportista_Vehiculo con ID_Emp {id_emp} y Matricula {matricula}"}), 404

        # Eliminar la relación Transportista_Vehiculo de la base de datos
        cur.execute('DELETE FROM Transportista_Vehiculo WHERE ID_Emp = %s AND Matricula = %s;', (id_emp, matricula))
        conn.commit()

        cur.close()
        conn.close()

        return jsonify({"message": f"Relación Transportista_Vehiculo con ID_Emp {id_emp} y Matricula {matricula} eliminada exitosamente"})

    except Exception as err:
        return jsonify({"error": str(err)}), 500