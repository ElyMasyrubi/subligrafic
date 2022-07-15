from flask import Flask
from routes import Login, Producto, Pedidos, TipoDeProducto, Tematica, TipoDeTrabajo, CampoPersonalizado, DetallesDePago, Estado
from config import config





app=Flask(__name__)

app.secret_key = 'Password0101'

@app.route('/')
def index():
    return "Pagina de inicio"


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_blueprint(Login.main, url_prefix='/api/login')
    app.register_blueprint(Producto.prod, url_prefix='/api/producto')
    app.register_blueprint(Pedidos.orders, url_prefix='/api/orders')
    app.register_blueprint(TipoDeProducto.kind_of_product, url_prefix='/api/kind_of_product')
    app.register_blueprint(Tematica.theme, url_prefix='/api/theme')
    app.register_blueprint(TipoDeTrabajo.type_of_job, url_prefix='/api/type_of_job')
    app.register_blueprint(CampoPersonalizado.custom_field, url_prefix='/api/custom_field')
    app.register_blueprint(DetallesDePago.payment_details, url_prefix='/api/payment_details')
    app.register_blueprint(Estado.condition, url_prefix='/api/condition')
    app.run()