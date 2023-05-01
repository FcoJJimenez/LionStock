from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,PasswordField, IntegerField, EmailField,DecimalField, TextAreaField,SelectField, FileField
from wtforms.validators import InputRequired, EqualTo, Length, ValidationError, NumberRange

#from wtforms_sqlalchemy.fields import QuerySelectField
#from wtforms.fields import DateField, DateTimeField
import db
#from datetime import datetime

from models import Proveedor, Categoria, User



#Formularios de Administrador zona proveedores
class FormAdminAdministrador(FlaskForm):

    id=IntegerField("ID")
    username = StringField("USUARIO",validators=[InputRequired(), Length(
        min=4, max=25)], render_kw={"placeholder": "username"})

    password = PasswordField(
        validators=[InputRequired(), EqualTo('confirm', message='Password deben ser iguales'), Length(
            min=4, max=25,)], render_kw={"placeholder": "password"})

    confirm = PasswordField(validators=[InputRequired()], render_kw={"placeholder": "repita password"})

    rol=StringField("ROL")

    submit = SubmitField("Crear Administrador")

class FormAdminCrearAdministrador(FlaskForm):

    username = StringField("USUARIO DE ACCESO:", validators=[InputRequired(), Length(
        min=4, max=25)], render_kw={"placeholder": "username"})

    password = PasswordField("PASSWORD:",
        validators=[InputRequired(), EqualTo('confirm', message='Password deben ser iguales'), Length(
            min=4, max=25, message="La Password debe ser entre 4 y 25 caracteres")], render_kw={"placeholder": "password"})

    confirm = PasswordField("REPITA PASSWORD:", validators=[InputRequired()], render_kw={"placeholder": "repita password"})

    submit = SubmitField("Guardar")

    def validate_username(self, username):
        # consultamos si existe un usuario con el mismo nombre

        usuario = db.session.query(User).filter_by(username=username.data).first()
        # print(usuario)
        if usuario:
            raise ValidationError("Nombre de usuario ya existe. Elija otro, por favor")

#Formularios de Administrador zona proveedores
class FormAdminProveedor(FlaskForm):

    cif_nif = StringField("C.I.F./N.I.F.", validators=[InputRequired(), Length(min=1, max=10)]
                          , render_kw={"placeholder": "C.I.F. / N.I.F."})
    nombre = StringField("PROVEEDOR", validators=[InputRequired(), Length(min=1, max=150)]
                         , render_kw={"placeholder": "Nombre de la Empresa"})
    direccion = StringField("DOMICILIO", validators=[InputRequired(), Length(min=1, max=150)]
                            , render_kw={"placeholder": "Dirección"})
    cod_post = IntegerField("C. POST.", validators=[InputRequired(), NumberRange(min=1, max=99999)]
                            , render_kw={"placeholder": "Código Postal"})
    localidad = StringField("LOCALIDAD", validators=[InputRequired(), Length(min=1, max=150)]
                            , render_kw={"placeholder": "Localidad(Provincia)"})
    telefono = StringField("TFNO.", validators=[InputRequired(), Length(min=1, max=20)]
                           , render_kw={"placeholder": "Teléfono/s de contacto"})
    email = EmailField("EMAIL", validators=[InputRequired(), Length(min=1, max=100)]
                       , render_kw={"placeholder": "Email"})
    submit = SubmitField("Cerrar")

class FormAdminUpdateProveedor(FlaskForm):
    cif_nif = StringField("C.I.F. / N.I.F :", validators=[InputRequired(), Length(min=1, max=10)]
                          , render_kw={"placeholder": "C.I.F. / N.I.F."})
    nombre = StringField("NOMBRE:", validators=[InputRequired(), Length(min=1, max=150)]
                         , render_kw={"placeholder": "Nombre de la Empresa"})
    direccion = StringField("DOMICILIO:", validators=[InputRequired(), Length(min=1, max=150)]
                            , render_kw={"placeholder": "Dirección"})
    cod_post = IntegerField("C. POSTAL:", validators=[InputRequired(), NumberRange(min=1, max=99999)]
                            , render_kw={"placeholder": "Código Postal"})
    localidad = StringField("LOCALIDAD PROVINCIA:",validators=[InputRequired(), Length(min=1, max=150)]
                            , render_kw={"placeholder": "Localidad(Provincia)"})
    telefono = StringField("TELEFONO:",validators=[InputRequired(), Length(min=1, max=20)]
                           , render_kw={"placeholder": "Teléfono/s de contacto"})
    email = EmailField("EMAIL:",validators=[InputRequired(), Length(min=1, max=100)]
                       , render_kw={"placeholder": "Email"})

    submit = SubmitField("Modificar")


#Formularios de Administrador zona Categorias
class FormAdminCategorias(FlaskForm):
    nombre = StringField("NOMBRE",validators=[InputRequired(), Length(min=1, max=50)]
                         , render_kw={"placeholder": "Nombre de la Empresa"})

    submit = SubmitField("Crear Categoria")


# Formularios de Administrador zona Categorias
class FormAdminAltaCategoria(FlaskForm):
    nombre = StringField("NOMBRE CATEGORIA:", validators=[InputRequired(), Length(min=1, max=50)]
                         , render_kw={"placeholder": "Nombre de la Empresa"})

    submit = SubmitField("Guardar")


#Formularios de Administrador zona productos
class FormAdminProductos(FlaskForm):
    nombre = StringField("NOMBRE",validators=[InputRequired(), Length(min=1, max=50)]
                         , render_kw={"placeholder": "Nombre de la Empresa"})
    categoria = StringField("CATEGORIA")
    descripcion = TextAreaField("DESCRIPCION",validators=[InputRequired(), Length(min=1, max=250)]
                            , render_kw={"placeholder": "Dirección"})
    precio_venta = DecimalField("P.V.P.",validators=[InputRequired(), NumberRange(min=0, max=99999)]
                            , render_kw={"placeholder": "Código Postal"})
    precio_compra = DecimalField("P. ULT. COMPRA",validators=[InputRequired(), NumberRange(min=0, max=99999) ]
                            , render_kw={"placeholder": "Localidad(Provincia)"})
    stock = IntegerField("STOCK ACTUAL",validators=[InputRequired()]
                           , render_kw={"placeholder": "Teléfono/s de contacto"})
    stockmax = IntegerField("STOCK MAX.",validators=[InputRequired()]
                       , render_kw={"placeholder": "Email"})
    proveedor_id = StringField("PROVEEDOR",validators=[InputRequired(), Length(min=1, max=100)]
                          , render_kw={"placeholder": "Email"})
    ubicacion = StringField("UBICACION",validators=[InputRequired(), Length(min=1, max=100)]
                          , render_kw={"placeholder": "Email"})

    imagen = FileField("IMAGEN")

    submit = SubmitField("Crear Producto")

class FormAdminAltaProducto(FlaskForm):

    query = db.session.query(Proveedor).all()
    tablaProveedores = []
    for prov in query:
        proveedor=(prov.id_proveedor, prov.nombreProv)
        tablaProveedores.append(proveedor)



    query = db.session.query(Categoria).all()
    tablaCategorias = [(0,'Todas')]
    for cat in query:
        cat = (cat.id_categoria, cat.nombreCate)
        tablaCategorias.append(cat)



    nombre = StringField("NOMBRE PRODUCTO:", validators=[InputRequired(), Length(min=1, max=50)], render_kw={"placeholder": "Nombre Producto"})
    proveedor = SelectField("PROVEEDOR:", choices=tablaProveedores)
    categoria = SelectField("CATEGORIA:", choices=tablaCategorias)
    descripcion = TextAreaField("DESCRIPCION:", validators=[InputRequired(), Length(min=1, max=250)],
                                render_kw={"placeholder": "Descripción"})
    precio_venta = DecimalField("P. VENTA PUBL.:", validators=[InputRequired(), NumberRange(min=0, max=999999)],
                                render_kw={"placeholder": "Precio Venta"})
    precio_compra = DecimalField("ULT. PRECIO COMPRA", validators=[InputRequired(), NumberRange(min=0, max=999999)],
                                 render_kw={"placeholder": "Precio Compra"})
    stock = IntegerField("STOCK ACTUAL", validators=[InputRequired(), NumberRange(min=0, max=999999)],
                         render_kw={"placeholder": "Stock Actual"})
    stockmax = IntegerField("STOCK MAXIMO", validators=[InputRequired(), NumberRange(min=0, max=999999)],
                            render_kw={"placeholder": "Stock Maximo"})

    imagen = FileField("Imagen:")
    ubicacion = StringField("UBICACION DEL PRODUCTO:", validators=[InputRequired(), Length(min=1, max=100)],
                            render_kw={"placeholder": "Ubicacion"})

    submit = SubmitField("Guardar")

class FormAdminComprarProducto(FlaskForm):

    cantidadCompra = IntegerField("UNIDADES A COMPRAR:", validators=[InputRequired(), NumberRange(min=1, max=999999)],
                         render_kw={"placeholder": "Unidades a comprar"})

    precioUnidad = DecimalField("PRECIO POR UNIDAD:", validators=[InputRequired(), NumberRange(min=0, max=999999)],
                                render_kw={"placeholder": "Precio Unidad"})
    #fechaCompra =DateField(format='%d-%m-%Y', default=datetime.now())

    submit = SubmitField("Pedir")


#Formularios de Administrador zona clientes
class FormAdminCliente(FlaskForm):

    nombre = StringField("CLIENTE", validators=[InputRequired(), Length(min=1, max=150)]
                         , render_kw={"placeholder": "Nombre de la Empresa"})
    cif_nif = StringField("C.I.F./N.I.F.", validators=[InputRequired(), Length(min=1, max=10)]
                          , render_kw={"placeholder": "C.I.F. / N.I.F."})
    direccion = StringField("DOMICILIO",validators=[InputRequired(), Length(min=1, max=150)]
                            , render_kw={"placeholder": "Dirección"})
    cod_post = IntegerField("C. POST.",validators=[InputRequired(), NumberRange(min=1, max=99999)]
                            , render_kw={"placeholder": "Código Postal"})
    localidad = StringField("LOCALIDAD",validators=[InputRequired(), Length(min=1, max=150)]
                            , render_kw={"placeholder": "Localidad(Provincia)"})
    telefono = StringField("TELEFONO",validators=[InputRequired(), Length(min=1, max=20)]
                           , render_kw={"placeholder": "Teléfono/s de contacto"})
    email = EmailField("EMAIL",validators=[InputRequired(), Length(min=1, max=100)]
                       , render_kw={"placeholder": "Email"})
    submit = SubmitField("Cerrar")


class FormAdminUpdateCliente(FlaskForm):
    cif_nif = StringField("C.I.F. / N.I.F.:", validators=[InputRequired(), Length(min=1, max=10)]
                          , render_kw={"placeholder": "C.I.F. / N.I.F."})
    nombre = StringField("NOMBRE:", validators=[InputRequired(), Length(min=1, max=150)]
                         , render_kw={"placeholder": "Nombre de la Empresa"})
    direccion = StringField("DOMICILIO:", validators=[InputRequired(), Length(min=1, max=150)]
                            , render_kw={"placeholder": "Dirección"})
    cod_post = IntegerField("C. POST.:", validators=[InputRequired(), NumberRange(min=1, max=99999)]
                            , render_kw={"placeholder": "Código Postal"})
    localidad = StringField("LOCALIDAD/PROVINCIA:", validators=[InputRequired(), Length(min=1, max=150)]
                            , render_kw={"placeholder": "Localidad(Provincia)"})
    telefono = StringField("TELEFONO:", validators=[InputRequired(), Length(min=1, max=20)]
                           , render_kw={"placeholder": "Teléfono/s de contacto"})
    email = EmailField("EMAIL:", validators=[InputRequired(), Length(min=1, max=100)]
                       , render_kw={"placeholder": "Email"})

    submit = SubmitField("Modificar")

