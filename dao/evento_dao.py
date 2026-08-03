from database.conexion import Conexion
from models.evento import Evento
from psycopg2.extras import Json

class EventoDAO:

    #SELCT * from
    #==========================================================================================

    def obtener_todo(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM vista_evento")
        registros = cursor.fetchall()

        eventos = []
        for registro in registros:
            evento = Evento(
                id = registro[0],
                nombre_evento= registro[1],
                categoria = registro[2],
                fecha = registro[3],
                horario_inicio= registro[4],
                horario_fin= registro[5],
                ubicacion= registro[6],
                latitud = registro[7],
                longitud = registro[8],
                nombre_organizador= registro[9],
                edad= registro[10],
                telefono = registro[11],
                correo = registro[12],
                descripcion_corta = registro[13],
                descripcion_completa = registro[14],
                caracteristica_1 = registro[15],
                caracteristica_2 = registro[16],
                caracteristica_3 = registro[17],
                instagram = registro[18],
                facebook = registro[19],
                pagina_web = registro[20],
                estado = registro[21],
                datos_destacados = registro[22]

            )
            eventos.append(evento)

        cursor.close()
        conexion.close()
        return eventos
    
    #==========================================================================================

    def insertar(self, evento):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        INSERT INTO evento (
        id, nombre_evento, categoria, fecha, hora_inicio, hora_fin, ubicacion, mapa,
        nombre_organizador, edad, telefono, correo, descripcion_corta, 
        descripcion_completa, caracteristica_1, caracteristica_2, caracteristica_3, instagram,
        facebook, pagina_web, estado, datos_destacados) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, POINT(%s,%s), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s ) 
        """
        cursor.execute(sql, (
            evento.id,
            evento.nombre_evento,
            evento.categoria,
            evento.fecha,
            evento.horario_inicio,
            evento.horario_fin,
            evento.ubicacion,
            evento.longitud,
            evento.latitud,
            evento.nombre_organizador,
            evento.edad,
            evento.telefono,
            evento.correo,
            evento.descripcion_corta,
            evento.descripcion_completa,
            evento.caracteristica_1,
            evento.caracteristica_2,
            evento.caracteristica_3,
            evento.instagram,
            evento.facebook,
            evento.pagina_web,
            evento.estado,
            Json(evento.datos_destacados)
        ))

        conexion.commit()
        cursor.close()
        conexion.close()

    #==========================================================================================

    def actualizar(self, evento):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
            UPDATE evento SET
            nombre_evento = %s, categoria = %s, fecha = %s, hora_inicio = %s, hora_fin = %s, ubicacion = %s, mapa = POINT(%s, %s),
            nombre_organizador = %s, edad = %s, telefono = %s, correo = %s, descripcion_corta = %s, 
            descripcion_completa = %s, caracteristica_1 = %s, caracteristica_2 = %s, caracteristica_3 = %s, instagram = %s,
            facebook = %s, pagina_web = %s, estado = %s, datos_destacados = %s
            WHERE id = %s;
        """
        cursor.execute(sql, (
                        evento.id,
                        evento.nombre_evento,
                        evento.categoria,
                        evento.fecha,
                        evento.horario_inicio,
                        evento.horario_fin,
                        evento.ubicacion,
                        evento.longitud,
                        evento.nombre_organizador,
                        evento.edad,
                        evento.telefono,
                        evento.correo,
                        evento.descripcion_corta,
                        evento.descripcion_completa,
                        evento.caracteristica_1,
                        evento.caracteristica_2,
                        evento.caracteristica_3,
                        evento.instagram,
                        evento.facebook,
                        evento.pagina_web,
                        evento.estado,
                        Json(evento.datos_destacados)
                        ))

        conexion.commit()
        cursor.close()
        conexion.close()

    #==========================================================================================

    def eliminar(self,id):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("DELETE FROM evento WHERE id = %s", (id,))

        conexion.commit()
        cursor.close()
        conexion.close()

    #==========================================================================================
    
    def obtener_ultimo_id(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT MAX(id) FROM evento")
        resultado = cursor.fetchone()

        cursor.close()
        conexion.close()

        if resultado[0] is None:
            return 0
        return resultado[0]

    #==========================================================================================

        #BUSCAR
    #==========================================================================================

    def buscar(self, texto):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        SELECT * FROM evento
        WHERE nombre ILIKE %s
        ORDER BY nombre
        """

        cursor.execute(sql, (f"%{texto}%",))

        registros = cursor.fetchall()

        eventos = []
        for registro in registros:
            evento = Evento(
                id = registro[0],
                nombre_evento= registro[1],
                categoria = registro[2],
                fecha = registro[3],
                horario_inicio= registro[4],
                horario_fin= registro[5],
                ubicacion= registro[6],
                latitud = registro[7],
                longitud = registro[8],
                nombre_organizador= registro[9],
                edad= registro[10],
                telefono = registro[11],
                correo = registro[12],
                descripcion_corta = registro[13],
                descripcion_completa = registro[14],
                caracteristica_1 = registro[15],
                caracteristica_2 = registro[16],
                caracteristica_3 = registro[17],
                instagram = registro[18],
                facebook = registro[19],
                pagina_web = registro[20],
                estado = registro[21],
                datos_destacados = registro[22]

            )
            eventos.append(evento)

        cursor.close()
        conexion.close()

        return eventos
    
    #ESTADO
    #==========================================================================================
    def cambiar_estado(self, evento):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        UPDATE evento
        SET activo = %s
        WHERE id = %s
        """

        cursor.execute(sql, (
                        evento.estado,
                        evento.id
        ))

        conexion.commit()
        cursor.close()
        conexion.close()