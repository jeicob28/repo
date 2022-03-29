
from enum import auto
from lib2to3.pgen2 import token
from logging import exception
import numbers
from socket import create_connection
from flask.views import MethodView
from itsdangerous import json
from validators import  CreateRegisterSchema
from flask import jsonify, request
from model import users
import bcrypt
import pymysql
import jwt
from config import KEY_TOKEN_AUTH
import datetime

#insertar datos en la de createRegister
create_register_schema = CreateRegisterSchema()


# Defino funcion para conectar a la db
def crear_conexion():
    try:
        conexion = pymysql.connect(host='localhost',user='root',passwd='12345',db="tallerevaluativo" )
        return conexion
    except pymysql.Error as error:
        print('Se ha producido un error al crear la conexión:', error),402

#  Creo clase para registrar usuario

class RegisterControllers(MethodView):
    
    def post(self):
        content = request.get_json() #!para parametros por json
        errors = create_register_schema.validate(content)
        if errors:
            return errors, 400
        correo = content.get("correo")
        password = content.get("password")
        nombres = content.get("nombres")
        apellidos = content.get("apellidos")
        print(correo,password,nombres,apellidos)
        salt = bcrypt.gensalt()
        hash_password = bcrypt.hashpw(bytes(str(password), encoding= 'utf-8'), salt)
        conexion=crear_conexion()
        print(conexion)
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT password,correo FROM registro_user WHERE correo=%s", (correo, ))
        auto=cursor.fetchone()
        if auto==None:
            cursor.execute(
                 "INSERT INTO registro_user(correo,nombres,apellidos,password) VALUES(%s,%s,%s,%s)", (correo,nombres,apellidos,hash_password,))
            conexion.commit()
            conexion.close()
            return ("bienvenido registro exitoso"),200
        else :
            conexion.close()
            return ("el usuario ya esta registrado"),400

# Creo Clase para realizar login del usuarion en la base de datos

class LoginControllers(MethodView):

    def post(self):
        #!content = request.args #!para parametros de consulta.
        content = request.get_json()
        password = bytes(str(content.get("password")), encoding= 'utf-8')
        correo = content.get("correo")
        print("--------",correo,content.get("password"), correo,password)

        conexion=crear_conexion()
        print("conexion a la bd",conexion)
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT password,correo,nombres FROM registro_user WHERE correo=%s", (correo, ))
        auto=cursor.fetchone()
        if auto==None:
            conexion.close()
            return ("el usuario no esta registrado")
        else:
            bytepwd=bytes(auto[0], encoding= 'utf-8') #!para comparar el password tomado del parametro de ruta con el de la bd.
            if bcrypt.checkpw(password, bytepwd):
                conexion.close()
                exp = datetime.datetime.utcnow() + datetime.timedelta(seconds=1500)#! se crea la variable exp para enviar al token.
                payload={'exp': exp, 'correo': correo, 'nombres': auto[2] }
                encoded_jwt = jwt.encode(payload, KEY_TOKEN_AUTH , algorithm='HS256')
                print(" El token es:------------",encoded_jwt)
                return ("bienvenido"+"\nhas iniciado sesion correctamente"+"\n"+"token:"+encoded_jwt),200
            else:
                conexion.close()
                return ("contraseña incorrecta"),400

# creo la clase para realizar consulra de todos los productos creados en la base de datos
class CrearProductoControllers(MethodView):

    def post(self):
        content = request.get_json()
        print(content)
        var_jwt=request.headers.get('Authorization')
        print("Auth: ", var_jwt)
        datosHeader= var_jwt.split(" ")
        if (len(datosHeader) <= 1):
            return jsonify({"Status": "Header de autorización no válido"}), 400
        print("datosHeader: ", datosHeader[1])
        print(datosHeader)
        jwt_token= (datosHeader[1])
        print("Este es el token: ",datosHeader[1])
        try:
            payload = jwt.decode(jwt_token,KEY_TOKEN_AUTH,algorithms='HS256')
        except:
            return jsonify({"Status": "Token no válido"}), 400
        print("este es el token ", payload)

        conexion=crear_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO productod(nombre,precio) VALUES(%s,%s)", (content.get("nombre"),content.get("precio"),))
        conexion.commit()
        conexion.close()
        auto1=cursor
        if auto1==None:
            return ("el producto ya esta registrado"),400
        else:
            return jsonify({"Status": "El producto se fue creeado Correctamente","token":jwt_token}), 200

class ProductosControllers(MethodView):

    def get(self):
        conexion = crear_conexion()
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM productod")
        auto=cursor.fetchall()
        print("Lista de producto",auto)
        conexion.close()
        return jsonify("Los datos son: ",auto),200