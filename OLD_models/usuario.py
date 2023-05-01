from sqlalchemy import Column, Integer, String, ForeignKey
from flask_login import UserMixin
from werkzeug.security import check_password_hash
import db


# definicion de la clase usuarios
class User(db.Base, UserMixin):
    __tablename__ = 'users'
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True)
    username = Column(String(25), nullable=False, unique=True, index=True)
    password = Column(String(102), nullable=False)
    rol_id = Column(Integer, ForeignKey("rol.id_rol"))

    def __init__(self, id, username, password, rol_id):
        self.id=id
        self.username = username
        self.password = password
        self.rol_id = rol_id

    def __str__(self):
        print("ID:", self.id)
        print("User:", self.username)
        print("Pass:", self.password)
        print("ROL: ",self.rol_id)

        return "User P: {}-->{} -->{} -->{}".format(self.id,
                                            self.username,
                                            self.password,
                                            self.rol_id)


    '''
    @classmethod
    def check_password(self,hashed_password,password):
        print (hashed_password)
        print(password)
        return check_password_hash(hashed_password,password)
    '''
    @classmethod
    def login(self,db,user):
        print ("imprimoDB:",db)
        print("----111------------->", user, db)
        print("user.username y password", user.username, user.password, db)

        #query=db.session.query(User).filter_by(username=user.username).first()
        #print("QUery montada:\n",query)


        try:
            resultado = db.session.query(User).filter_by(username=user.username).first()

            print("Este es el resultado", resultado)

            if resultado != None:
                #validamos hash para comprobar la password
                check=check_password_hash(resultado.password,user.password)
                print (check)
                usuario=User(resultado.id,resultado.username,check,resultado.rol_id)
                print("Usuario query:", usuario)
                return usuario
            else:
                return None
        except Exception as ex:
            raise Exception(ex)


    @classmethod
    def get_by_id(self, db, id):
        print("entro en GET BY ID", id)



        try:
            query = db.session.query(User).filter_by(id=id).first()
            #cursor = db.connection.cursor()
            #sql = "SELECT id, username FROM user WHERE id='{}'".format(user.id)
            print ("******************************************", query)

            if query != None:
                print ("query get id es true")
                print("ID------------------>",query.id)
                print(query.rol_id)
                print(query.username)

                usuario = User(query.id, query.username,query.password,query.rol_id)
                return usuario
            else:
                return None
        except Exception as ex:
            raise Exception(ex)



# añadimos el usuario administrador el cual debe tener el id_rol=1
def addAdmin():
    user_admin = User("Administrador",
                      "password_administrator",
                      rol_id=1)
    db.session.add(user_admin)
    db.session.commit()
    db.session.close()
