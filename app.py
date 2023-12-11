
from flask import Flask, request, jsonify


from flask_sqlalchemy import SQLAlchemy

from flask_cors import CORS


app = Flask(__name__)


CORS(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://powerfulfitness:root1234@powerfulfitness.mysql.pythonanywhere-services.com/powerfulfitness$default'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)



class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    precio=db.Column(db.Integer)
    cantidad=db.Column(db.Integer)
    direccion=db.Column(db.String(400))

    def __init__(self,nombre,precio,cantidad,direccion):
        self.nombre=nombre
        self.precio=precio
        self.cantidad=cantidad
        self.direccion=direccion


with app.app_context():
    db.create_all()


@app.route("/")
def index():
    return f'App Web para registrar pedidos de Powerful Fitness'


@app.route("/registro", methods=['POST'])
def registro():
    nombre_recibido = request.json["nombre"]
    precio=request.json['precio']
    cantidad=request.json['cantidad']
    direccion=request.json['direccion']

    nuevo_registro = Pedido(nombre=nombre_recibido,precio=precio,cantidad=cantidad,direccion=direccion)
    db.session.add(nuevo_registro)
    db.session.commit()

    return "Solicitud de post recibida"



@app.route("/pedidos",  methods=['GET'])
def pedidos():

    all_registros = Pedido.query.all()

    data_serializada = []

    for objeto in all_registros:
        data_serializada.append({"id":objeto.id, "nombre":objeto.nombre, "precio":objeto.precio, "cantidad":objeto.cantidad, "direccion":objeto.direccion})

    return jsonify(data_serializada)


@app.route('/update/<id>', methods=['PUT'])
def update(id):

    pedido = Pedido.query.get(id)

    nombre = request.json["nombre"]
    precio=request.json['precio']
    cantidad=request.json['cantidad']
    direccion=request.json['direccion']

    pedido.nombre=nombre
    pedido.precio=precio
    pedido.cantidad=cantidad
    pedido.direccion=direccion
    db.session.commit()

    data_serializada = [{"id":pedido.id, "nombre":pedido.nombre, "precio":pedido.precio, "cantidad":pedido.cantidad, "direccion":pedido.direccion}]

    return jsonify(data_serializada)


@app.route('/borrar/<id>', methods=['DELETE'])
def borrar(id):


    pedido = Pedido.query.get(id)


    db.session.delete(pedido)
    db.session.commit()

    data_serializada = [{"id":pedido.id, "nombre":pedido.nombre, "precio":pedido.precio, "cantidad":pedido.cantidad, "direccion":pedido.direccion}]

    return jsonify(data_serializada)


if __name__ == "__main__":
    app.run(debug=True)

