from flask import Blueprint, request, flash, jsonify
from database.db import get_connection
kind_of_product = Blueprint('kind_of_product_blueprint', __name__)
import psycopg2
from .Tablas.TiposDeProducto import TipoDeProducto

@kind_of_product.route('/')
def home():
    return 'Pagina de Tipo de producto'



@kind_of_product.route('/registro', methods=['GET', 'POST'])
def registro():
    try:
        conexion = get_connection()
        with conexion.cursor() as cursor:
            requestjson = request.json

            if request.method == 'POST' and 'nombre' in requestjson and 'tipos_del_productos' in requestjson:
                nombre = requestjson['nombre']
                tipos_del_productos = requestjson['tipos_del_productos']
                #cursor.execute('SELECT * FROM pedidos WHERE id_usuario = %s', (id_usuario,))
                # cursor.fetchone()
                cursor.execute("INSERT INTO tipo_de_producto (nombre, tipos_del_productos) VALUES (%s,%s)", (
                    nombre, tipos_del_productos))
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


@kind_of_product.route('/tpproduct')
def tipo_product():
    try:
        conexion = get_connection()
        tpro = []
        with conexion.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            sentencia = ("SELECT id,nombre,tipos_del_productos FROM tipo_de_producto ORDER BY id ASC")
            cursor.execute(sentencia)
            resultado=cursor.fetchall()
            for row in resultado:
                tipro = TipoDeProducto(row[0], row[1], row[2])
                tpro.append(tipro.to_JSON())
            return jsonify(tpro)
    except Exception as ex:
        raise Exception(ex)
    finally:
        conexion.close()


@kind_of_product.route('/productosid/<int:id>')
def tipo_producid(id):
    try:
        conexion = get_connection()
        tpro = []
        with conexion.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute("SELECT id, nombre, tipos_del_productos FROM tipo_de_producto WHERE id = %s", (id,))
            filas = cursor.fetchall()
            for row in filas:
                tipro = TipoDeProducto(row[0], row[1], row[2])
                tpro.append(tipro.to_JSON())
            return jsonify(tpro)
        
       
    except Exception as ex:
        raise Exception(ex)
    finally:
         conexion.close()


@kind_of_product.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    try:
        conexion = get_connection()
        with conexion.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute("DELETE FROM tipo_de_producto WHERE id = %s", (id,))
            filas = cursor.rowcount
            conexion.commit()
        conexion.close()
        return f'Elementos eliminados: {filas}'
    except Exception as ex:
        raise Exception(ex)