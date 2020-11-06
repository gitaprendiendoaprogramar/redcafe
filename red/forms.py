from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, IntegerField, \
    TextAreaField, SelectField, PasswordField, HiddenField
from wtforms.fields.html5 import EmailField
from flask_wtf.file import FileField
from wtforms.validators import Required, NumberRange


class FormCategoria(FlaskForm):
    nombre = StringField("Nombre:",
                         validators=[Required("Tienes que introducir el dato")]
                         )
    submit = SubmitField('Enviar')

class FormTitulo(FlaskForm):
    nombre = StringField("Nombre:",
                         validators=[Required("Tienes que introducir el dato")]
                         )
    submit = SubmitField('Enviar')

class FormForo(FlaskForm):
    UsuarioId = HiddenField()
    TituloId = SelectField("Titulo:", coerce=int)
    descripcion = TextAreaField("Descripción:")
    created_at = HiddenField()
    submit = SubmitField('Enviar')
    
class FormBlog(FlaskForm):
    UsuarioId = HiddenField()
    titulo = StringField("Titulo:",
                         validators=[Required("Tienes que introducir el dato")]
                         )
    descripcion = TextAreaField("Descripción:")
    created_at = HiddenField()
    submit = SubmitField('Enviar')
    comentario = TextAreaField("Comentario:", validators=[Required("Tienes que introducir el dato")])
    comentar = SubmitField('Comentar')
      

class FormSINO(FlaskForm):
    si = SubmitField('Si')
    no = SubmitField('No')

class LoginForm(FlaskForm):
    username = StringField('Login', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField('Entrar')

class FormUsuario(FlaskForm):
    username = StringField('Login', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])
    nombre = StringField('Nombre completo')
    email = EmailField('Email')
    submit = SubmitField('Aceptar')

class FormChangePassword(FlaskForm):
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField('Aceptar')
