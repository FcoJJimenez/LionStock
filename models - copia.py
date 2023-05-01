from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
import db


# definicion de la clase Roles
class Rol(db.Base):
    __tablename__ = 'rol'
    __table_args__ = {'sqlite_autoincrement': True}
    id_rol = Column(Integer, primary_key=True)
    descripcion = Column(String(50), unique=True)

    def __init__(self, id_rol, descripcion):
        self.id_rol = id_rol
        self.descripcion = descripcion

    def __str__(self):
        return "Rol: -->{} -->{} ".format(self.id_rol, self.descripcion)

    @classmethod
    def get_rol(self, id):
        try:
            resultado = db.session.query(Rol).filter_by(id_rol=id).first()
            print("Consulta de ID", resultado)
            if resultado != None:
                return resultado.descripcion
            else:
                return None
        except Exception as ex:
            raise Exception(ex)


# definicion de la clase usuarios
class User(db.Base, UserMixin):
    __tablename__ = 'users'
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True)
    username = Column(String(25), nullable=False, unique=True, index=True)
    password = Column(String(102), nullable=False)
    rol_id = Column(Integer, ForeignKey("rol.id_rol"))
    nomRolUser = relationship("Rol")
    def __init__(self, id, username, password, rol_id):
        self.id = id
        self.username = username
        self.password = password
        self.rol_id = rol_id

    def __str__(self):


        return "User: {}-->{} -->{} -->{} \n {}".format(self.id,
                                                    self.username,
                                                    self.password,
                                                    self.rol_id,
                                                        self.nomRolUser)


    @classmethod
    def login(self, db, user):


        # query=db.session.query(User).filter_by(username=user.username).first()
        # print("QUery montada:\n",query)

        try:
            resultado = db.session.query(User).filter_by(username=user.username).first()


            if resultado != None:
                # validamos hash para comprobar la password
                check = check_password_hash(resultado.password, user.password)
                usuario = User(resultado.id, resultado.username, check, resultado.rol_id)

                return usuario
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_by_id(self, db, id):
        print("entro en GET BY ID", id)

        try:
            query = db.session.query(User).filter_by(id=id).first()
            # cursor = db.connection.cursor()
            # sql = "SELECT id, username FROM user WHERE id='{}'".format(user.id)
            print("******************************************", query)

            if query != None:

                usuario = User(query.id, query.username, query.password, query.rol_id)
                return usuario
            else:
                return None
        except Exception as ex:
            raise Exception(ex)


# definicion de la clase cliente
class Cliente(db.Base):
    __tablename__ = 'cliente'
    __table_args__ = {'sqlite_autoincrement': True}
    id_cliente = Column(Integer, primary_key=True)
    nombreClie = Column(String(150))
    cifClie = Column(String(10))
    direcClie = Column(String(150))
    cpClie = Column(Integer())
    locClie = Column(String(150))
    tfnoClie = Column(String(20))
    emailClie = Column(String(100))
    userIdClie = Column(Integer, ForeignKey("users.id"))
    nomUsuClie = relationship("User")

    def __init__(self, id_cliente, nombreClie, cifClie, direcClie, cpClie, locClie, tfnoClie, emailClie, userIdClie):
        self.id_cliente = id_cliente
        self.nombreClie = nombreClie
        self.cifClie = cifClie
        self.direcClie = direcClie
        self.cpClie = cpClie
        self.locClie = locClie
        self.tfnoClie = tfnoClie
        self.emailClie = emailClie
        self.userIdClie = userIdClie

    def __str__(self):
        return "Cliente: {} -->{} -->{} -->{} -->{} -->{} -->{} -->{} -->{} \n {}".\
                format(self.id_cliente,
                       self.nombreClie,
                       self.cifClie,
                       self.direcClie,
                       self.cpClie,
                       self.locClie,
                       self.tfnoClie,
                       self.emailClie,
                       self.userIdClie,
                       self.nomUsuClie)


# definicion de la clase Proveedor
class Proveedor(db.Base):
    __tablename__ = 'proveedor'
    __table_args__ = {'sqlite_autoincrement': True}
    id_proveedor = Column(Integer, primary_key=True)
    nombreProv = Column(String(150))
    cifProv = Column(String(10))
    direcProv = Column(String(150))
    cpProv = Column(Integer())
    locProv = Column(String(150))
    emailProv = Column(String(100))
    tfnoProv = Column(String(20))
    userIdProv = Column(Integer, ForeignKey("users.id"))

    def __init__(self, id_proveedor, nombreProv, cifProv, direcProv, cpProv, locProv, emailProv, tfnoProv, userIdProv):
        self.id_proveedor = id_proveedor
        self.nombreProv = nombreProv
        self.cifProv = cifProv
        self.direcProv = direcProv
        self.cpProv = cpProv
        self.locProv = locProv
        self.emailProv = emailProv
        self.tfnoProv = tfnoProv
        self.userIdProv = userIdProv

    def __str__(self):
        return "Proveedor: -->{} -->{}-->{} -->{}-->{} -->{}-->{} -->{}-->{}".format(self.id_proveedor,
                                                                                     self.nombreProv,
                                                                                     self.cifProv,
                                                                                     self.direcProv,
                                                                                     self.cpProv,
                                                                                     self.locProv,
                                                                                     self.emailProv,
                                                                                     self.tfnoProv,
                                                                                     self.userIdProv)


# Definicion de la clase Categoria
class Categoria(db.Base):
    __tablename__ = 'categoria'
    __table_args__ = {'sqlite_autoincrement': True}
    id_categoria = Column(Integer, primary_key=True)
    nombreCate = Column(String(50), nullable=False)

    def __init__(self, id_categoria, nombreCate):
        self.id_categoria = id_categoria
        self.nombreCate = nombreCate

    def __str__(self):
        return "Categoria: -->{} -->{}".format(self.id_categoria,
                                               self.nombreCate)


# Definicion de la clase Producto
class Producto(db.Base):
    __tablename__ = 'producto'
    __table_args__ = {'sqlite_autoincrement': True}
    id_producto = Column(Integer, primary_key=True)
    nombreProd = Column(String(50), nullable=False)
    descProd = Column(String(250), nullable=False)
    pVentaProd = Column(Float, nullable=False)
    pCompraProd = Column(Float, nullable=False)
    stockProd = Column(Integer(), default=0)
    sMaxProd = Column(Integer(), default=0)
    ubicaProd = Column(String(20))
    provIdProd = Column(Integer, ForeignKey("proveedor.id_proveedor"))
    cateIdProd = Column(Integer, ForeignKey("categoria.id_categoria"))
    imgProd = Column(String(30), nullable=True)
    nomProvProd = relationship("Proveedor")
    nomCateProd = relationship("Categoria")

    def __init__(self, id_producto, nombreProd, descProd, pVentaProd, pCompraProd, stockProd, sMaxProd, ubicaProd,
                 provIdProd, cateIdProd,
                 imgProd="../static/image/image-db/image-default.jpg"):
        self.id_producto = id_producto
        self.nombreProd = nombreProd
        self.descProd = descProd
        self.pVentaProd = pVentaProd
        self.pCompraProd = pCompraProd
        self.stockProd = stockProd
        self.sMaxProd = sMaxProd
        self.ubicaProd = ubicaProd
        self.provIdProd = provIdProd
        self.cateIdProd = cateIdProd
        self.imgProd = imgProd


    def __str__(self):
        return "Producto: ->{} ->{} ->{} ->{} ->{} ->{} ->{} ->{} ->{} ->{} ->{} ->{}".format(self.nombreProd,
                                                                self.descProd,
                                                                self.pVentaProd,
                                                                self.pCompraProd,
                                                                self.stockProd,
                                                                self.sMaxProd,
                                                                self.ubicaProd,
                                                                self.provIdProd,
                                                                self.cateIdProd,
                                                                self.imgProd,
                                                                self.nomProvProd,
                                                                self.nomCateProd)



# definicio de la clase ComprasProv
class Compras(db.Base):
    __tablename__ = 'compras'
    __table_args__ = {'sqlite_autoincrement': True}
    id_compra = Column(Integer, primary_key=True)
    cantidadComp = Column(Integer(), default=0)
    pUnidadComp = Column(Float, nullable=False)
    fechaComp = Column(Date)
    provIdComp = Column(Integer, ForeignKey("proveedor.id_proveedor"))
    prodIdComp = Column(Integer, ForeignKey("producto.id_producto"))
    cateIdComp = Column(Integer, ForeignKey("categoria.id_categoria"))
    nomProdComp = relationship('Producto')
    nomCateComp = relationship('Categoria')
    nomProvComp = relationship('Proveedor')

    def __init__(self, id_compra, cantidadComp, pUnidadComp, fechaComp, provIdComp, prodIdComp, cateIdComp):
        self.id_compra = id_compra
        self.cantidadComp = cantidadComp
        self.pUnidadComp = pUnidadComp
        self.fechaComp = fechaComp
        self.provIdComp = provIdComp
        self.prodIdComp = prodIdComp
        self.cateIdComp = cateIdComp

    def __str__(self):
        return "Compras: -->{} -->{} -->{} -->{} -->{} --{} -->{}".format(self.cantidadComp,
                                                                     self.pUnidadComp,
                                                                     self.fechaComp,
                                                                     self.provIdComp,
                                                                     self.prodIdComp,
                                                                     self.cateIdComp,
                                                                     self.nomProdComp,
                                                                           self.prodIdComp,
                                                                           self.cateIdComp)


# definicion de la clase Ventas
class Ventas(db.Base):
    __tablename__ = 'ventas'
    __table_args__ = {'sqlite_autoincrement': True}
    id_ventas = Column(Integer, primary_key=True)
    cantidadVent = Column(Integer(), default=0)
    pUnidadVent = Column(Float, nullable=False)
    fechaVent = Column(Date)
    prodIdVent = Column(Integer, ForeignKey("producto.id_producto"))
    clieIdVent = Column(Integer, ForeignKey("cliente.id_cliente"))
    provIdVent = Column(Integer, ForeignKey("proveedor.id_proveedor"))
    cateIdVent = Column(Integer, ForeignKey("categoria.id_categoria"))
    nomProdVent = relationship('Producto')
    nomCateVent = relationship('Categoria')
    nomProvVent = relationship('Proveedor')
    nomClieVent = relationship('Cliente')

    def __init__(self, id_ventas, cantidadVent, pUnidadVent, fechaVent, prodIdVent, clieIdVent, provIdVent, cateIdVent):
        self.id_ventas = id_ventas
        self.cantidadVent = cantidadVent
        self.pUnidadVent = pUnidadVent
        self.fechaVent = fechaVent
        self.prodIdVent = prodIdVent
        self.clieIdVent = clieIdVent
        self.provIdVent = provIdVent
        self.cateIdVent = cateIdVent

    def __str__(self):
        return "Ventas: -->{} -->{}  -->{} -->{} -->{} -->{} -->{}".format(self.cantidadVent, self.pUnidadVent,
                                                                           self.fechaVent, self.prodIdVenta,
                                                                           self.clieIdVent,
                                                                           self.provIdVent, self.cateIdVent)
