from database.conexion import Conexion
from models.admin import Admin

class AdminDAO:

    #SELCT * from
    #==========================================================================================

    def obtener_todo(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM vista_admin")
        registros = cursor.fetchall()

        admins = []
        for registro in registros:
            admin = Admin(
                id = registro[0],
                nombre = registro[1],
                correo = registro[2]
            )
            admins.append(admin)
        cursor.close()
        conexion.close()
        return admins 
        #==========================================================================================

    def actualizar(self, admin):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        UPDATE admin
        SET nombre = %s, apellido_p = %s, apellido_m = %s, correo = %s, password = %s
        WHERE id = %s
        """
        
        cursor.execute(sql, (
                        admin.nombre,
                        admin.apellido_p,
                        admin.apellido_m,
                        admin.correo,
                        admin.password,
                        admin.id
                        ))

        conexion.commit()
        cursor.close()
        conexion.close()

    # DELATE
    #==========================================================================================

    def eliminar(self,id):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("DELETE FROM admin WHERE id = %s", (id,))

        conexion.commit()
        cursor.close()
        conexion.close()

        #==========================================================================================

    def obtener_ultimo_id(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT MAX(id) FROM admin")
        resultado = cursor.fetchone()

        cursor.close()
        conexion.close()

        if resultado[0] is None:
            return 0
        return resultado[0]