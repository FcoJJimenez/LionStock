from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash
from models import *
import db


def init_db():
    print("Inicializando BBDD")
    db.Base.metadata.create_all(db.engine)


    # creamos el nuevo usuario enla BBDD de usuarios y en la de proveedores o clientes según el rol


#--------------------------------------------
    nuevo_usuario = User(None, username="cliente1", password=generate_password_hash("cliente1"), rol_id=2)
    datos_proveedor = Cliente(None, "cliente1 Nombre Completo", "11222333A",
                                "C/ Domicilio del cliente1", 14002, "Córdoba", "777111331", "cliente1@gmail.com", 7)
    db.session.add(nuevo_usuario)
    db.session.add(datos_proveedor)

    nuevo_usuario = User(None, username="cliente2", password=generate_password_hash("cliente2"), rol_id=2)
    datos_proveedor = Cliente(None, "cliente2 Nombre Completo", "22222333A",
                              "C/ Domicilio del cliente2", 14002, "Córdoba", "777111332", "cliente2@gmail.com", 8)

    db.session.add(nuevo_usuario)
    db.session.add(datos_proveedor)

    nuevo_usuario = User(None, username="cliente3", password=generate_password_hash("cliente3"), rol_id=2)
    datos_proveedor = Cliente(None, "cliente3 Nombre Completo", "33222333A",
                              "C/ Domicilio del cliente3", 14002, "Córdoba", "777111333", "cliente3@gmail.com", 9)
    db.session.add(nuevo_usuario)
    db.session.add(datos_proveedor)


    db.session.add(nuevo_usuario)
    db.session.add(datos_proveedor)


    db.session.commit()

    db.session.close()

if __name__ == "__main__":
    init_db()
