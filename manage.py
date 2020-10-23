from flask_script import Manager, Server
from red.app import app, db
from red.models import *
from getpass import getpass

manager = Manager(app)
app.config['DEBUG'] = True  # Ensure debugger will load.

@manager.command
def create_tables():
    "Create relational database tables."
    db.create_all()
    categoria = Titulos(id=0, nombre="Todos")
    db.session.add(categoria)
    db.session.commit()

@manager.command
def drop_tables():
    "Drop all project relational database tables. THIS DELETES DATA."
    db.drop_all()

@manager.command
def add_data_tables():
    db.create_all()
    categorias = ("Siembra", "Capachos", "Trilladoras")
    for cat in categorias:
        categoria = Titulos(nombre=cat)
        db.session.add(categoria)
        db.session.commit()

@manager.command
def create_admin():
    usuario = {"username": input("Usuario:"),
               "password": getpass("Password:"),
               "nombre": input("Nombre completo:"),
               "email": input("Email:"),
               "admin": True}
    usu = Usuarios(**usuario)
    db.session.add(usu)
    db.session.commit()

 # Turn on debugger by default and reloader 
manager.add_command("runserver", Server(
    use_debugger = True,
    use_reloader = True,
    port = '8000',
    host = '0.0.0.0') )

if __name__ == '__main__':
    manager.run()
