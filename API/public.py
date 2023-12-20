from flask import Blueprint,jsonify , request

from db import  get_db_connection

public_bp = Blueprint('public', __name__)


@public_bp.route('/visitas', methods=["GET"])
def getGuides():
    try:
        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Obtener visita por ID
        cur.execute('SELECT * FROM Visita;')
        data = cur.fetchall()
        cur.close()
        conn.close()

        if not data:
            return jsonify({"error": f"No se ha encontrado ningnuna visita"}), 404

        return jsonify(data)

    except Exception as err:
        return jsonify({"error": str(err)}), 500

@public_bp.route('/residuos', methods=["GET"])
def getWaste():
    try:
        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Obtener visita por ID
        cur.execute('SELECT (Tipo,Cantidad,Origen,Fecha_de_recepcion) FROM Residuo;')
        data = cur.fetchall()
        cur.close()
        conn.close()

        if not data:
            return jsonify({"error": f"No se ha encontrado ningnuna visita"}), 404

        return jsonify(data)

    except Exception as err:
        return jsonify({"error": str(err)}), 500