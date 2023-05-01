from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash
from models import *
import db


def init_db():
    print("Inicializando BBDD")
    db.Base.metadata.create_all(db.engine)


    hash_password = generate_password_hash("ADMIN")

    # creamos el nuevo usuario enla BBDD de usuarios y en la de proveedores o clientes según el rol

    rol_administrador = Rol(1, "ADMINISTRADOR")
    rol_cliente = Rol(2, "CLIENTE")
    rol_proveedor = Rol(3, "PROVEEDOR")
    db.session.add(rol_administrador)
    db.session.add(rol_cliente)
    db.session.add(rol_proveedor)

    nuevo_usuario = User(None, username="ADMIN",
                         password=hash_password,
                         rol_id=1)

    db.session.add(nuevo_usuario)
    db.session.commit()


    db.session.close()
    print("TIPOS DE USUARIOS CREADOS")
    print("USUARIO ADMINISTRADOR CREADO")
    print("USUARIO: ADMIN")
    print("PASSWORD: ADMIN")
if __name__ == "__main__":
    init_db()
