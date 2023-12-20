from flask import Blueprint,jsonify , request

from db import  get_db_connection

tec_inst_bp = Blueprint('tec_inst', __name__)



@tec_inst_bp.route('/tec/<int:id_emp>', methods=["GET"])
def getTechnicianInstallationByEmpId(id_emp):
    try:
        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Obtener Tecnico_Instalacion por  ID_Emp
        cur.execute('SELECT * FROM Tecnico_Instalacion WHERE AND ID_Emp = %s;', (id_emp,))
        data = cur.fetchone()
        cur.close()
        conn.close()

        if not data:
            return jsonify({"error": f"No se ha encontrado una relación Tecnico_Instalacion con  ID_Emp {id_emp}"}), 404

        return jsonify(data)

    except Exception as err:
        return jsonify({"error": str(err)}), 500
    

@tec_inst_bp.route('/inst/<int:id_i>', methods=["GET"])
def getTechnicianInstallationByInstId(id_i):
    try:
        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Obtener Tecnico_Instalacion por ID_I 
        cur.execute('SELECT * FROM Tecnico_Instalacion WHERE ID_I = %s;', (id_i,))
        data = cur.fetchone()
        cur.close()
        conn.close()

        if not data:
            return jsonify({"error": f"No se ha encontrado una relación Tecnico_Instalacion con ID_I {id_i}"}), 404

        return jsonify(data)

    except Exception as err:
        return jsonify({"error": str(err)}), 500
    

@tec_inst_bp.route('/', methods=["GET"])
def getTechnicianInstallation():
    try:
        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Obtener Tecnico_Instalacion
        cur.execute('SELECT * FROM Tecnico_Instalacion WHERE ID_I = %s;')
        data = cur.fetchone()
        cur.close()
        conn.close()

        if not data:
            return jsonify({"error": f"No se ha encontrado niguna relación Tecnico_Instalacion"}), 404

        return jsonify(data)

    except Exception as err:
        return jsonify({"error": str(err)}), 500
    



@tec_inst_bp.route('/', methods=["POST"])
def createTechnicianInstallation():
    try:
        # Obtener datos del cuerpo de la solicitud
        data = request.get_json()

        # Validar que se proporcionaron todos los campos necesarios
        if "ID_I" not in data or "ID_Emp" not in data:
            return jsonify({"error": "ID_I e ID_Emp son campos requeridos"}), 400

        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Verificar si la instalación existe
        cur.execute('SELECT * FROM Instalacion WHERE ID_I = %s;', (data["ID_I"],))
        existing_installation = cur.fetchone()

        if not existing_installation:
            cur.close()
            conn.close()
            return jsonify({"error": f"No se ha encontrado una instalación con ID_I {data['ID_I']}"}), 404

        # Verificar si el técnico existe
        cur.execute('SELECT * FROM Tecnico WHERE ID_Emp = %s;', (data["ID_Emp"],))
        existing_technician = cur.fetchone()

        if not existing_technician:
            cur.close()
            conn.close()
            return jsonify({"error": f"No se ha encontrado un técnico con ID_Emp {data['ID_Emp']}"}), 404

        # Insertar nueva relación Tecnico_Instalacion en la base de datos
        cur.execute('INSERT INTO Tecnico_Instalacion (ID_I, ID_Emp) VALUES (%s, %s);', (data["ID_I"], data["ID_Emp"]))
        conn.commit()

        cur.close()
        conn.close()

        return jsonify({"message": "Relación Tecnico_Instalacion creada exitosamente"}), 201

    except Exception as err:
        return jsonify({"error": str(err)}), 500
    

@tec_inst_bp.route('/<int:id_i>/<int:id_emp>', methods=["PATCH"])
def updateTechnicianInstallationById(id_i, id_emp):
    try:
        # Obtener datos del cuerpo de la solicitud
        data = request.get_json()

        # Validar que se proporcionaron datos para actualizar
        if not data:
            return jsonify({"error": "No se proporcionaron datos para actualizar"}), 400

        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Verificar si la relación Tecnico_Instalacion existe antes de intentar actualizarla
        cur.execute('SELECT * FROM Tecnico_Instalacion WHERE ID_I = %s AND ID_Emp = %s;', (id_i, id_emp))
        existing_relationship = cur.fetchall()

        if not existing_relationship:
            cur.close()
            conn.close()
            return jsonify({"error": f"No se ha encontrado una relación Tecnico_Instalacion con ID_I {id_i} e ID_Emp {id_emp}"}), 404

        # Construir la consulta de actualización
        update_query = 'UPDATE Tecnico_Instalacion SET '
        values = []

        for key, value in data.items():
            update_query += f'{key} = %s, '
            values.append(value)

        # Eliminar la coma extra al final y agregar la condición WHERE
        update_query = update_query.rstrip(', ') + f' WHERE ID_I = %s AND ID_Emp = %s;'
        values.extend([id_i, id_emp])

        # Ejecutar la consulta de actualización
        cur.execute(update_query, tuple(values))
        conn.commit()

        cur.close()
        conn.close()

        return jsonify({"message": f"Relación Tecnico_Instalacion con ID_I {id_i} e ID_Emp {id_emp} actualizada exitosamente"})

    except Exception as err:
        return jsonify({"error": str(err)}), 500
    


@tec_inst_bp.route('/tecnico_instalacion/<int:id_i>/<int:id_emp>', methods=["DELETE"])
def deleteTechnicianInstallationById(id_i, id_emp):
    try:
        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Verificar si la relación Tecnico_Instalacion existe antes de intentar eliminarla
        cur.execute('SELECT * FROM Tecnico_Instalacion WHERE ID_I = %s AND ID_Emp = %s;', (id_i, id_emp))
        existing_relationship = cur.fetchall()

        if not existing_relationship:
            cur.close()
            conn.close()
            return jsonify({"error": f"No se ha encontrado una relación Tecnico_Instalacion con ID_I {id_i} e ID_Emp {id_emp}"}), 404

        # Eliminar la relación Tecnico_Instalacion de la base de datos
        cur.execute('DELETE FROM Tecnico_Instalacion WHERE ID_I = %s AND ID_Emp = %s;', (id_i, id_emp))
        conn.commit()

        cur.close()
        conn.close()

        return jsonify({"message": f"Relación Tecnico_Instalacion con ID_I {id_i} e ID_Emp {id_emp} eliminada exitosamente"})

    except Exception as err:
        return jsonify({"error": str(err)}), 500