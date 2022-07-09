from flask import Blueprint, request, flash, jsonify
from database.db import get_connection
import psycopg2

from .Tablas.Estado import Estado

condition = Blueprint('condition_blueprint', __name__)


@condition.route('/')
def home():
    return 'Pagina de Estado'


@condition.route('/registro', methods=['GET', 'POST'])
def registro():
    try:
        conexion = get_connection()
        with conexion.cursor() as cursor:
            requestjson = request.json
            if request.method == 'POST' and 'nombre' in requestjson:
                nombre = requestjson['nombre']
                #cursor.execute('SELECT * FROM pedidos WHERE id_usuario = %s', (id_usuario,))
                # cursor.fetchone()
                cursor.execute("INSERT INTO estado (nombre) VALUES (%s)", (nombre,))
                conexion.commit()
                flash('You have successfully registered!')
                return 'You have successfully registered!'
            elif request.method == 'POST':
                flash('El formulario esta vacio')
            return 'Vuelve a Intentarlo'
    except Exception as ex:
        raise Exception(ex)
    finally:
        conexion.close()

@condition.route('/allcondition')
def all_condition():
    try:
        conexion = get_connection()
        conditio = []
        with conexion.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            sentencia = ("SELECT * FROM estado")
            cursor.execute(sentencia)
            resultado = cursor.fetchall()
            for row in resultado:
                conditi = Estado(row[0], row[1])
                conditio.append(conditi.to_JSON())
            return jsonify(conditio)
            
    except Exception as ex:
        raise Exception(ex)
    finally:
        conexion.close()

@condition.route('/idcondition/<int:id>')
def id_condition(id):
    try:
        conexion = get_connection()
        conditio = []
        with conexion.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute("SELECT id, nombre FROM estado WHERE id = %s", (id,))
            resultado = cursor.fetchall()
            for row in resultado:
                conditi = Estado(row[0], row[1])
                conditio.append(conditi.to_JSON())
            return jsonify(conditio)
    except Exception as ex:
        raise Exception(ex)
    finally:
        conexion.close()



@condition.route('/delete/<int:id>', methods=['DELETE'])
def id_delete(id):
    try:
        conexion = get_connection()
        with conexion.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute("DELETE FROM estado WHERE id = %s", (id,))
            filas = cursor.rowcount
            conexion.commit()
        conexion.close()
        return f'Elementos eliminados: {filas}'
    except Exception as ex:
        raise Exception(ex)