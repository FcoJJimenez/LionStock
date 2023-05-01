from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, EmailField
from wtforms.validators import InputRequired, Length, NumberRange



#

class FormDatosProveedor(FlaskForm):

    cif_nif = StringField("CIF/NIF:", validators=[InputRequired(), Length(min=1, max=10)]
                          , render_kw={"placeholder": "C.I.F. / N.I.F."})
    nombre = StringField("PROVEEDOR:", validators=[InputRequired(), Length(min=1, max=150)]
                         , render_kw={"placeholder": "Nombre de la Empresa"})
    direccion = StringField("DOMICILIO:", validators=[InputRequired(), Length(min=1, max=150)]
                            , render_kw={"placeholder": "Dirección"})
    cod_post = IntegerField("C. POSTAL:", validators=[InputRequired(), NumberRange(min=1, max=99999)]
                            , render_kw={"placeholder": "Código Postal"})
    localidad = StringField("LOCALIDAD:",validators=[InputRequired(), Length(min=1, max=150)]
                            , render_kw={"placeholder": "Localidad(Provincia)"})
    telefono = StringField("TFNO:", validators=[InputRequired(), Length(min=1, max=20)]
                           , render_kw={"placeholder": "Teléfono/s de contacto"})
    email = EmailField("EMAIL:", validators=[InputRequired(), Length(min=1, max=100)]
                       , render_kw={"placeholder": "Email"})

    submit = SubmitField("Modificar datos")
