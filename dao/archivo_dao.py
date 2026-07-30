from database.conexion import Conexion
from models.archivo import Archivo

class ArchivoDAO:

    #SELCT * from
    #==========================================================================================

    def obtener_todo(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM vista_archivo")
        registros = cursor.fetchall()

        archivos = []
        for registro in registros:
            archivo = Archivo(
                id = registro[0],
                id_establecimiento= registro[1],
                id_entretenimiento=  registro[2],
                id_evento=  registro[3],
                nombre_archivo= registro[4],
                extencion= registro[5],
                tipo_archivo= registro[6],
                url_archivo= registro[7],
                public_id= registro[8],
                fecha_subida= registro[9]
            )
            archivos.append(archivo)
        cursor.close()
        conexion.close()
        return archivos 
    
    #==========================================================================================
    
    def insertar(self, archivo):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        INSERT INTO archivo(id, id_establecimiento, id_entretenimiento, id_evento, nombre_archivo, extencion, tipo_archivo, url_archivo, public_id, fecha_subida)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(sql, (
            archivo.id,
            archivo.id_establecimiento,
            archivo.id_entretenimiento,
            archivo.id_evento,
            archivo.nombre_archivo,
            archivo.extencion,
            archivo.tipo_archivo,
            archivo.url_archivo,
            archivo.public_id,
            archivo.fecha_subida
        ))

        conexion.commit()
        cursor.close()
        conexion.close()

        #UPDATE
        #==========================================================================================

    def actualizar(self, archivo):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        UPDATE admin
        SET id_establecimiento = %s, id_entretenimiento = %s, id_evento = %s, nombre_archivo = %s, extencion = %s, tipo_archivo = %s, url_archivo = %s, public_id = %s, fecha_subida = %s
        WHERE id = %s
        """
        
        cursor.execute(sql, (
                        archivo.id_establecimiento,
                        archivo.id_entretenimiento,
                        archivo.id_evento,
                        archivo.nombre_archivo,
                        archivo.extencion,
                        archivo.tipo_archivo,
                        archivo.url_archivo,
                        archivo.public_id,
                        archivo.fecha_subida,
                        archivo.id
                        ))

        conexion.commit()
        cursor.close()
        conexion.close()

    # DELATE
    #==========================================================================================

    def eliminar(self,id):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("DELETE FROM archivo WHERE id = %s", (id,))

        conexion.commit()
        cursor.close()
        conexion.close()

        #==========================================================================================

    def obtener_ultimo_id(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT MAX(id) FROM archivo")
        resultado = cursor.fetchone()

        cursor.close()
        conexion.close()

        if resultado[0] is None:
            return 0
        return resultado[0]