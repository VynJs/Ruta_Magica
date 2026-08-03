from database.conexion import Conexion
from models.imagen import Imagen


class ImagenDAO:

    def obtener_todo(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        try:
            # Primero se ejecuta la consulta y después fetchall()
            cursor.execute("""
                SELECT
                    id,
                    id_establecimiento,
                    id_entretenimiento,
                    id_evento,
                    url_imagen,
                    public_id,
                    admin
                FROM imagenes
                ORDER BY id;
            """)

            registros = cursor.fetchall()
            imagenes = []

            for registro in registros:
                imagen = Imagen(
                    id=registro[0],
                    id_establecimiento=registro[1],
                    id_entretenimiento=registro[2],
                    id_evento=registro[3],
                    url_imagen=registro[4],
                    public_id=registro[5],
                    admin=registro[6],
                )

                imagenes.append(imagen)

            return imagenes

        finally:
            cursor.close()
            conexion.close()

    def insertar(self, imagen):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
            INSERT INTO imagenes (
                id,
                id_establecimiento,
                id_entretenimiento,
                id_evento,
                url_imagen,
                public_id,
                admin
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
        """

        try:
            cursor.execute(
                sql,
                (
                    imagen.id,
                    imagen.id_establecimiento,
                    imagen.id_entretenimiento,
                    imagen.id_evento,
                    imagen.url_imagen,
                    imagen.public_id,
                    imagen.admin,
                ),
            )

            id_insertado = cursor.fetchone()[0]
            conexion.commit()

            return id_insertado

        except Exception:
            conexion.rollback()
            raise

        finally:
            cursor.close()
            conexion.close()

    def actualizar(self, imagen):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
            UPDATE imagenes
            SET
                id_establecimiento = %s,
                id_entretenimiento = %s,
                id_evento = %s,
                url_imagen = %s,
                public_id = %s,
                admin = %s
            WHERE id = %s;
        """

        try:
            cursor.execute(
                sql,
                (
                    imagen.id_establecimiento,
                    imagen.id_entretenimiento,
                    imagen.id_evento,
                    imagen.url_imagen,
                    imagen.public_id,
                    imagen.admin,
                    imagen.id,
                ),
            )

            conexion.commit()
            return cursor.rowcount > 0

        except Exception:
            conexion.rollback()
            raise

        finally:
            cursor.close()
            conexion.close()

    def eliminar(self, id_imagen):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        try:
            cursor.execute(
                "DELETE FROM imagenes WHERE id = %s;",
                (id_imagen,),
            )

            conexion.commit()
            return cursor.rowcount > 0

        except Exception:
            conexion.rollback()
            raise

        finally:
            cursor.close()
            conexion.close()

    def buscar(self, texto):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
            SELECT
                id,
                id_establecimiento,
                id_entretenimiento,
                id_evento,
                url_imagen,
                public_id,
                admin
            FROM imagenes
            WHERE url_imagen ILIKE %s
            ORDER BY id;
        """

        try:
            cursor.execute(sql, (f"%{texto}%",))
            registros = cursor.fetchall()

            imagenes = []

            for registro in registros:
                imagen = Imagen(
                    id=registro[0],
                    id_establecimiento=registro[1],
                    id_entretenimiento=registro[2],
                    id_evento=registro[3],
                    url_imagen=registro[4],
                    public_id=registro[5]
                )

                imagenes.append(imagen)

            return imagenes

        finally:
            cursor.close()
            conexion.close()

    def obtener_ultimo_id(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        try:
            cursor.execute("""
                SELECT COALESCE(MAX(id), 0)
                FROM imagenes;
            """)

            resultado = cursor.fetchone()
            return resultado[0]

        finally:
            cursor.close()
            conexion.close()