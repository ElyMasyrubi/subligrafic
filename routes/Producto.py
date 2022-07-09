from flask import Blueprint, request, flash, jsonify
from database.db import get_connection

import psycopg2
from .Tablas.Producto import Producto


prod = Blueprint('prud_blueprint', __name__)


@prod.route('/')
def homeproducto():
    return 'home desde Producto'


@prod.route('/registro', methods=['GET', 'POST'])
def registro():
    try:
        conexion = get_connection()
        with conexion.cursor() as cursor:
            requestjson = request.json

            if request.method == 'POST' and 'code' in requestjson and 'title' in requestjson and 'description' in requestjson:
                code = requestjson['code']
                title = requestjson['title']
                description = requestjson['description']
                price = requestjson['price']
                porcentajedeOferta = requestjson['porcentajedeOferta']
                Mainimage = requestjson['Mainimage']
                Tipodeproducto = requestjson['Tipodeproducto']
                Tematica = requestjson['Tematica']
                Esdestacado = requestjson['Esdestacado']
                Tipodetrabajo = requestjson['Tipodetrabajo']
                Campopersonalizado = requestjson['Campopersonalizado']

                cursor.execute(
                    'SELECT * FROM producto WHERE code = %s', (code,))
                account = cursor.fetchone()
                if account:
                    flash('La Cuenta Ya Existe')

                else:
                    cursor.execute("INSERT INTO producto (code, title, description, price,porcentajedeOferta,Mainimage,Tipodeproducto,Tematica,Esdestacado,Tipodetrabajo,Campopersonalizado) VALUES (%s,%s,%s,%s,%s,%s,%s, %s,%s,%s,%s)", (
                        code, title, description, price, porcentajedeOferta, Mainimage, Tipodeproducto, Tematica, Esdestacado, Tipodetrabajo, Campopersonalizado))
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


@prod.route('/productos')
def get_productos():
    try:
        conexion = get_connection()
        produs = []
        with conexion.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            sentencia = "SELECT id, code, title, description, price, porcentajedeoferta, mainimage, tipodeproducto, tematica, esdestacado, tipodetrabajo, campopersonalizado FROM producto ORDER BY id ASC"
            cursor.execute(sentencia)
            resultado = cursor.fetchall()
            for row in resultado:
                produ = Producto(row[0], row[1], row[2], row[3], row[4],
                                 row[5], row[6], row[7], row[8], row[9], row[10], row[11])
                produs.append(produ.to_JSON())

            return jsonify(produs)
    except Exception as ex:
        raise Exception(ex)
    finally:
        conexion.close()


@prod.route('/productosid/<int:id>')
def productoid(id):
    try:
        conexion = get_connection()
        produs = []
        with conexion.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute("SELECT code, title, description, price, porcentajedeOferta, Mainimage ,Tipodeproducto ,Tematica , Esdestacado,Tipodetrabajo, Campopersonalizado FROM producto WHERE id = %s", (id,))
            filas = cursor.fetchall()
            for row in filas:
                produ = Producto(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10])
                produs.append(produ.to_JSON())
                return jsonify(produs)
    except Exception as ex:
        raise Exception(ex)
    finally:
        conexion.close()


@prod.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    try:
        conexion = get_connection()
        with conexion.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute("DELETE FROM producto WHERE id = %s", (id,))
            filas = cursor.rowcount
            conexion.commit()
        conexion.close()
        return f'Elementos eliminados: {filas}'
    except Exception as ex:
        raise Exception(ex)
    finally:
        conexion.close()

# Ver un tipo_de_producto de productos
@prod.route('/tipnombr')
def tipnombr():
    try:
        conexion = get_connection()
        produc = []
        with conexion.cursor() as cursor:
            requestjson = request.json
            if request.method == 'GET' and 'tipodeproducto' in requestjson:
                tipodeproducto = requestjson['tipodeproducto']
                cursor.execute('SELECT * FROM producto WHERE tipodeproducto = %s', (tipodeproducto,))
                filas = cursor.fetchall()
                for row in filas:
                    pedi = Producto(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10])
                    produc.append(pedi.to_JSON())
                return jsonify(produc)
    except Exception as ex:
        raise Exception(ex)
    finally:
        conexion.close()


# Ver una tematica desde los productos
@prod.route('/titema')
def titemas():
    try:
        conexion = get_connection()
        produc = []
        with conexion.cursor() as cursor:
            requestjson = request.json
            if request.method == 'GET' and 'nombre' in requestjson:
                titemaa = requestjson['nombre']
                cursor.execute('SELECT * FROM producto WHERE tematica = %s', (titemaa,))
                filas = cursor.fetchall()
                for row in filas:
                    pedi = Producto(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10])
                    produc.append(pedi.to_JSON())
                return jsonify(produc)
                
    except Exception as ex:
        raise Exception(ex)
    finally:
        conexion.close()


# Ver un tipo_de_trabajo desde los productos
@prod.route('/tipotra')
def tipotra():
    try:
        conexion = get_connection()
        produc = []
        with conexion.cursor() as cursor:
            requestjson = request.json
            if request.method == 'GET' and 'tipodetrabajo' in requestjson:
                tipot = requestjson['tipodetrabajo']
                cursor.execute('SELECT * FROM producto WHERE tipodetrabajo = %s', (tipot,))
                filas = cursor.fetchall()
                for row in filas:
                    pedi = Producto(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10])
                    produc.append(pedi.to_JSON())
                return jsonify(produc)
        
    except Exception as ex:
        raise Exception(ex)
    finally:
        conexion.close()


# Ver un Campo_perzonalixado de productos
@prod.route('/campo')
def campo():
    try:
        conexion = get_connection()
        produc = []
        with conexion.cursor() as cursor:
            requestjson = request.json
            if request.method == 'GET' and 'campopersonalizado' in requestjson:
                campopersonalizado = requestjson['campopersonalizado']
                cursor.execute('SELECT * FROM producto WHERE campopersonalizado = %s', (campopersonalizado,))
                filas = cursor.fetchall()
                for row in filas:
                    pedi = Producto(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10])
                    produc.append(pedi.to_JSON())
                return jsonify(produc)
    except Exception as ex:
        raise Exception(ex)
    finally:
        conexion.close()

