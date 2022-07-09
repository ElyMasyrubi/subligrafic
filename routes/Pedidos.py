from flask import Blueprint, jsonify, request, flash
from database.db import get_connection
import psycopg2
import re
import psycopg2.extras
import psycopg2
from .Tablas.Pedidos import Pedidos

orders = Blueprint('orders_blueprint', __name__)


@orders.route('/pedidos')
def orders_get():
    try:
        conexion = get_connection()
        pedis = []
        with conexion.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            sentencia = ("SELECT id, id_usuario, fecha, productos , detalledepago, estado FROM pedidos ORDER BY id ASC")
            cursor.execute(sentencia)
            resultado = cursor.fetchall()
            for row in resultado:
                pedi = Pedidos(row[0], row[1], row[2], row[3], row[4], row[5])
                pedis.append(pedi.to_JSON())

            return jsonify(pedis)
        
    except Exception as ex:
        raise Exception(ex)
    finally:
        conexion.close()


@orders.route('/registro', methods=['GET', 'POST'])
def registro():
    try:
        conexion = get_connection()
        with conexion.cursor() as cursor:
            requestjson = request.json

            if request.method == 'POST' and 'id_usuario' in requestjson and 'fecha' in requestjson and 'productos' in requestjson:
                id_usuario = requestjson['id_usuario']
                fecha = requestjson['fecha']
                productos = requestjson['productos']
                precioTotal = requestjson['precioTotal']
                detalledepago = requestjson['detalledepago']
                estado = requestjson['estado']
                #cursor.execute('SELECT * FROM pedidos WHERE id_usuario = %s', (id_usuario,))
                # cursor.fetchone()
                cursor.execute("INSERT INTO pedidos (id_usuario, fecha, productos,precioTotal, detalledepago,estado) VALUES (%s,%s,%s,%s,%s,%s)", (
                    id_usuario, fecha, productos,precioTotal, detalledepago, estado))
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


@orders.route('/pedidosid/<int:id>')
def productoid(id):
    try:
        conexion = get_connection()
        pedis = []
        with conexion.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute(
                "SELECT id, id_usuario, fecha, productos, detalledepago, estado FROM pedidos WHERE id = %s", (id,))
            filas = cursor.fetchall()
            for row in filas:
                pedi = Pedidos(row[0], row[1], row[2], row[3], row[4], row[5])
                pedis.append(pedi.to_JSON())
            return jsonify(pedis)
   
        return jsonify(filas)
    except Exception as ex:
        raise Exception(ex)
    finally:
        conexion.close()


#Ver los pedidos de un usuario
@orders.route('/userid')
def userid():
    try:
        conexion = get_connection()
        pedis = []
        with conexion.cursor() as cursor:
            requestjson = request.json
            if request.method == 'GET' and 'id_usuario' in requestjson:
                id_usuario = requestjson['id_usuario']
                cursor.execute('SELECT * FROM pedidos WHERE id_usuario = %s', (id_usuario,))
                filas = cursor.fetchall()
                for row in filas:
                    pedi = Pedidos(row[0], row[1], row[2], row[3], row[4], row[5])
                    pedis.append(pedi.to_JSON())
                return jsonify(pedis)
    except Exception as ex:
        raise Exception(ex)
    finally:
        conexion.close()

@orders.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    try:
        conexion = get_connection()
        with conexion.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute("DELETE FROM pedidos WHERE id = %s", (id,))
            filas = cursor.rowcount
            conexion.commit()
        conexion.close()
        return f'Elementos eliminados: {filas}'
    except Exception as ex:
        raise Exception(ex)



# Ver el Estado de un Pedido
@orders.route('/peidos')
def campo():
    try:
        conexion = get_connection()
        pedis = []
        with conexion.cursor() as cursor:
            requestjson = request.json
            if request.method == 'GET' and 'estado' in requestjson:
                estado = requestjson['estado']
                cursor.execute('SELECT * FROM pedidos WHERE estado = %s', (estado,))
                filas = cursor.fetchall()
                for row in filas:
                    pedi = Pedidos(row[0], row[1], row[2], row[3], row[4], row[5])
                    pedis.append(pedi.to_JSON())
                return jsonify(pedis)
        
    except Exception as ex:
        raise Exception(ex)
    finally:
        conexion.close()
