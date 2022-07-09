from flask import Blueprint, request, flash, session, redirect, url_for, jsonify
from database.db import get_connection 
from werkzeug.security import generate_password_hash, check_password_hash
import re
import psycopg2.extras
import psycopg2
from .Tablas.Usuario import Usuario


main = Blueprint('login_blueprint', __name__)

@main.route('/home')
def home():
    try:
        if 'loggedin' in session:
            return "Has iniciado Seccion"
        else:
            return "Intenta de nuevo"
    except Exception as e:
        print(f'Ocurrio un error {e}')


@main.route('/registro', methods=['GET', 'POST'])
def registro():
    try:
        conexion =  get_connection()
        with conexion.cursor() as cursor:
            requestjson = request.json

            if request.method == 'POST' and 'username' in requestjson and 'password' in requestjson and 'email' in requestjson:
                name = requestjson['name']
                lastname = requestjson['lastname']
                username = requestjson['username']
                password = requestjson['password']
                email = requestjson['email']
                phone = requestjson['phone']
                adress = requestjson['adress']
                favorito = requestjson['favorito']
                pedidos = requestjson['pedidos']
                _hashed_password = generate_password_hash(password)
                cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
                account = cursor.fetchone()
                if account:
                    flash('La Cuenta Ya Existe')
                elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                    flash('Invalid email address!')
                elif not re.match(r'[A-Za-z0-9]+', username):
                    flash('Username must contain only characters and numbers!')
                elif not username or not password or not email:
                    flash('Please fill out the form!')
                else:
                    cursor.execute("INSERT INTO users (name, lastname, username, password, email,phone,adress,favorito,pedidos) VALUES (%s,%s,%s,%s,%s,%s,%s,%s, %s)", (name,lastname, username, _hashed_password, email,phone,adress,favorito,pedidos))
                    conexion.commit()
                    print(conexion)
                    flash('You have successfully registered!')
                    return 'You have successfully registered!'
            elif request.method=='POST':
                flash('El formulario esta vacio')
            return 'Vuelve a Intentarlo'
    except Exception as ex:
        raise Exception(ex)
    finally:
        conexion.close()



@main.route('/login', methods=['GET', 'POST'])
def login():
    try:
        conexion = get_connection()
        with conexion.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            requesjon = request.json

            if request.method == 'POST' and 'username' in requesjon and 'password' in requesjon:
                username = requesjon['username']
                password = requesjon['password']
                cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
                account = cursor.fetchone()
                if account:
                    password_rs = account['password']
                    if check_password_hash(password_rs, password):
                        session['loggedin'] = True
                        session['id'] = account['id']
                        session['username'] = account['username']
                        return redirect(url_for('login_blueprint.home'))
                    else:
                        'Password Incorrecta'
                else:
                    'Password Incorrecta'
            return redirect(url_for('login_blueprint.home'))
    except Exception as ex:
        raise Exception(ex)
    finally:
        conexion.close()

@main.route('/logout')
def logout():
    try:
        if session != None:
            session.pop('loggedin', None)
            session.pop('id', None)
            session.pop('username', None)
        
            return redirect(url_for('login_blueprint.home'))
    except Exception as ex:
        raise Exception(ex)

@main.route('/user')
def get_user():
    try:
        conexion = get_connection()
        users = []
        with conexion.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            sentencia = "SELECT id, name, lastname, email,password,  phone, adress FROM users ORDER BY id ASC"
            cursor.execute(sentencia)
            resultado=cursor.fetchall()
            for row in resultado:
                print(row)
                user = Usuario(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
                users.append(user.to_JSON())
                
            #if cursor != None:
            #    return jsonify(resultado)
            return jsonify(users)
    except Exception as ex:
        raise Exception(ex)
    finally:
        conexion.close()
    
@main.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    try:
        conexion = get_connection()
        with conexion.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute("DELETE FROM users WHERE id = %s", (id,))
            filas = cursor.rowcount
            conexion.commit()
        conexion.close()

        return f'Elementos eliminados: {filas}'
    except Exception as ex:
        raise Exception(ex)

@main.route('/userid/<int:id>')
def userid(id):
    try:
        conexion = get_connection()
        filass = []
        with conexion.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute("SELECT id, name, lastname, username, email, phone ,adress FROM users  WHERE id = %s", (id,) )
            filas = cursor.fetchall()
            for row in filas:
                fila = Usuario(row[0],row[1], row[2], row[3], row[4], row[5], row[6])
                filass.append(fila.to_JSON())
                #return jsonify(filas)
                return jsonify(filass)
    except Exception as ex:
        raise Exception(ex)
    finally:
         conexion.close()

@main.route('/update/<int:id>', methods=['PUT'])
def update(id):
    try:
        conexion = get_connection()
        with conexion.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute("""UPDATE users SET fullname = %s, username = %s, email = %s
                                WHERE id = %s""", (fullname.fullname, username.username, email.email, id ))

                                #(name, lastname, username, password, email,phone,adress,favorito,pedidos) VALUES (%s,%s,%s,%s,%s,%s,%s,%s, %s)", (name,lastname, username, _hashed_password, email,phone,adress,favorito,pedidos)

            filas = cursor.rowcount
            conexion.commit()
        conexion.close()
        return jsonify(filas)
    except Exception as ex:
        raise Exception(ex)
        
#try:
          
#  except Exception as ex:
#  raise Exception(ex)