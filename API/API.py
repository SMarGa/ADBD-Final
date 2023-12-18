

from flask import Flask , request, jsonify

from employee import employee_bp 
from cell import cell_bp
from instalation import instalation_bp
from route import route_bp
from db import  get_db_connection


app = Flask(__name__)
app.register_blueprint(employee_bp, url_prefix='/empleado')
app.register_blueprint(cell_bp, url_prefix='/celda')
app.register_blueprint(instalation_bp, url_prefix='/instalacion')

app.register_blueprint(route_bp, url_prefix='/ruta')

@app.route('/', methods=['GET'])
def welcome():
  
    return jsonify("This is a api for the accesing data from the databases of the CAT!")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)