from sqlalchemy import Boolean, Column, ForeignKey
from sqlalchemy import DateTime, Integer, String, Text, Float
from sqlalchemy.orm import relationship
from red.app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date, time, timedelta

class Trilladoras(db.Model):
    """Trilladoras"""
    __tablename__ = 'trilladoras'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(60))
    ubicacion = Column(String(40))
    telefono = Column(String(30))
    horario = Column(String(30))
    
    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))
    
class Titulos(db.Model):
    """Titulos de los Foros"""
    __tablename__ = 'titulos'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100))
    foros = relationship("Foros", cascade="all, delete-orphan",
                             backref="Titulos", lazy='dynamic')

    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))

class Foros(db.Model):
    """Foros de nuestra Sitio"""
    __tablename__ = 'foros'
    id = Column(Integer, primary_key=True)
    descripcion = Column(String(255))
    created_at = db.Column(db.DateTime)
    UsuarioId = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    TituloId = Column(Integer, ForeignKey('titulos.id'), nullable=False)
    titulo = relationship("Titulos", backref="Foros")
    usuario = relationship("Usuarios", backref="Foros")
    
    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))

class Blogs(db.Model):
    """Blogs de nuestra Sitio"""
    __tablename__ = 'blogs'
    id = Column(Integer, primary_key=True)
    titulo = Column(String(100))
    descripcion = Column(String(255))
    created_at = db.Column(db.DateTime)
    UsuarioId = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    usuario = relationship("Usuarios", backref="blogs")
    
    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))
    
class Usuarios(db.Model):
    """Usuarios"""
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False)
    password_hash = Column(String(128), nullable=False)
    nombre = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False)
    admin = Column(Boolean, default=False)

    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


# Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def is_admin(self):
        return self.admin
