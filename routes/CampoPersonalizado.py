from flask import Blueprint, request, flash, jsonify
from database.db import get_connection
import psycopg2
from .Tablas.CampoPerzonalizado import CampoPerzonalizado
custom_field= Blueprint('custom_field_blueprint', __name__)


@custom_field.route('/')
def home():
    return 'Pagina de campo personalizado'



@custom_field.route('/registro', methods=['GET', 'POST'])
def registro():
    try:
        conexion = get_connection()
        with conexion.cursor() as cursor:
            requestjson = request.json
            if request.method == 'POST' and 'nombre' in requestjson and 'bolean' in requestjson:
                nombre = requestjson['nombre']
                bolean = requestjson['bolean']
                #cursor.execute('SELECT * FROM pedidos WHERE id_usuario = %s', (id_usuario,))
                # cursor.fetchone()
                cursor.execute("INSERT INTO campo_personalizado (nombre, bolean) VALUES (%s, %s)", (nombre, bolean,))
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


@custom_field.route('/allcustom')
def all_custom_field():
    try:
        conexion = get_connection()
        custom = []
        with conexion.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            sentencia = ("SELECT * FROM campo_personalizado")
            cursor.execute(sentencia)
            resultado=cursor.fetchall()
            for row in resultado:
                custo = CampoPerzonalizado(row[0], row[1], row[2])
                custom.append(custo.to_JSON())
            return jsonify(custom)
    except Exception as ex:
        raise Exception(ex)
    finally:
        conexion.close()


@custom_field.route('/idcustom/<int:id>')
def id_custom_field(id):
    try:
        conexion = get_connection()
        custom = []
        with conexion.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute("SELECT id, nombre, bolean FROM campo_personalizado WHERE id = %s", (id,))
            resultado = cursor.fetchall()
            for row in resultado:
                custo = CampoPerzonalizado(row[0], row[1], row[2])
                custom.append(custo.to_JSON())
            return jsonify(custom)
    except Exception as ex:
        raise Exception(ex)
    finally:
        conexion.close()




@custom_field.route('/delete/<int:id>', methods=['DELETE'])
def id_delete(id):
    try:
        conexion = get_connection()
        with conexion.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute("DELETE FROM campo_personalizado WHERE id = %s", (id,))
            filas = cursor.rowcount
            conexion.commit()
        conexion.close()
        return f'Elementos eliminados: {filas}'
    except Exception as ex:
        raise Exception(ex)