import os #  permite acceder a funcionalidades dependientes del Sistema Operativo
# CONFUGURACION DE CLAVES


SECRET_KEY = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT' # clave encriptada 
PWD = os.path.abspath(os.curdir) # Devulve una version normalizada de la ruta
# os.curdir es el componene de la ruta que hace referencia al directorio actual.....

DEBUG = True # que este reciviendo cambios... 
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}/dbase.db'.format(PWD) # Es el URI de la base que se usa para la conexíon, con el sistema.
SQLALCHEMY_TRACK_MODIFICATIONS = False # Si se estavblece True ratreara la modificaciones de los objectos y emitira señales
