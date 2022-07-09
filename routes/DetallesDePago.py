from flask import Blueprint

payment_details = Blueprint('payment_details_field_blueprint', __name__)


@payment_details.route('/')
def home():
    return 'Pagina de Detalles de pago'
