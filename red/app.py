from flask import Flask, render_template, redirect, url_for, request, abort, \
    session, make_response, Response
from flask_sqlalchemy import SQLAlchemy
from red import config
from red.forms import FormTitulo, FormForo, FormBlog, FormSINO, LoginForm,\
    FormUsuario, FormChangePassword
from werkzeug.utils import secure_filename
from flask_login import LoginManager, login_user, logout_user, login_required,\
    current_user
import os
from bson import json_util
from bson.objectid import ObjectId
import json
from datetime import datetime

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@app.route('/')
def inicio():
    return render_template("inicio.html")

@app.route('/foros')
@app.route('/foros/<id>')
def foros(id='0'):
    from red.models import Foros, Titulos
    titulo = Titulos.query.get(id)
    if id == '0':
        foros = Foros.query.all()
    else:
        foros = Foros.query.filter_by(TituloId=id)
    titulos = Titulos.query.all()
    print(foros)
    return render_template("foros.html", foros=foros, titulos=titulos, titulo=titulo)

@app.route('/categorias')
def categorias():
    from red.models import Titulos
    categorias = Titulos.query.all()
    return render_template("categorias.html", categorias=categorias)

@app.route('/categorias/new', methods=["get", "post"])
@login_required
def categorias_new():
    from red.models import Titulos
    # Control de permisos
    if not current_user.is_admin():
        abort(404)
    form = FormTitulo(request.form)
    if form.validate_on_submit():
        tit = Titulos(nombre=form.nombre.data)
        db.session.add(tit)
        db.session.commit()
        return redirect(url_for("categorias"))
    else:
        return render_template("categorias_new.html", form=form)

@app.route('/categorias/<id>/edit', methods=["get", "post"])
@login_required
def categorias_edit(id):
    from red.models import Titulos
    # Control de permisos
    if not current_user.is_admin():
        abort(404)
    tit = Titulos.query.get(id)
    if tit is None:
        abort(404)
    form = FormTitulo(request.form, obj=tit)
    if form.validate_on_submit():
        form.populate_obj(tit)
        db.session.commit()
        return redirect(url_for("categorias"))
    return render_template("categorias_new.html", form=form)

@app.route('/categorias/<id>/delete', methods=["get", "post"])
@login_required
def categorias_delete(id):
    from red.models import Titulos
    # Control de permisos
    if not current_user.is_admin():
        abort(404)
    tit = Titulos.query.get(id)
    if tit is None:
        abort(404)
    form = FormSINO()
    if form.validate_on_submit():
        if form.si.data:
            db.session.delete(tit)
            db.session.commit()
        return redirect(url_for("categorias"))
    return render_template("categorias_delete.html", form=form, tit=tit)

@app.route('/foros/new', methods=["get", "post"])
@login_required
def foros_new():
    from red.models import Foros, Titulos
     #Control de permisos
    if not current_user.is_admin():
        abort(404)
    form = FormForo()
    titulos = [(c.id, c.nombre) for c in Titulos.query.all()[1:]]
    form.TituloId.choices = titulos
    form.UsuarioId.data = current_user.id
    form.created_at.data = datetime.now()
    if form.validate_on_submit():
        frs = Foros()
        form.populate_obj(frs)
        db.session.add(frs)
        db.session.commit()
        return redirect(url_for("foros"))
    else:
        return render_template("foros_new.html", form=form, accion='add')

@app.route('/foros/<id>/edit', methods=["get", "post"])
@login_required
def foros_edit(id):
    from red.models import Foros, Titulos
     #Control de permisos no
    if not current_user.is_admin():
        abort(404)
    frs = Foros.query.get(id)
    if frs is None:
       abort(404)
    form = FormForo(obj=frs)
    titulos = [(c.id, c.nombre) for c in Titulos.query.all()[1:]]
    form.TituloId.choices = titulos
    if form.validate_on_submit():
        form.populate_obj(frs)
        db.session.commit()
        return redirect(url_for("foros"))
    return render_template("foros_new.html", form=form, accion='edt')

@app.route('/foros/<id>/delete', methods=["get", "post"])
@login_required
def foros_delete(id):
    from red.models import Foros
     #Control de permisos
    if not current_user.is_admin():
        abort(404)
    frs = Foros.query.get(id)
    if frs is None:
        abort(404)
    form = FormSINO()
    if form.validate_on_submit():
        if form.si.data:
            db.session.delete(frs)
            db.session.commit()
        return redirect(url_for("foros"))
    return render_template("foros_delete.html", form=form, frs=frs)

@app.route("/form")
def Form():
    return render_template("form.html")

@app.route("/blogs")
def blogs():
    from red.models import Blogs, Usuarios
    blogs = Blogs.query.all()
    print(blogs)
    return render_template("blogs.html", blogs=blogs)

@app.route('/blogs/<id>/view', methods=["get", "post"])
# @login_required
def blogs_view(id):
    from red.models import Blogs, Usuarios
    # Control de permisos
    # if not current_user.is_admin():
    #     abort(404)
    frs = Blogs.query.get(id)
    if frs is None:
        abort(404)
    form = FormBlog(obj=frs)
    if form.validate_on_submit():
        form.populate_obj(frs)
        db.session.commit()
        return redirect(url_for("blogs"))
    return render_template("blogs_new.html", form=form, blog=frs, accion='vie')

@app.route('/blogs/new', methods=["get", "post"])
@login_required
def blogs_new():
    from red.models import Blogs, Usuarios
    # Control de permisos
    if not current_user.is_admin():
        abort(404)
    form = FormBlog()
    form.UsuarioId.data = current_user.id
    form.created_at.data = datetime.now()
    if form.validate_on_submit():
        frs = Blogs()
        form.populate_obj(frs)
        db.session.add(frs)
        db.session.commit()
        return redirect(url_for("blogs"))
    else:
        return render_template("blogs_new.html", form=form, blog='', accion='add')

@app.route('/blogs/<id>/edit', methods=["get", "post"])
@login_required
def blogs_edit(id):
    from red.models import Blogs, Usuarios
    # Control de permisos
    if not current_user.is_admin():
        abort(404)
    frs = Blogs.query.get(id)
    if frs is None:
        abort(404)
    form = FormBlog(obj=frs)
    if form.validate_on_submit():
        form.populate_obj(frs)
        db.session.commit()
        return redirect(url_for("blogs"))
    return render_template("blogs_new.html", form=form, blog=frs, accion='edt')

@app.route('/blogs/<id>/delete', methods=["get", "post"])
@login_required
def blogs_delete(id):
    from red.models import Blogs, Usuarios
    # Control de permisos
    if not current_user.is_admin():
        abort(404)
    frs = Blogs.query.get(id)
    if frs is None:
        abort(404)
    form = FormSINO()
    if form.validate_on_submit():
        if form.si.data:
            db.session.delete(frs)
            db.session.commit()
        return redirect(url_for("blogs"))
    return render_template("blogs_delete.html", form=form, frs=frs)

@app.route("/trilladoras/nuevo", methods=['POST'])
def nueva_trilladora():
    from red.models import Trilladoras
    tri = Trilladoras(nombre = request.json['nombre'], ubicacion = request.json['ubicacion'], telefono  = request.json['telefono'], horario   = request.json['horario'])
    # print(nombre+" " + ubicacion + " " + telefono + " " + horario)
    print(tri)
    db.session.add(tri)
    db.session.commit()
    dato = { 'res': 'ok' }
    res = json_util.dumps(dato)
    return Response(res, mimetype="application/json")

@app.route("/trilladoras/consultar", methods=['GET'])
def consultar_trilladoras():
    from red.models import Trilladoras
    # consulta = mongo.db.trilladoras.find()
    consulta = Trilladoras.query.all()
    datos = []
    for cn in consulta:
        dato = { 'nombre': cn.nombre, 'ubicacion': cn.ubicacion, 'telefono': cn.telefono, 'horario': cn.horario}
        datos.append(dato)
    res = json_util.dumps(datos)
    return Response(res, mimetype="application/json")

#@app.route("/informacion")
#def informacion():
#    return render_template("informacion.html")

@app.route("/trilladoras")
def Trilladoras():
    return render_template("trilladoras.html")

@app.route("/calculo")
def calculo():
    return render_template("calculo.html")

@app.route("/foro")
def Foro():
    return render_template("foros.html")

@app.route('/login', methods=['get', 'post'])
def login():
    from red.models import Usuarios
    # Control de permisos
    if current_user.is_authenticated:
        return redirect(url_for("inicio"))
    form = LoginForm()
    if form.validate_on_submit():
        user = Usuarios.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            next = request.args.get('next')
            return redirect(next or url_for('inicio'))
        form.username.errors.append("Usuario o contraseña incorrectas.")
    return render_template('login.html', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/registro", methods=["get", "post"])
def registro():
    from red.models import Usuarios
    # Control de permisos
    if current_user.is_authenticated:
        return redirect(url_for("inicio"))
    form = FormUsuario()
    if form.validate_on_submit():
        existe_usuario = Usuarios.query.\
            filter_by(username=form.username.data).first()
        if existe_usuario is None:
            user = Usuarios()
            form.populate_obj(user)
            user.admin = False
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("inicio"))
        form.username.errors.append("Nombre de usuario ya existe.")
    return render_template("usuarios_new.html", form=form)


@app.route('/perfil/<username>', methods=["get", "post"])
@login_required
def perfil(username):
    from red.models import Usuarios
    user = Usuarios.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    form = FormUsuario(request.form, obj=user)
    del form.password
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        return redirect(url_for("inicio"))
    return render_template("usuarios_new.html", form=form, perfil=True)


@app.route('/changepassword/<username>', methods=["get", "post"])
@login_required
def changepassword(username):
    from red.models import Usuarios
    user = Usuarios.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    form = FormChangePassword()
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        return redirect(url_for("inicio"))
    return render_template("changepassword.html", form=form)


@login_manager.user_loader
def load_user(user_id):
    from red.models import Usuarios
    return Usuarios.query.get(int(user_id))


@app.errorhandler(404)
def page_not_found(error):
    return render_template("error.html", error="Página no encontrada..."), 404
