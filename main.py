# flask
from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response
from sqlalchemy import func, desc
from flask_login import LoginManager, login_user, logout_user, login_required,current_user
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import check_password_hash,generate_password_hash
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

#añadimos la siguiente linea para evitar el error e graficos de:
# RuntimeError: main thread is not in main loop
plt.switch_backend('agg')
import numpy as np

#DDBB
import db


#Models

from models import *

#Formularios
from forms.formusuario import LoginForm, RegistroForm
from forms.formproveedor import FormDatosProveedor
from forms.formcliente import FormClienDatosCliente, FormClienTiendaCliente
from forms.formadministracion import FormAdminAdministrador, FormAdminCrearAdministrador,\
                                    FormAdminProveedor,FormAdminUpdateProveedor, \
                                    FormAdminProductos, FormAdminAltaProducto, \
                                    FormAdminCliente, FormAdminUpdateCliente, FormAdminComprarProducto,\
                                    FormAdminCategorias, FormAdminAltaCategoria



#Otros


#Inicio del servidor web Flask
app = Flask(__name__)

#Configuracion (variables GLOBALES)
#Establecemos secret.key para manejar datos de sesion como son mensajes de flasK"
app.config['SECRET_KEY'] = b"\xc5\x98?\xfa\xd0\xeeEwU'K\x92"
app.config['UPLOAD_FOLDER'] = "static"

csrf=CSRFProtect()
login_manager_app = LoginManager(app)
login_manager_app.login_view="login"


#Routes
@app.route("/")
def index():
    return redirect(url_for('login'))


@app.route('/home')
@login_required
def home():
    #print("ROL:", current_user.rol_id)
    #print("USUARIO:", current_user.id)

    fecha_inicial=(datetime.now()-timedelta(days=30)).strftime("%Y-%m-%d")
    #print(fecha_inicial, fecha_actual)
    #all_products = db_session.query(Product).all()
    #return render_template("home.html", all_products=all_products)
    if current_user.rol_id == 1:
        compras_mes=db.session.query(Compras).filter(Compras.fechaComp >= fecha_inicial).all()
        ventas_mes = db.session.query(Ventas).filter(Ventas.fechaVent >= fecha_inicial).all()

        if len(compras_mes)==0:
            compras_mes=None
        if len(ventas_mes)==0:
            ventas_mes=None

        return render_template("home.html", compras=compras_mes, ventas=ventas_mes)
    if current_user.rol_id == 2:
        cliente_id=db.session.query(Cliente).filter(Cliente.userIdClie==current_user.id).first()

        ventas_mes = db.session.query(Ventas).filter(Ventas.clieIdVent==cliente_id.id_cliente,Ventas.fechaVent >= fecha_inicial).all()

        compras_mes=None
        if len(ventas_mes)==0:
            ventas_mes=None

        return render_template("home.html", compras=compras_mes, ventas=ventas_mes)

    if current_user.rol_id == 3:
        proveedor_id=db.session.query(Proveedor).filter(Proveedor.userIdProv==current_user.id).first()

        ventas_mes = db.session.query(Compras).filter(Compras.provIdComp==proveedor_id.id_proveedor,Compras.fechaComp >= fecha_inicial).all()

        compras_mes=None
        if len(ventas_mes)==0:
            ventas_mes=None


    return render_template("home.html", compras=compras_mes, ventas=ventas_mes)

#Login de cualquier tipo de usuario
@login_manager_app.user_loader
def load_user(id):
    query = db.session.query(User).filter(User.id == int(id)).first()
    return query


@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        usuario = db.session.query(User).filter_by(username=form.username.data).first()

        if usuario:
            if check_password_hash(usuario.password, form.password.data):
                login_user(usuario)

                return redirect(url_for("home"))
            else:
                flash("Password no valida")
                return render_template("usuarios/login.html", form=form)
        else:
            flash("Usuario no válido")
            return render_template("usuarios/login.html", form=form)

    return render_template("usuarios/login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


#************************************************
#** ZONA GRAL DE REGISTRO DE DE USUARIOS       **
#************************************************
#** Registro de usuarios
@app.route("/registro", methods=["GET", "POST"])
def registro():
    form = RegistroForm()

    if form.validate_on_submit():

        # comprobamos el tipo de usuario que ha elegido para
        # asignarle los valores en la base de datos
        if form.tipoUsuario.data == "CLIENTE":
            rol = 2
        else:
            rol = 3

        print("ROLLLLL ELEGIDO:", rol)
        # generamos la password_hash

        hash_password = generate_password_hash(form.password.data)

        # creamos el nuevo usuario enla BBDD de usuarios y en la de proveedores o clientes según el rol

        nuevo_usuario = User(None, username=form.username.data,
                             password=hash_password,
                             rol_id=rol)

        db.session.add(nuevo_usuario)
        db.session.commit()
        db.session.close()

        print("NOMBRE DE USUARIO:_____________", form.username.data)
        # consultamos el registro dado de alta en usuarios para saber que id le ha asignado.
        query = db.session.query(User).filter_by(username=form.username.data).first()

        print(query.id)

        id = None
        nombre = form.nombre.data
        cif = form.cif_nif.data
        direccion = form.direccion.data
        cp = form.cod_post.data
        locProv = form.localidad.data
        email = form.email.data
        telefono = form.telefono.data
        if rol == 2:
            nuevo_registro = Cliente(id, nombre, cif, direccion, cp, locProv, telefono, email, query.id)
            print("Nuevo registro ---------------------->:", nuevo_registro)
        else:
            nuevo_registro = Proveedor(id, nombre, cif, direccion, cp, locProv, email, telefono, query.id)
            print(nuevo_registro)

        db.session.add(nuevo_registro)
        db.session.commit()
        db.session.close()
        # una vez creado el nuevo usuario lo redirigimos nuevamente
        # a LOGIN para que se logee

        return redirect(url_for('login'))
    return render_template("usuarios/registro.html", form=form)

#************************************************
#** ZONA DE PROVEEDORES                        **
#** ROL = 3                                    **
#************************************************
#** Datos del proveedor
@app.route("/datos_proveedor" , methods=['GET', 'POST'])
@login_required
def datos_proveedor():
    user_id = current_user.id
    #print("USER ID DE DATOS PROVEEDOR", user_id)
    proveedor = db.session.query(Proveedor).filter(Proveedor.userIdProv == user_id).first()
    form = FormDatosProveedor()

    form.cif_nif.data = proveedor.cifProv
    form.nombre.data = proveedor.nombreProv
    form.direccion.data = proveedor.direcProv
    form.cod_post.data = proveedor.cpProv
    form.localidad.data = proveedor.locProv
    form.telefono.data = proveedor.tfnoProv
    form.email.data = proveedor.emailProv
    return render_template('proveedor/datos_proveedor.html', form=form, proveedor=proveedor)


#** Actualización Datos del proveedor
@app.route("/update_proveedor/<id>" , methods=['POST'])
@login_required
def updateproveedor(id):
    proveedor = db.session.query(Proveedor).filter(Proveedor.user_id == id).first()

    proveedor.nombreProv = request.form["nombre"]
    proveedor.cifProv = request.form["cif_nif"]
    proveedor.direcProv=request.form["direccion"]
    proveedor.cpProv=request.form["cod_post"]
    proveedor.locProv=request.form["localidad"]
    proveedor.emailProv=request.form["email"]
    proveedor.tfnoProv=request.form["telefono"]


    db.session.commit()
    return redirect(url_for("home"))


#** Graficas Proveedor
@app.route("/provee_graficos" ,methods=['GET', 'POST'])
@login_required
def provee_graficos():

    #consultamos el id del proveedor
     # ----------------------------GRAFICO DE VENTAS (para nosotros compras) --------------------------
    proveedor_id = db.session.query(Proveedor).filter(Proveedor.userIdProv == current_user.id).first()

    query = db.session.query(Compras.prodIdComp, Producto.nombreProd, \
                                    func.sum(Compras.cantidadComp).label('total_cantidades'), \
                                    func.sum(Compras.cantidadComp * Compras.pUnidadComp).label('total_comprado')) \
        .join(Producto, Producto.id_producto == Compras.prodIdComp) \
        .filter(Compras.provIdComp==proveedor_id.id_proveedor) \
        .group_by(Compras.prodIdComp) \
        .order_by(desc('total_cantidades')) \
        .limit(10).all()
    crear_graf(query,"compras")
    fichero="graph/"+str(current_user.id)+"_P_10ventas.png"

    return render_template('proveedor/provee_graficos.html', fichero=fichero)


#************************************************
#** ZONA DE CLIENTES                           **
#** ROL = 2                                    **
#************************************************
#** Datos del Cliente
@app.route("/clien_datoscliente/<id>" , methods=['GET', 'POST'])
@login_required
def clien_datoscliente(id):
    form = FormClienDatosCliente()
    user_id = id
    cliente = db.session.query(Cliente).filter(Cliente.userIdClie == user_id).first()
    if form.validate_on_submit():
        cliente.nombreClie = request.form["nombre"]
        cliente.cifClie = request.form["cif_nif"]
        cliente.direcClie = request.form["direccion"]
        cliente.cpClie = request.form["cod_post"]
        cliente.locClie = request.form["localidad"]
        cliente.emailClie = request.form["email"]
        cliente.tfnoClie = request.form["telefono"]
        db.session.commit()
        return redirect(url_for("home"))

    else:
        form.cif_nif.data = cliente.cifClie
        form.nombre.data = cliente.nombreClie
        form.direccion.data = cliente.direcClie
        form.cod_post.data = cliente.cpClie
        form.localidad.data = cliente.locClie
        form.telefono.data = cliente.tfnoClie
        form.email.data = cliente.emailClie
        return render_template('clientes/clien_datoscliente.html', form=form, cliente=cliente)

#** Graficas Cliente
@app.route("/clien_graficos" ,methods=['GET', 'POST'])
@login_required
def clien_graficos():
    #consultamos el id del cliente
     # ----------------------------GRAFICO DE VENTAS --------------------------
    cliente_id = db.session.query(Cliente).filter(Cliente.userIdClie == current_user.id).first()

    query = db.session.query(Ventas.prodIdVent, Producto.nombreProd, \
                             func.sum(Ventas.cantidadVent).label('total_cantidades'), \
                             func.sum(Ventas.cantidadVent * Ventas.pUnidadVent).label('total_vendido')) \
        .join(Producto, Producto.id_producto == Ventas.prodIdVent) \
        .filter(Ventas.clieIdVent == cliente_id.id_cliente) \
        .group_by(Ventas.prodIdVent) \
        .order_by(desc('total_cantidades')) \
        .limit(10).all()
    crear_graf(query, "ventas")
    fichero="graph/"+str(current_user.id)+"_C_10compras.png"

    return render_template('clientes/clien_graficos.html', fichero=fichero)

#Tienda
@app.route("/clien_tiendacliente" , methods=['GET', 'POST'])
@login_required
def clien_tiendacliente():
    form = FormClienTiendaCliente()

    #lo primero que hacemos es comprobar si el cliente tiene creada la cookie para el carrito
    custom_cookie = request.cookies.get(str(current_user.id), False)

    if form.categoria.data is None or form.categoria.data=='0':
        lista_productos = db.session.query(Producto).all()
    else:
        categoria_id = int(form.categoria.data)
        lista_productos = db.session.query(Producto).filter(Producto.cateIdProd == categoria_id).all()

    for prod in lista_productos:
        if prod.imgProd:
            prod.imgProg = prod.imgProd[3:]

    #datos_carrito = json.loads(carrito)
    if custom_cookie:

        carrito = request.cookies.get(str(current_user.id))
        #volcamos lo que haya en la cookie a json
        datos_carrito = json.loads(carrito)

        total_carro = 0
        for datos in datos_carrito:
            cantidad = datos.get("cantidad")
            pvp = datos.get("pvp")
            total_carro += cantidad * pvp

        return render_template('clientes/clien_tiendacliente.html', form=form, productos=lista_productos,
                                   datos_carrito=datos_carrito, total=total_carro)

    else:
        #Creamos la cookie si no existe con el id del usuario

        datos_carrito = []
        total_carro = 0
        response = make_response(render_template('clientes/clien_tiendacliente.html', form=form, productos=lista_productos,
                                                 datos_carrito=datos_carrito, total=total_carro))
        response.set_cookie(str(current_user.id))
        return response


#********************************************
# Gestion del carrito
#********************************************

@app.route("/clien_comprarproducto/<id>" , methods=['GET', 'POST'])
@login_required
def clien_comprarproducto(id):
    id=int(id)

    #obtenemos el producto elegido
    producto=db.session.query(Producto).filter(Producto.id_producto == id).first()
    # leemos los datos de la cookie
    carrito=request.cookies.get(str(current_user.id))

    #leemos datos carrito y si da error lo inicializamos teniendo en cuenta que la primera vez tenemos que añadir el producto
    try:
        datos_carrito = json.loads(carrito)
        contador=0
        encontrado=False
        for datos in datos_carrito:
            if datos["id"] == producto.id_producto:  # si existe, tengo que aniadir 1 a cantidad
                datos["cantidad"] += 1
                encontrado=True

        if not encontrado:
            datos_carrito.append({"id":producto.id_producto, "producto":producto.nombreProd, "cantidad": 1, "pvp":producto.pVentaProd})

    except:
        datos_carrito=[]
        datos_carrito.append({"id":producto.id_producto, "producto":producto.nombreProd, "cantidad": 1, "pvp":producto.pVentaProd})

    #debemos dar de baja en una cantidad al stock.
    producto.stockProd-=1
    db.session.commit()

    lista_productos = db.session.query(Producto).all()
    response = make_response( redirect(url_for('clien_tiendacliente')))
    response.set_cookie(str(current_user.id), json.dumps(datos_carrito))
    return response


@app.route("/clien_deleteproducto/<id>" , methods=['GET', 'POST'])
@login_required
def clien_deleteproducto(id):
    id=int(id)
    carrito = request.cookies.get(str(current_user.id))
    datos_carrito = json.loads(carrito)

    for datos in datos_carrito:

        if datos["id"] == id:  # si existe, tengo que quitar 1 a cantidad
            datos["cantidad"]-=1
            #debemos comprobar que si el producto queda a 0 en el carro eliminarlo de json
            if datos["cantidad"]==0:
                datos_carrito.remove(datos)

            #debemos aumentar 1 el stock de la bbdd
            producto = db.session.query(Producto).filter(Producto.id_producto == id).first()
            producto.stockProd += 1
            db.session.commit()

    print("Carrito eliminacion de producto", datos_carrito )

    response = make_response(redirect(url_for('clien_tiendacliente')))
    response.set_cookie(str(current_user.id), json.dumps(datos_carrito))
    return response


@app.route("/clien_comprarcarro" , methods=['GET', 'POST'])
@login_required
def clien_comprarcarro():
    cliente = db.session.query(Cliente).filter(Cliente.userIdClie == current_user.id).first()
    id_cliente = cliente.id_cliente
    carrito = request.cookies.get(str(current_user.id))
    datos_carrito = json.loads(carrito)
    for datos in datos_carrito:
        id_producto=datos["id"]
        cantidad_producto=datos["cantidad"]
        precio_unidad=datos["pvp"]
        total_producto=datos["cantidad"]*datos["pvp"]
        #consultamos la tabla de productos para obtener el resto de datos
        producto=db.session.query(Producto).filter(Producto.id_producto==datos["id"]).first()

        nueva_venta=Ventas(None,cantidad_producto,precio_unidad,datetime.now(), id_producto,id_cliente,producto.provIdProd,producto.cateIdProd)

        db.session.add(nueva_venta)
        db.session.commit()

    #debemos vaciar el carrito y para ello usamos expires=0
    response = make_response(redirect(url_for('clien_tiendacliente')))
    response.set_cookie(str(current_user.id), json.dumps(datos_carrito), expires=0)
    return response


#************************************************
#** ZONA DE ADMINISTRADOR                      **
#** ROL = 1                                    **
#************************************************

#** Administracion de Administradores
@app.route('/admin_administrador', methods=['GET', 'POST'])
@login_required
def admin_administrador():
    lista_usuarios = db.session.query(User).filter(User.rol_id == 1).all()
    form = FormAdminAdministrador()

    if request.method=="GET":

        return render_template("admin/admin_administrador.html", form=form, usuarios=lista_usuarios)
    else:

        return redirect(url_for("admin_crearadministrador"))


#** Administracion de Datos Administrador
@app.route('/admin_crearadministrador', methods=['GET', 'POST'])
@login_required
def admin_crearadministrador():
    print("AQUI LLEGO")
    form=FormAdminCrearAdministrador()
    if form.validate_on_submit():
        print("validate")
        print(form.username.data)

        hash_password = generate_password_hash(form.password.data)

        # creamos el nuevo usuario enla BBDD de usuarios y en la de proveedores o clientes según el rol

        nuevo_usuario = User(None, username=form.username.data,
                             password=hash_password,
                             rol_id=1)

        db.session.add(nuevo_usuario)
        db.session.commit()
        return redirect(url_for("admin_administrador"))

    else:
        return render_template("admin/admin_crearadministrador.html", form=form)


#** Administracion de proveedores
@app.route('/admin_proveedores', methods=['GET', 'POST'])
@login_required
def admin_proveedores():
    form = FormAdminProveedor()
    lista_proveedores = db.session.query(Proveedor).all()

    if request.method =='POST':
        return redirect(url_for("home"))
    else:

        return render_template("admin/admin_proveedores.html", form=form, proveedores=lista_proveedores)


#** Administracion de Datos del proveedor
@app.route('/admin_datosproveedor/<id>', methods=['GET', 'POST'])
@login_required
def admin_datosproveedor(id):
    form = FormAdminUpdateProveedor()
    proveedor = db.session.query(Proveedor).filter(Proveedor.id_proveedor == id).first()
    if form.validate_on_submit():
        proveedor.nombreProv = form.nombre.data
        proveedor.cifProv = form.cif_nif.data
        proveedor.direcProv = form.direccion.data
        proveedor.cpProv = form.cod_post.data
        proveedor.locProv = form.localidad.data
        proveedor.emailProv = form.email.data
        proveedor.tfnoProv = form.telefono.data
        db.session.commit()
        return redirect(url_for("admin_proveedores"))
    else:
        form.nombre.data = proveedor.nombreProv
        form.cif_nif.data =  proveedor.cifProv
        form.direccion.data = proveedor.direcProv
        form.cod_post.data = proveedor.cpProv
        form.localidad.data  = proveedor.locProv
        form.email.data = proveedor.emailProv
        form.telefono.data =proveedor.tfnoProv
        return render_template("admin/admin_datosproveedor.html", form=form, proveedor=proveedor)

#** Eliminacion de Datos del proveedor
@app.route('/admin_deleteproveedor/<id>/<id_user>', methods=['GET', 'POST'])
@login_required
def admin_deleteproveedor(id, id_user):
    #consultas antes de borrado:
    # Si tiene productos en stock no se puede borrar.
    # Si tienen productos vendidos a clientes no se puede borrar
    # Si tiene productos comprados al proveedor no se puede borrar.

    #VER RELACIONES EN SQL ALCHEMY.

    prod_stock = db.session.query(Producto.stockProd).filter(Producto.stockProd>0, Producto.provIdProd==id).count()
    prod_venta=db.session.query(Ventas).filter(Ventas.provIdVent==id).count()
    prod_compra = db.session.query(Compras).filter(Compras.provIdComp == id).count()

    if prod_stock > 0:
        flash("Proveedor con artículos en stock. No puede eliminarse")
    elif prod_venta > 0:
        flash("Proveedor con artículos vendidos. No puede eliminarse")
    elif prod_compra > 0:
        flash("Proveedor con artículos comprados. No puede eliminarse")
    else:
        usuario = db.session.query(User).filter(User.id == id_user).delete()
        proveedor = db.session.query(Proveedor).filter(Proveedor.id_proveedor == id).delete()
        db.session.commit()

    return redirect(url_for("admin_proveedores"))

#** Administracion de clientes
@app.route('/admin_clientes', methods=['GET', 'POST'])
@login_required
def admin_clientes():
    form = FormAdminCliente()
    lista_clientes = db.session.query(Cliente).all()

    if request.method == 'POST':
        return redirect(url_for("home"))
    else:

        return render_template("admin/admin_clientes.html", form=form, clientes=lista_clientes)

#** Administracion de Datos del clientes
@app.route('/admin_datoscliente/<id>', methods=['GET', 'POST'])
@login_required
def admin_datoscliente(id):
    form = FormAdminUpdateCliente()
    cliente = db.session.query(Cliente).filter(Cliente.id_cliente == id).first()

    if form.validate_on_submit():
        cliente.nombreClie = form.nombre.data
        cliente.cifClie = form.cif_nif.data
        cliente.direcClie = form.direccion.data
        cliente.cpClie = form.cod_post.data
        cliente.locClie = form.cod_post.data
        cliente.emailClie = form.email.data
        cliente.tfnoClie = form.telefono.data
        db.session.commit()
        return redirect(url_for("admin_clientes"))

    else:
        form.nombre.data = cliente.nombreClie
        form.cif_nif.data =  cliente.cifClie
        form.direccion.data = cliente.direcClie
        form.cod_post.data = cliente.cpClie
        form.localidad.data  = cliente.locClie
        form.email.data = cliente.emailClie
        form.telefono.data =cliente.tfnoClie
        return render_template("admin/admin_datoscliente.html", form=form, cliente=cliente)


#** Eliminacion de Datos de clientes
@app.route('/admin_deletecliente/<id>/<id_user>', methods=['GET', 'POST'])
@login_required
def admin_deletecliente(id, id_user):
    #Comprobamos si el cliente tiene realizada alguna venta
    #en ese caso no podemos borrarlo

    ventas_cliente = db.session.query(Ventas.clieIdVent).filter(Ventas.clieIdVent== id).first()

    if ventas_cliente is None:
        usuario = db.session.query(User).filter(User.id==id_user).delete()
        cliente = db.session.query(Cliente).filter(Cliente.id_cliente==id).delete()
        db.session.commit()
    else:
        flash("Cliente con artículos en ventas. No puede eliminarse")

    return redirect(url_for("admin_clientes"))

#** Administracion de Productos
@app.route('/admin_productos', methods=['GET', 'POST'])
@login_required
def admin_productos():
    form = FormAdminProductos()

    if request.method == 'GET':

        lista_productos = db.session.query(Producto, Proveedor, Categoria).filter(Proveedor.id_proveedor==Producto.provIdProd, Categoria.id_categoria==Producto.cateIdProd).all()

        for prod, prov, cate in lista_productos:
            if prod.imgProd is None or prod.imgProd == '':
                prod.imgProd = None


        return render_template("admin/admin_productos.html", form=form, productos=lista_productos)
    else:

        return redirect(url_for("admin_altaproducto"))

#** Alta de Productos
@app.route('/admin_altaproducto', methods=['GET', 'POST'])
@login_required
def admin_altaproducto():
    form = FormAdminAltaProducto()
    if form.validate_on_submit():
        nombre = form.nombre.data
        categoria_id=int(form.categoria.data)

        descripcion = form.descripcion.data
        precioventa = form.precio_venta.data
        preciocompra = form.precio_compra.data
        stock = form.stock.data
        stockmax = form.stockmax.data

        proveedor_id = int(form.proveedor.data)

        imagen = form.imagen.data
        ubicacion = form.ubicacion.data
        ruta_imagen = None
        nuevo_producto = Producto(None, nombre, descripcion, precioventa, preciocompra, stock, stockmax, ubicacion,
                                  proveedor_id, categoria_id,ruta_imagen)

        print(nuevo_producto)
        db.session.add(nuevo_producto)
        db.session.commit()

        # refrescamos la sesion para obtener el id para luego poder agregar la imagen.
        db.session.refresh(nuevo_producto)

        if imagen.filename != '':
            ruta_imagen = upload_imagen(imagen, nuevo_producto.id_producto)
        else:
            ruta_imagen = None

        nuevo_producto.imgProd = ruta_imagen
        db.session.commit()

        return redirect(url_for("admin_productos"))

    else:
        return render_template("admin/admin_altaproducto.html", form=form)


#** Administracion de Datos de Productos
@app.route('/admin_datosproducto/<id>', methods=['GET', 'POST'])
@login_required
def admin_datosProducto(id):

    producto=db.session.query(Producto).filter(Producto.id_producto == id).first()
    form = FormAdminAltaProducto(proveedor=producto.provIdProd, categoria=producto.cateIdProd)

    if form.validate_on_submit():
        producto.nombreProd = form.nombre.data
        producto.cateIdProd = form.categoria.data
        producto.descProd = form.descripcion.data
        producto.pVentaProd = form.precio_venta.data
        producto.pCompraProd = form.precio_compra.data
        producto.stockProd = form.stock.data
        producto.sMaxProd = form.stockmax.data
        producto.provIdProd = form.proveedor.data
        producto.ubicaProd = form.ubicacion.data


        # gestion de subida de la imagen
        imagen = form.imagen.data


        if imagen.filename == '' and producto.imgProd != '':
            pass
        else:

            if imagen.filename != '':
                ruta_imagen = upload_imagen(imagen, id)
                producto.imgProd = ruta_imagen
            else:
                producto.imgProd = None

        db.session.commit()
        return redirect(url_for("admin_productos"))
    else:
        form.nombre.data = producto.nombreProd
        form.descripcion.data =  producto.descProd
        form.precio_venta.data = producto.pVentaProd
        form.precio_compra.data = producto.pCompraProd
        form.stock.data  = producto.stockProd
        form.stockmax.data = producto.sMaxProd
        form.imagen.data=producto.imgProd


        if producto.imgProd is None or producto.imgProd=='':
            producto.imgProd =None

        form.ubicacion.data= producto.ubicaProd
        return render_template("admin/admin_datosproducto.html", form=form, producto=producto)

#** Compra de Productos bajo stock
@app.route('/admin_comprarproducto/<id>', methods=['GET', 'POST'])
@login_required
def admin_comprarproducto(id):
    form = FormAdminComprarProducto()
    producto = db.session.query(Producto).filter(Producto.id_producto == id).first()

    fecha_now=datetime.now()
    if form.validate_on_submit():

        compra_realizada = Compras(None, form.cantidadCompra.data, form.precioUnidad.data, fecha_now,
                                   producto.provIdProd, producto.id_producto, producto.cateIdProd)
        # añadimos la compra realizada
        db.session.add(compra_realizada)

        # actualizamos el producto

        producto.stockProd=producto.stockProd+form.cantidadCompra.data
        producto.pCompraProd=form.precioUnidad.data



        db.session.commit()
        return redirect(url_for("admin_productos"))
    else:
        form.cantidadCompra.data=0
        form.precioUnidad.data=0
        return render_template("admin/admin_comprarproducto.html", form=form, producto=producto)

#** Eliminacion de Productos
@app.route('/admin_deleteproducto/<id>', methods=['GET', 'POST'])
@login_required
def admin_deleteproducto(id):
    #Comprobamos si el producto tiene stock a 0
    #comprobamos si el producto ha sido vendido alguna vez
    # comprobamos si el producto ha sido comprado alguna vez

    #en ese caso de cumplirse alguna de las anteriores no podemos borrarlo


    prod_stock = db.session.query(Producto).filter(Producto.stockProd > 0, Producto.id_producto == id).count()
    prod_venta = db.session.query(Ventas).filter(Ventas.prodIdVent == id).count()
    prod_compra = db.session.query(Compras).filter(Compras.prodIdComp == id).count()


    if prod_stock > 0:
        flash("Producto con stock. No puede eliminarse")
    elif prod_venta > 0:
        flash("Producto vendido alguna vez. No puede eliminarse")
    elif prod_compra > 0:
        flash("Producto comprado alguna vez. No puede eliminarse")
    else:
        #hacemos primero la consulta para obtener el nombre de la
        # imagen ya que debemos eliminarla tambien.
        producto = db.session.query(Producto).filter(Producto.id_producto == id).first()

        directorio_archivo=producto.imgProd[3:]
        if os.path.exists(directorio_archivo):
            os.remove(directorio_archivo)

        #una vez eliminado el fichero de la imagen podemos eliminar el registro de la BB.DD
        producto = db.session.query(Producto).filter(Producto.id_producto == id).delete()
        db.session.commit()


    return redirect(url_for("admin_productos"))

#** Administracion de Categorias
@app.route('/admin_categorias', methods=['GET', 'POST'])
@login_required
def admin_categorias():
    form = FormAdminCategorias()
    lista_categorias = db.session.query(Categoria).all()


    if request.method == 'GET':
        return render_template("admin/admin_categorias.html", form=form, categorias=lista_categorias)
    else:
        return redirect(url_for("admin_altacategoria"))

#** Alta de Categorias
@app.route('/admin_altacategoria', methods=['GET', 'POST'])
@login_required
def admin_altacategoria():
    form = FormAdminAltaCategoria()
    if form.validate_on_submit():
        nombre = form.nombre.data
        nueva_categoria = Categoria(None, nombre)\

        db.session.add(nueva_categoria)
        db.session.commit()

        return redirect(url_for("admin_categorias"))

    else:
        return render_template("admin/admin_altacategoria.html", form=form)

#** Administracion Datos de Categorias
@app.route('/admin_datoscategoria/<id>', methods=['GET', 'POST'])
@login_required
def admin_datoscategoria(id):

    categoria=db.session.query(Categoria).filter(Categoria.id_categoria == id).first()

    form = FormAdminAltaCategoria()
    if form.validate_on_submit():
        categoria.nombreCate = form.nombre.data
        db.session.commit()
        return redirect(url_for("admin_categorias"))
    else:
        form.nombre.data = categoria.nombreCate

        return render_template("admin/admin_datoscategoria.html", form=form, categoria=categoria)


#** Eliminacion de Categorias
@app.route('/admin_deletecategoria/<id>', methods=['GET', 'POST'])
@login_required
def admin_deletecategoria(id):

    #Comprobamis si la categoria esta en algún producto
    #comprobamos si la está en un producto y  vendido alguna vez
    # comprobamos si la categoria esta en algún producto  comprado alguna vez

    #en ese caso de cumplirse alguna de las anteriores no podemos borrarla



    cate_prod = db.session.query(Producto).filter(Producto.cateIdProd == id).count()
    cate_venta = db.session.query(Ventas).filter(Ventas.cateIdVent == id).count()
    cate_compra = db.session.query(Compras).filter(Compras.cateIdComp == id).count()

    if cate_prod > 0:
        flash("Productos con categoria asignada. No puede eliminarse")
    elif cate_venta > 0:
        flash("Productos vendidos con categoria asignada. No puede eliminarse")
    elif cate_compra > 0:
        flash("Producto comprados con categoria asignada. No puede eliminarse")
    else:
        categoria = db.session.query(Categoria).filter(Categoria.id_categoria == id).delete()
        db.session.commit()

    return redirect(url_for("admin_categorias"))


#** GRAFICOS COMPRAS -ADMINISTRACION-
@app.route('/admin_grafcompras', methods=['GET', 'POST'])
@login_required
def admin_grafcompras():

    # ----------------------------GRAFICO DE VENTAS --------------------------
    query=db.session.query(Ventas.prodIdVent,Producto.nombreProd, \
                                func.sum(Ventas.cantidadVent).label('total_cantidades'),\
                                func.sum(Ventas.cantidadVent*Ventas.pUnidadVent).label('total_vendido'))\
                                .join(Producto, Producto.id_producto==Ventas.prodIdVent)\
                                .group_by(Ventas.prodIdVent)\
                                .order_by(desc('total_cantidades'))\
                                .limit(10).all()
    #crear_graf(query, "ventas")
    graf_ventas = crear_graf(query, "ventas")
    print("HAY GRAFICO Ventas?", graf_ventas)

    # ----------------------------GRAFICO DE COMPRAS --------------------------
    query = db.session.query(Compras.prodIdComp, Producto.nombreProd, \
                                    func.sum(Compras.cantidadComp).label('total_cantidades'), \
                                    func.sum(Compras.cantidadComp * Compras.pUnidadComp).label('total_comprado')) \
        .join(Producto, Producto.id_producto == Compras.prodIdComp) \
        .group_by(Compras.prodIdComp) \
        .order_by(desc('total_cantidades')) \
        .limit(10).all()
    graf_compras=crear_graf(query, "compras")
    print("HAY GRAFICO COMPRAS?", graf_compras)

    # ----------------------------GRAFICO DE Bºs en %--------------------------
    beneficios_join = db.session.query(Ventas.prodIdVent, Producto.nombreProd, \
                                    Compras.pUnidadComp,
                                   func.sum(Ventas.cantidadVent).label('total_cantidades'), \
                                   func.sum(Ventas.cantidadVent * Ventas.pUnidadVent).label('total_vendido'))\
        .join(Producto, Producto.id_producto == Ventas.prodIdVent) \
        .join(Compras, Compras.prodIdComp == Ventas.prodIdVent) \
        .group_by(Ventas.prodIdVent) \
        .order_by(desc('total_cantidades')) \
        .limit(10).all()

    productos = []
    beneficio=[]
    if len(productos) < 1 or len(beneficio) < 1:
        graf_benefic = False
    else:
        for i in beneficios_join:

            productos.append(i[1])
            beneficio.append(i[4]-i[2]*i[3])

        #contruimos un desfase para poder separar el sector con mayor Bº y para ello buscamos el indice del valor
        #maximo de beneficio
        desfase=[]
        for i in range(len(productos)):
            if i == beneficio.index(max(beneficio)):
                desfase.append(0.1)
            else:
                desfase.append(0)
        #creamos el gráfico poniendo la funcion para que nos de porcentajes
        plt.pie(beneficio, labels=productos, autopct="%0.2f %%", explode=desfase)
        plt.legend(title="Facturación Productos", labels=beneficio, loc="upper center",
                   bbox_to_anchor=(0.5, -0.04), ncol=2)


        #con esto hacemos que salga redondo y no achatado
        plt.axis("equal")

        plt.title('Bº de los 10 productos más vendidos')

        plt.savefig('static/graph/admin_10Benef.png', bbox_inches='tight')

        # Eliminamos la grafica creada en memoria
        plt.clf()

    print("ANTES DE ENVIAR:", graf_compras, "y:", graf_ventas)
    return render_template("admin/admin_grafcompras.html", compras=graf_compras, ventas=graf_ventas, benef=graf_benefic)


#definicion de otras funciones ----------------------------
#gestion de imagenes
def upload_imagen(imagen, id):
    nombre_imagen = secure_filename(str(id) + '_' + imagen.filename)
    ruta_imagen = os.path.join(app.config["UPLOAD_FOLDER"]+'\\uploads\\{}'.format(nombre_imagen))
    imagen.save(ruta_imagen)
    print("RUTA:", ruta_imagen)
    nombre_imagen="..\\"+ruta_imagen
    print(nombre_imagen)
    return nombre_imagen

#Lista de productos segun categoria
def listaProductos_cat(categoria):
    if categoria != 0:
        return db.session.query(Producto).filter(Producto.cateIdProd == categoria).all()
    else:
        return db.session.query(Producto).all()

def status_401(error):
    return redirect(url_for('login'))

def status_404(error):
    return "<h1>P&aacute;gina no encontrada</h1>", 404

def obtener_idproveedor(nombre):
    proveedor= db.session.query(Proveedor).filter(Proveedor.nombreProv==nombre).first()
    return proveedor.id_proveedor

@app.route("/filtra_categoria/<nombre>",methods=['POST','GET'])
@login_required
def filtra_categoria(nombre):
    if nombre=="Todas":
        categoria=0
    else:
        i= db.session.query(Categoria.id_categoria).filter(Categoria.nombreCate == nombre).first()
        categoria=i.id_categoria

    print("FILTRA:", categoria)

    return redirect(url_for("clien_tiendacliente", categoria=categoria))

#creacion de graficas
def crear_graf(query,grafico):
    print("-------------CREAR GRAFICAS -------------")
    print(current_user.rol_id)
    print (query)
    if current_user.rol_id == 1:
        productos=[]
        unidades=[]
        print(len(productos), len(unidades))
        for i in query:
            print(i)
            productos.append(i[1])
            unidades.append(i[2])
        if len(productos) < 1 or len(unidades) < 1:
            print("no hay datos")
            return False

        print("G.:, ", productos)
        # Obtenemos una lista con las posiciones de cada articulo(producto), asignandole (0,1,2...9)
        x_pos = np.arange(len(productos))

        # creamos la grafica, en este caso de barras horizontales
        plt.bar(x_pos, unidades, color='blue')

        # añadimos las etiquetas de cada producto y las rotamos 45 grados y las ponemos a la dcha para que queden bien
        plt.xticks(x_pos, productos, rotation=45, ha='right')

        # añadimos las etiquetas de las cantidades vendidas
        print(grafico)
        if grafico=="ventas":

            plt.ylabel('Unidades Vendidas')
            plt.xlabel('Productos')
            # añadimos el titulo al gráfico
            plt.title('10 productos más vendidos')
            # guardamos la grafica con el parametro bbox para que no nos corte la imagen
            plt.savefig('static/graph/admin_10ventas.png', bbox_inches='tight')
            # Eliminamos la grafica creada en memoria
            plt.clf()
        if grafico=="compras":
            plt.ylabel('Unidades Compradas')
            plt.xlabel('Productos')
            # añadimos el titulo al gráfico
            plt.title('10 productos más comprados')
            # guardamos la grafica con el parametro bbox para que no nos corte la imagen
            plt.savefig('static/graph/admin_10compras.png', bbox_inches='tight')
            # Eliminamos la grafica creada en memoria
            plt.clf()
    if current_user.rol_id == 2:
        productos = []
        unidades = []
        for i in query:
            print(i)
            productos.append(i[1])
            unidades.append(i[2])
        print("G.:, ", productos)
        # Obtenemos una lista con las posiciones de cada articulo(producto), asignandole (0,1,2...9)
        x_pos = np.arange(len(productos))

        # creamos la grafica, en este caso de barras horizontales
        plt.bar(x_pos, unidades, color='blue')

        # añadimos las etiquetas de cada producto y las rotamos 45 grados y las ponemos a la dcha para que queden bien
        plt.xticks(x_pos, productos, rotation=45, ha='right')

        # añadimos las etiquetas de las cantidades vendidas
        print(grafico)

        plt.ylabel('Unidades Compradas')
        plt.xlabel('Productos')
        # añadimos el titulo al gráfico
        plt.title('10 productos más comprados')

        # guardamos la grafica con el parametro bbox para que no nos corte la imagen
        fichero = str(current_user.id) + "_" + "C_10compras.png"
        plt.savefig('static/graph/' + fichero, bbox_inches='tight')
        # Eliminamos la grafica creada en memoria
        plt.clf()
    if current_user.rol_id == 3:
        print("GRAFICA DEL PROVEEDOR")
        productos = []
        unidades = []
        for i in query:
            print(i)
            productos.append(i[1])
            unidades.append(i[2])
        print("G.:, ", productos)
        # Obtenemos una lista con las posiciones de cada articulo(producto), asignandole (0,1,2...9)
        x_pos = np.arange(len(productos))

        # creamos la grafica, en este caso de barras horizontales
        plt.bar(x_pos, unidades, color='blue')

        # añadimos las etiquetas de cada producto y las rotamos 45 grados y las ponemos a la dcha para que queden bien
        plt.xticks(x_pos, productos, rotation=45, ha='right')

        # añadimos las etiquetas de las cantidades vendidas
        print(grafico)
        plt.ylabel('Unidades Vendidas')
        plt.xlabel('Productos')
        # añadimos el titulo al gráfico
        plt.title('10 productos más vendidos')
        # guardamos la grafica con el parametro bbox para que no nos corte la imagen
        fichero=str(current_user.id)+"_"+"P_10ventas.png"
        plt.savefig('static/graph/'+fichero, bbox_inches='tight')
        # Eliminamos la grafica creada en memoria
        plt.clf()

    return


if __name__ == "__main__":
    db.Base.metadata.create_all(db.engine)
    csrf.init_app(app)
    app.register_error_handler(401,status_401)
    app.register_error_handler(404, status_404)
    app.run(debug=True)                 #hay que instalar pip install flask


