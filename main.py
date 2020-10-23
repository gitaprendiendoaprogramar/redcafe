from flask_script import Manager, Server
from red import run
from red.models import *
from getpass import getpass

app = run.create_app()
manager = Manager(app)

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
    host = '0.0.0.0') )

if __name__ == '__main__':
    manager.run()