from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, EmailField
from wtforms.validators import InputRequired, EqualTo, Length, ValidationError, NumberRange
import db
# models
from models import User, Rol


# Formulario para el login de la app
class LoginForm(FlaskForm):
    username = StringField("USUARIO DE ACCESO:", validators=[InputRequired(), Length(
        min=4, max=25)], render_kw={"placeholder": "Username"})
    password = PasswordField("PASSWORD:", validators=[InputRequired(), Length(
        min=4, max=25)], render_kw={"placeholder": "password"})
    submit = SubmitField("Login")

# Formulario para el registro de usuario, comprobando
# que no exista el nombre
class RegistroForm(FlaskForm):
    # hacemos consulta a la tabla de ROLES para cargar odos los que haya distintos de ADMINISTRADOR

    query = db.session.query(Rol).filter(Rol.id_rol > 1)
    # print("----->FORMULAR", query)
    # print(type(query))
    tablaroles = []
    for i in query:
        tablaroles.append(i.descripcion)
    # print(tablaroles)
    username = StringField("USUARIO DE ACCESO:", validators=[InputRequired(), Length(
        min=4, max=25)], render_kw={"placeholder": "username"})

    password = PasswordField("PASSWORD",
        validators=[InputRequired(), EqualTo('confirm', message='Password deben ser iguales'), Length(
            min=4, max=25, message="la Password debe ser entre 4 y 25 caracteres")], render_kw={"placeholder": "password"})

    confirm = PasswordField("REPITA PASSWORD:", validators=[InputRequired()], render_kw={"placeholder": "repita password"})

    tipoUsuario = SelectField("TIPO DE USUARIO (SELECCIONE UNA OPCION:", choices=tablaroles, validators=[InputRequired()],
                              render_kw={"placeholder": "Tipo de usuario"})

    nombre = StringField("NOMBRE COMPLETO:", validators=[InputRequired(), Length(min=1, max=150)]
                         , render_kw={"placeholder": "Nombre de la Empresa"})

    cif_nif = StringField("CIF/NIF:", validators=[InputRequired(), Length(min=1, max=10)]
                          , render_kw={"placeholder": "C.I.F. / N.I.F."})

    direccion = StringField("DOMICILIO:", validators=[InputRequired(), Length(min=1, max=150)]
                            , render_kw={"placeholder": "Dirección"})
    cod_post = IntegerField("CODIGO POSTAL:", validators=[InputRequired(), NumberRange(min=1, max=99999)]
                            , render_kw={"placeholder": "Código Postal"})
    localidad = StringField("LOCALIDAD/PROVINCIA:", validators=[InputRequired(), Length(min=1, max=150)]
                            , render_kw={"placeholder": "Localidad(Provincia)"})
    telefono = StringField("TELEFONO:", validators=[InputRequired(), Length(min=1, max=20)]
                           , render_kw={"placeholder": "Teléfono/s de contacto"})
    email = EmailField("EMAIL:", validators=[InputRequired(), Length(min=1, max=100)]
                       , render_kw={"placeholder": "Email"})

    submit = SubmitField("Registro")

    def validate_username(self, username):
        # consultamos si existe un usuario con el mismo nombre

        usuario = db.session.query(User).filter_by(username=username.data).first()
        # print(usuario)
        if usuario:
            raise ValidationError("Nombre de usuario ya existe. Elija otro, por favor")
