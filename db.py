# import
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

#file_path = os.path.abspath(os.getcwd())+"\lionstock.db"

# sqlite://<nohostname>/<path>
# where <path> is relative:
engine = create_engine('sqlite:///database/lionstock.db', connect_args={'check_same_thread': False})

# sesion
Session = sessionmaker(bind=engine)
session = Session()
# es la forma de instanciar la clase Session, session (minuscula) es como voy a referenciarla

# vinculación         (al ORM le decimos que debe transformar clases en tablas)
#                      en el fichero models.py en las clases donde queramos que se transformen en tablas, le
#                       añadiremos esta variable, y esto se encargará de mapear y vincular la clase a la tabla


Base = declarative_base()