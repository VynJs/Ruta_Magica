from database.conexion import Conexion
from models.entretenimiento import Entretenimiento


class EntretenimientoDAO:
    """DAO con operaciones CRUD y búsquedas sobre entretenimiento."""

    def obtener_todo(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM vista_entretenimiento ")

        registros = cursor.fetchall()

        entretenimientos = []
        for registro in registros:
            entretenimiento = Entretenimiento(
                id = registro[0],
                nombre_entretenimeinto = registro[1],
                categoria = registro[2],
                horario_inicio = registro[3],
                horario_fin= registro[4],
                direccion= registro[5],
                latitud = registro[6],
                longitud = registro[7],
                nombre_responsable= registro[8],
                telefono= registro[9],
                correo= registro[10],
                descripcion_corta= registro[11],
                descripcion_completa= registro[12],
                caracteristica_1= registro[13],
                caracteristica_2= registro[14],
                caracteristica_3= registro[15],
                capacidad= registro[16],
                precio= registro[17],
                servicio_1= registro[18],
                servicio_2= registro[19],
                servicio_3= registro[20],
                servicio_4= registro[21],
                servicio_5= registro[22],
                recomendacion_1= registro[23],
                recomendacion_2= registro[24],
                recomendacion_3= registro[25],
                instagram= registro[26],
                facebook= registro[27],
                pagina_web= registro[28],
            )
            entretenimientos.append(entretenimiento)

        cursor.close()
        conexion.close()
        return entretenimientos
            

    def insertar(self, entretenimiento):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
            INSERT INTO entretenimiento (
                id, nombre_entretenimiento, categoria, horario_inicio, horario_fin,
                direccion, mapa, nombre_responsable, telefono, correo,
                descripcion_corta, descripcion_completa, caracteristica_1, caracteristica_2, caracteristica_3,
                capacidad, precio, servicio_1, servicio_2, servicio_3, servicio_4, servicio_5,
                recomendacion_1, recomendacion_2, recomendacion_3, recomendacion_4, instagram, facebook,
                pagina_web
            ) VALUES (
                %s, %s, %s, %s, %s, %s, POINT(%s,%s), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
        """
        cursor.execute(sql, (
            entretenimiento.id,
            entretenimiento.nombre_entretenimiento,
            entretenimiento.categoria,
            entretenimiento.horario_inicio,
            entretenimiento.horario_fin,
            entretenimiento.direccion,
            entretenimiento.latitud if entretenimiento.latitud is not None else 0,
            entretenimiento.longitud if entretenimiento.longitud is not None else 0,
            entretenimiento.nombre_responsable,
            entretenimiento.telefono,
            entretenimiento.correo,
            entretenimiento.descripcion_corta,
            entretenimiento.descripcion_completa,
            entretenimiento.caracteristica_1,
            entretenimiento.caracteristica_2,
            entretenimiento.caracteristica_3,
            entretenimiento.capacidad,
            entretenimiento.precio,
            entretenimiento.servicio_1,
            entretenimiento.servicio_2,
            entretenimiento.servicio_3,
            entretenimiento.servicio_4,
            entretenimiento.servicio_5,
            entretenimiento.recomendacion_1,
            entretenimiento.recomendacion_2,
            entretenimiento.recomendacion_3,
            entretenimiento.recomendacion_4,
            entretenimiento.instagram,
            entretenimiento.facebook,
            entretenimiento.pagina_web,
        ))
        conexion.commit()
        cursor.close()
        conexion.close()

    def actualizar(self, entretenimiento):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
            UPDATE entretenimiento SET
            nombre_entretenimiento = %s, categoria = %s, horario_inicio = %s, horario_fin = %s,
            direccion = %s, mapa = POINT(%s, %s), nombre_responsable = %s, telefono = %s, correo = %s,
            descripcion_corta = %s, descripcion_completa = %s, caracteristica_1 = %s, caracteristica_2 = %s, caracteristica_3 = %s,
            capacidad = %s, precio = %s, servicio_1 = %s, servicio_2 = %s, servicio_3 = %s, servicio_4 = %s, servicio_5 = %s,
            recomendacion_1 = %s, recomendacion_2 = %s, recomendacion_3 = %s, recomendacion_4 = %s, instagram = %s, facebook = %s,
            pagina_web = %s
            WHERE id = %s;
        """
        cursor.execute(sql, (
            entretenimiento.nombre_entretenimiento,
            entretenimiento.categoria,
            entretenimiento.horario_inicio,
            entretenimiento.horario_fin,
            entretenimiento.direccion,
            entretenimiento.latitud if entretenimiento.latitud is not None else 0,
            entretenimiento.longitud if entretenimiento.longitud is not None else 0,
            entretenimiento.nombre_responsable,
            entretenimiento.telefono,
            entretenimiento.correo,
            entretenimiento.descripcion_corta,
            entretenimiento.descripcion_completa,
            entretenimiento.caracteristica_1,
            entretenimiento.caracteristica_2,
            entretenimiento.caracteristica_3,
            entretenimiento.capacidad,
            entretenimiento.precio,
            entretenimiento.servicio_1,
            entretenimiento.servicio_2,
            entretenimiento.servicio_3,
            entretenimiento.servicio_4,
            entretenimiento.servicio_5,
            entretenimiento.recomendacion_1,
            entretenimiento.recomendacion_2,
            entretenimiento.recomendacion_3,
            entretenimiento.recomendacion_4,
            entretenimiento.instagram,
            entretenimiento.facebook,
            entretenimiento.pagina_web,
            entretenimiento.id,
        ))
        conexion.commit()
        cursor.close()
        conexion.close()

    def eliminar(self, id):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        
        cursor.execute("DELETE FROM entretenimiento WHERE id = %s;", (id,))

        conexion.commit()
        cursor.close()
        conexion.close()
    

    def buscar(self, texto):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        SELECT * FROM entretenimiento
        WHERE nombre ILIKE %s
        ORDER BY nombre
        """

        cursor.execute(sql, (f"%{texto}%",))

        registros = cursor.fetchall()

        entretenimientos = []
        for registro in registros:
            entretenimiento = Entretenimiento(
                id = registro[0],
                nombre_entretenimeinto = registro[1],
                categoria = registro[2],
                horario_inicio = registro[3],
                horario_fin= registro[4],
                direccion= registro[5],
                latitud = registro[6],
                longitud = registro[7],
                nombre_responsable= registro[8],
                telefono= registro[9],
                correo= registro[10],
                descripcion_corta= registro[11],
                descripcion_completa= registro[12],
                caracteristica_1= registro[13],
                caracteristica_2= registro[14],
                caracteristica_3= registro[15],
                capacidad= registro[16],
                precio= registro[17],
                servicio_1= registro[18],
                servicio_2= registro[19],
                servicio_3= registro[20],
                servicio_4= registro[21],
                servicio_5= registro[22],
                recomendacion_1= registro[23],
                recomendacion_2= registro[24],
                recomendacion_3= registro[25],
                instagram= registro[26],
                facebook= registro[27],
                pagina_web= registro[28],
            )
            entretenimientos.append(entretenimiento)

        cursor.close()
        conexion.close()

        return entretenimientos

    def obtener_ultimo_id(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT MAX(id) FROM entretenimiento;")
        resultado = cursor.fetchone()

        cursor.close()
        conexion.close()

        if resultado[0] is None:
            return 0
        return resultado[0]

    def cambiar_estado(self, entretenimiento):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        UPDATE entretenimiento
        SET activo = %s
        WHERE id = %s
        """

        cursor.execute(sql, (
            entretenimiento.activo,
            entretenimiento.id
    ))

        conexion.commit()
        cursor.close()
        conexion.close()