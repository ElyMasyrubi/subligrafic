from flask import Blueprint, request, flash, jsonify
from database.db import get_connection
import psycopg2
from .Tablas.Tematica import Tematica

theme = Blueprint('theme_blueprint', __name__)


@theme.route('/')
def home():
    return 'Pagina de Tematica'




@theme.route('/registro', methods=['GET', 'POST'])
def registro():
    try:
        conexion = get_connection()
        with conexion.cursor() as cursor:
            requestjson = request.json
            if request.method == 'POST' and 'nombre' in requestjson:
                nombre = requestjson['nombre']
                #cursor.execute('SELECT * FROM pedidos WHERE id_usuario = %s', (id_usuario,))
                # cursor.fetchone()
                cursor.execute("INSERT INTO tematica (nombre) VALUES (%s)", (nombre,))
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



@theme.route('/alltheme')
def all_theme():
    try:
        conexion = get_connection()
        themes = []
        with conexion.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            sentencia = ("SELECT * FROM tematica")
            cursor.execute(sentencia)
            resultado=cursor.fetchall()
            for row in resultado:
                them = Tematica(row[0], row[1])
                themes.append(them.to_JSON())
            return jsonify(themes)
    except Exception as ex:
        raise Exception(ex)
    finally:
        conexion.close()


@theme.route('/themeid/<int:id>')
def id_theme(id):
    try:
        conexion = get_connection()
        themes = []
        with conexion.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute("SELECT id, nombre  FROM tematica WHERE id = %s", (id,))
            filas = cursor.fetchall()
            for row in filas:
                them = Tematica(row[0], row[1])
                themes.append(them.to_JSON())
            return jsonify(themes)
    except Exception as ex:
        raise Exception(ex)
    finally:
        conexion.close()



@theme.route('/delete/<int:id>', methods=['DELETE'])
def id_delete(id):
    try:
        conexion = get_connection()
        with conexion.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute("DELETE FROM tematica WHERE id = %s", (id,))
            filas = cursor.rowcount
            conexion.commit()
        return f'Elementos eliminados: {filas}'
    except Exception as ex:
        raise Exception(ex)
    finally:
        conexion.close()