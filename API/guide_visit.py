from flask import Blueprint,jsonify , request

from db import  get_db_connection

guide_visit_bp = Blueprint('guide_visit', __name__)

@guide_visit_bp.route('/', methods=["GET"])
def getGuideVisit():
    try:
        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Obtener Guia_Visita 
        cur.execute('SELECT * FROM Guia_Visita ;')
        data = cur.fetchall()
        cur.close()
        conn.close()

        if not data:
            return jsonify({"error": f"No se ha encontrado una relación Guia_Visita "}), 404

        return jsonify(data)

    except Exception as err:
        return jsonify({"error": str(err)}), 500

@guide_visit_bp.route('/inst/<int:id_i>', methods=["GET"])
def getGuideVisitByInst(id_i):
    try:
        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Obtener Guia_Visita por ID_I
        cur.execute('SELECT * FROM Guia_Visita WHERE ID_I = %s;', (id_i,))
        data = cur.fetchall()
        cur.close()
        conn.close()

        if not data:
            return jsonify({"error": f"No se ha encontrado una relación Guia_Visita con ID_I {id_i}"}), 404

        return jsonify(data)

    except Exception as err:
        return jsonify({"error": str(err)}), 500

@guide_visit_bp.route('/visit/<int:id_visit>', methods=["GET"])
def getGuideVisiByVisit(id_visit):
    try:
        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Obtener Guia_Visita por ID_Visit
        cur.execute('SELECT * FROM Guia_Visita WHERE ID_Visit = %s;', (id_visit,))
        data = cur.fetchall()
        cur.close()
        conn.close()

        if not data:
            return jsonify({"error": f"No se ha encontrado una relación Guia_Visita con ID_Visit {id_visit}"}), 404

        return jsonify(data)

    except Exception as err:
        return jsonify({"error": str(err)}), 500

@guide_visit_bp.route('/guia/<int:id_emp>', methods=["GET"])
def getGuideVisitByEmp( id_emp ):
    try:
        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Obtener Guia_Visita por ID_Emp 
        cur.execute('SELECT * FROM Guia_Visita WHERE ID_Emp = %s;', (id_emp,))
        data = cur.fetchall()
        cur.close()
        conn.close()

        if not data:
            return jsonify({"error": f"No se ha encontrado una relación Guia_Visita con ID_Emp {id_emp}"}), 404

        return jsonify(data)

    except Exception as err:
        return jsonify({"error": str(err)}), 500

@guide_visit_bp.route('/', methods=["POST"])
def createGuideVisit():
    try:
        # Obtener datos del cuerpo de la solicitud
        data = request.get_json()

        # Validar que se proporcionaron todos los campos necesarios
        if "ID_Visit" not in data or "ID_Emp" not in data or "ID_I" not in data:
            return jsonify({"error": "ID_Visit, ID_Emp e ID_I son campos requeridos"}), 400

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

        # Verificar si el guía existe
        cur.execute('SELECT * FROM Guia WHERE ID_Emp = %s;', (data["ID_Emp"],))
        existing_guide = cur.fetchone()

        if not existing_guide:
            cur.close()
            conn.close()
            return jsonify({"error": f"No se ha encontrado un guía con ID_Emp {data['ID_Emp']}"}), 404

        # Verificar si la instalación existe
        cur.execute('SELECT * FROM Instalacion WHERE ID_I = %s;', (data["ID_I"],))
        existing_installation = cur.fetchone()

        if not existing_installation:
            cur.close()
            conn.close()
            return jsonify({"error": f"No se ha encontrado una instalación con ID_I {data['ID_I']}"}), 404

        # Insertar nueva relación Guia_Visita en la base de datos
        cur.execute('INSERT INTO Guia_Visita (ID_Visit, ID_Emp, ID_I) VALUES (%s, %s, %s);',
                    (data["ID_Visit"], data["ID_Emp"], data["ID_I"]))
        conn.commit()

        cur.close()
        conn.close()

        return jsonify({"message": "Relación Guia_Visita creada exitosamente"}), 201

    except Exception as err:
        return jsonify({"error": str(err)}), 500
    

@guide_visit_bp.route('/<int:id_visit>/<int:id_emp>/<int:id_i>', methods=["PATCH"])
def updateGuideVisit(id_visit, id_emp, id_i):
    try:
        # Obtener datos del cuerpo de la solicitud
        data = request.get_json()

        # Validar que se proporcionaron datos para actualizar
        if not data:
            return jsonify({"error": "No se proporcionaron datos para actualizar"}), 400

        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Verificar si la relación Guia_Visita existe antes de intentar actualizarla
        cur.execute('SELECT * FROM Guia_Visita WHERE ID_Visit = %s AND ID_Emp = %s AND ID_I = %s;', (id_visit, id_emp, id_i))
        existing_relationship = cur.fetchall()

        if not existing_relationship:
            cur.close()
            conn.close()
            return jsonify({"error": f"No se ha encontrado una relación Guia_Visita con ID_Visit {id_visit}, ID_Emp {id_emp} e ID_I {id_i}"}), 404

        # Verificar si la visita existe
        if "ID_Visit" in data:
            cur.execute('SELECT * FROM Visita WHERE ID_Visit = %s;', (data["ID_Visit"],))
            existing_visit = cur.fetchone()

            if not existing_visit:
                cur.close()
                conn.close()
                return jsonify({"error": f"No se ha encontrado una visita con ID_Visit {data['ID_Visit']}"}), 404

        # Verificar si el guía existe
        if "ID_Emp" in data:
            cur.execute('SELECT * FROM Guia WHERE ID_Emp = %s;', (data["ID_Emp"],))
            existing_guide = cur.fetchone()

            if not existing_guide:
                cur.close()
                conn.close()
                return jsonify({"error": f"No se ha encontrado un guía con ID_Emp {data['ID_Emp']}"}), 404

        # Verificar si la instalación existe
        if "ID_I" in data:
            cur.execute('SELECT * FROM Instalacion WHERE ID_I = %s;', (data["ID_I"],))
            existing_installation = cur.fetchone()

            if not existing_installation:
                cur.close()
                conn.close()
                return jsonify({"error": f"No se ha encontrado una instalación con ID_I {data['ID_I']}"}), 404

        # Construir la consulta de actualización
        update_query = 'UPDATE Guia_Visita SET '
        values = []

        for key, value in data.items():
            update_query += f'{key} = %s, '
            values.append(value)

        # Eliminar la coma extra al final y agregar la condición WHERE
        update_query = update_query.rstrip(', ') + f' WHERE ID_Visit = %s AND ID_Emp = %s AND ID_I = %s;'
        values.extend([id_visit, id_emp, id_i])

        # Ejecutar la consulta de actualización
        cur.execute(update_query, tuple(values))
        conn.commit()

        cur.close()
        conn.close()

        return jsonify({"message": f"Relación Guia_Visita con ID_Visit {id_visit}, ID_Emp {id_emp} e ID_I {id_i} actualizada exitosamente"})

    except Exception as err:
        return jsonify({"error": str(err)}), 500
    

@guide_visit_bp.route('/<int:id_visit>/<int:id_emp>/<int:id_i>', methods=["DELETE"])
def deleteGuideVisit(id_visit, id_emp, id_i):
    try:
        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Verificar si la relación Guia_Visita existe antes de intentar eliminarla
        cur.execute('SELECT * FROM Guia_Visita WHERE ID_Visit = %s AND ID_Emp = %s AND ID_I = %s;', (id_visit, id_emp, id_i))
        existing_relationship = cur.fetchall()

        if not existing_relationship:
            cur.close()
            conn.close()
            return jsonify({"error": f"No se ha encontrado una relación Guia_Visita con ID_Visit {id_visit}, ID_Emp {id_emp} e ID_I {id_i}"}), 404

        # Eliminar la relación Guia_Visita de la base de datos
        cur.execute('DELETE FROM Guia_Visita WHERE ID_Visit = %s AND ID_Emp = %s AND ID_I = %s;', (id_visit, id_emp, id_i))
        conn.commit()

        cur.close()
        conn.close()

        return jsonify({"message": f"Relación Guia_Visita con ID_Visit {id_visit}, ID_Emp {id_emp} e ID_I {id_i} eliminada exitosamente"})

    except Exception as err:
        return jsonify({"error": str(err)}), 500