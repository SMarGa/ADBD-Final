from flask import Blueprint,jsonify
from API import  get_db_connection

employee_bp = Blueprint('employee', __name__)

@employee_bp.route('/tecnico/<int:ID_Emp>', methods = ["Get"])
def getById(id):
    try:
        # Estableciendo conección con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()
        # Obetener técnicos por nombre
        cur.execute('SELECT * FROM Tecnico WHERE ID_Emp = %s;',(id,))
        
    except Exception as err:
        return jsonify({"error" : str(err)}), 500 
