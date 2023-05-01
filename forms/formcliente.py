from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, EmailField,DecimalField, TextAreaField,SelectField, FileField
from wtforms.validators import InputRequired, Length, NumberRange
import db
from models import Categoria
#


class FormClienDatosCliente(FlaskForm):

    cif_nif = StringField("CIF/NIF:",validators=[InputRequired(), Length(min=1, max=10)]
                          , render_kw={"placeholder": "C.I.F. / N.I.F."})
    nombre = StringField("NOMBRE:", validators=[InputRequired(), Length(min=1, max=150)]
                         , render_kw={"placeholder": "Nombre de la Empresa"})
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

    submit = SubmitField("Modificar datos")

class FormClienTiendaCliente(FlaskForm):

    query = db.session.query(Categoria).all()
    tablaCategorias = [(0, 'Todas')]
    for cat in query:
        cat = (cat.id_categoria, cat.nombreCate)
        tablaCategorias.append(cat)

    categoria = SelectField(u"Categoria:", choices=tablaCategorias)

    submit = SubmitField("Filtrar")
