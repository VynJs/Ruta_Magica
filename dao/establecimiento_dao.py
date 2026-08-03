from database.conexion import Conexion
from models.establecimiento import Establecimiento
from psycopg2.extras import Json
class EstablecimientoDAO:

 #SELCT * from
 # #==========================================================================================

    def obtener_todo(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM vista_establecimeinto")
        registros = cursor.fetchall()

        establecimientos = []
        for registro in registros:
            establecimiento = Establecimiento(
                id = registro[0],
                nombre_establecimiento = registro[1],
                categoria = registro[2],
                horario_inicio = registro[3],
                horario_fin= registro[4],
                direccion= registro[5],
                latitud = registro[6],
                longitud = registro[7],
                nombre_propietario= registro[8],
                edad= registro[9],
                telefono= registro[10],
                correo= registro[11],
                descripcion_corta= registro[12],
                descripcion_completa= registro[13],
                caracteristica_1= registro[14],
                caracteristica_2= registro[15],
                caracteristica_3= registro[16],
                instagram= registro[17],
                facebook= registro[18],
                pagina_web= registro[19],
                estado= registro[20],
                servicios= registro[21],
                rango_precios= registro[22],
                productos_ofrecer= registro[23]

            )
            establecimientos.append(establecimiento)
        cursor.close()
        conexion.close()
        return establecimientos
    
    #==========================================================================================

    def insertar(self, establecimiento):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        INSERT INTO establecimiento (
        nombre_establecimiento, categoria, horario_inicio, horario_fin, direccion, mapa, 
        nombre_propietario, edad, telefono, correo, descripcion_corta, descripcion_completa,
        caracteristica_1, caracteristica_2, caracteristica_3, instagram, facebook,
        pagina_web, estado, servicios, rango_precios, productos_ofrecer)
        VALUES ( %s, %s, %s, %s, %s, POINT(%s,%s), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(sql, (
            establecimiento.id,
            establecimiento.nombre_establecimiento,
            establecimiento.categoria,
            establecimiento.horario_inicio,
            establecimiento.horario_fin,
            establecimiento.direccion,
            establecimiento.longitud,
            establecimiento.latitud,
            establecimiento.nombre_propietario,
            establecimiento.edad,
            establecimiento.telefono,
            establecimiento.correo,
            establecimiento.descripcion_corta,
            establecimiento.descripcion_completa,
            establecimiento.caracteristica_1,
            establecimiento.caracteristica_2,
            establecimiento.caracteristica_3,
            establecimiento.instagram,
            establecimiento.facebook,
            establecimiento.pagina_web,
            establecimiento.estado,
            establecimiento.servicios,
            establecimiento.rango_precios,
            Json(establecimiento.productos_ofrecer)

        ))

        conexion.commit()
        cursor.close()
        conexion.close()

        #UPDATE
        #==========================================================================================


    def actualizar(self, establecimiento):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
            UPDATE establecimiento SET
            nombre_establecimiento = %s, categoria = %s, horario_inicio = %s, horario_fin = %s, direccion = %s, mapa = POINT(%s, %s), 
            nombre_propietario = %s, edad, telefono = %s, correo = %s, descripcion_corta = %s, descripcion_completa = %s,
            caracteristica_1 = %s, caracteristica_2 = %s, caracteristica_3 = %s, instagram = %s, facebook = %s,
            pagina_web, estado = %s, servicios = %s, rango_precios = %s, productos_ofrecer = %s,
            WHERE id = %s
        """
        cursor.execute(sql, (
                        establecimiento.id,
                        establecimiento.nombre_establecimiento,
                        establecimiento.categoria,
                        establecimiento.horario_inicio,
                        establecimiento.horario_fin,
                        establecimiento.direccion,
                        establecimiento.longitud,
                        establecimiento.latitud,
                        establecimiento.nombre_propietario,
                        establecimiento.edad,
                        establecimiento.telefono,
                        establecimiento.correo,
                        establecimiento.descripcion_corta,
                        establecimiento.descripcion_completa,
                        establecimiento.caracteristica_1,
                        establecimiento.caracteristica_2,
                        establecimiento.caracteristica_3,
                        establecimiento.instagram,
                        establecimiento.facebook,
                        establecimiento.pagina_web,
                        establecimiento.estado,
                        establecimiento.servicios,
                        establecimiento.rango_precios,
                        Json(establecimiento.productos_ofrecer)
                        ))

        conexion.commit()
        cursor.close()
        conexion.close()

    # DELATE
    #==========================================================================================


    def eliminar(self,id):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("DELETE FROM establecimiento WHERE id = %s", (id,))

        conexion.commit()
        cursor.close()
        conexion.close()

    #==========================================================================================
    def obtener_ultimo_id(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT MAX(id) FROM establecimiento")
        resultado = cursor.fetchone()

        cursor.close()
        conexion.close()

        if resultado[0] is None:
            return 0
        return resultado[0]

    #BUSCAR
    #==========================================================================================

    def buscar(self, texto):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        SELECT * FROM establecimientos
        WHERE nombre ILIKE %s
        ORDER BY nombre
        """

        cursor.execute(sql, (f"%{texto}%",))

        registros = cursor.fetchall()

        establecimientos = []
        for registro in registros:
            Establecimiento = Establecimiento(
                id = registro[0],
                nombre_establecimiento = registro[1],
                categoria = registro[2],
                horario_inicio = registro[3],
                horario_fin= registro[4],
                direccion= registro[5],
                latitud = registro[6],
                longitud = registro[7],
                nombre_propietario= registro[8],
                edad= registro[9],
                telefono= registro[10],
                correo= registro[11],
                descripcion_corta= registro[12],
                descripcion_completa= registro[13],
                caracteristica_1= registro[14],
                caracteristica_2= registro[15],
                caracteristica_3= registro[16],
                instagram= registro[17],
                facebook= registro[18],
                pagina_web= registro[19],
                estado= registro[20],
                servicios= registro[21],
                rango_precios= registro[22],
                productos_ofrecer= registro[23]
            )
            establecimientos.append(Establecimiento)

        cursor.close()
        conexion.close()

        return establecimientos
    
    #ESTADO
    #==========================================================================================
    def cambiar_estado(self, establecimiento):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        UPDATE establecimiento
        SET activo = %s
        WHERE id = %s
        """

        cursor.execute(sql, (
                        establecimiento.estado,
                        establecimiento.id
        ))

        conexion.commit()
        cursor.close()
        conexion.close()