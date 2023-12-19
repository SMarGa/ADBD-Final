

from flask import Flask , request, jsonify

from employee import employee_bp 
from cell import cell_bp
from instalation import instalation_bp
from route import route_bp
from machine import machine_bp
from waste import waste_bp
from vehicle import vehicle_bp
from db import  get_db_connection


app = Flask(__name__)

# Rutas destinadas a los cargos superiores del CAT
app.register_blueprint(employee_bp, url_prefix='/empleado')
app.register_blueprint(cell_bp, url_prefix='/celda')
app.register_blueprint(instalation_bp, url_prefix='/instalacion')

# Rutas destinadas a empleados
app.register_blueprint(route_bp, url_prefix='/ruta')
app.register_blueprint(waste_bp, url_prefix='/residuo')
app.register_blueprint(machine_bp, url_prefix='/maquina')
app.register_blueprint(vehicle_bp, url_prefix='/vehiculos')

# Rutas destinadas al público 




@app.route('/', methods=['GET'])
def welcome():
  
    return jsonify("This is a api for the accesing data from the databases of the CAT!")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)