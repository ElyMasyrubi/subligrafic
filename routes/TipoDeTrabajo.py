from flask import Blueprint, request, flash, jsonify
from database.db import get_connection
import psycopg2

from .Tablas.TipoDeTrabajo import TipoDeTrabajo

type_of_job = Blueprint('type_of_job_blueprint', __name__)


@type_of_job.route('/')
def home():
    return 'Pagina de Tipo de trabajo'


@type_of_job.route('/registro', methods=['GET', 'POST'])
def registro():
    try:
        conexion = get_connection()
        with conexion.cursor() as cursor:
            requestjson = request.json
            if request.method == 'POST' and 'nombre' in requestjson:
                nombre = requestjson['nombre']
                #cursor.execute('SELECT * FROM pedidos WHERE id_usuario = %s', (id_usuario,))
                # cursor.fetchone()
                cursor.execute("INSERT INTO tipo_de_trabajo (nombre) VALUES (%s)", (nombre,))
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


@type_of_job.route('/alltype')
def alltype_of_job():
    try:
        conexion = get_connection()
        alltypes = []
        with conexion.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            sentencia = ("SELECT * FROM tipo_de_trabajo")
            cursor.execute(sentencia)
            resultado=cursor.fetchall()
            for row in resultado:
                alltype = TipoDeTrabajo(row[0], row[1])
                alltypes.append(alltype.to_JSON())
            return jsonify(alltypes)
    except Exception as ex:
        raise Exception(ex)
    finally:
        conexion.close()

@type_of_job.route('/idtype/<int:id>')
def id_type_of_job(id):
    try:
        conexion = get_connection()
        alltypes = []
        with conexion.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute("SELECT id, nombre FROM tipo_de_trabajo WHERE id = %s", (id,))
            resultado = cursor.fetchall()
            for row in resultado:
                alltype = TipoDeTrabajo(row[0], row[1])
                alltypes.append(alltype.to_JSON())
            return jsonify(alltypes)
        
    except Exception as ex:
        raise Exception(ex)
    finally:
        conexion.close()


@type_of_job.route('/delete/<int:id>', methods=['DELETE'])
def id_delete(id):
    try:
        conexion = get_connection()
        with conexion.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute("DELETE FROM tipo_de_trabajo WHERE id = %s", (id,))
            filas = cursor.rowcount
            conexion.commit()
        conexion.close()
        return f'Elementos eliminados: {filas}'
    except Exception as ex:
        raise Exception(ex)
