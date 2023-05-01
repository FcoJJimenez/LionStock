from sqlalchemy import Column, Integer, String
import db


# print (generate_password_hash(""))

class Rol(db.Base):
    __tablename__ = 'rol'
    __table_args__ = {'sqlite_autoincrement': True}
    id_rol = Column(Integer, primary_key=True)
    descripcion = Column(String(50), unique=True)

    def __init__(self, id_rol,descripcion):
        self.id_rol= id_rol
        self.descripcion = descripcion

    def __str__(self):
        return "Rol: -->{} -->{} ".format(self.id_rol, self.descripcion)


    @classmethod
    def get_rol(self,id):
        try:
            resultado = db.session.query(Rol).filter_by(id_rol=id).first()
            print("Consulta de ID", resultado)
            if resultado != None:
                return resultado.descripcion
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

