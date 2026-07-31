"""
dao/imagen_dao.py
--------------------
Acceso a datos para la tabla `imagenes` (galería de fotos de
establecimientos, eventos y entretenimiento). Sigue el mismo CRUD
estándar del proyecto, más algunos métodos propios de una galería:
- obtener_por_entidad(): trae todas las fotos de un registro específico.
- obtener_principal(): trae solo la foto marcada como principal.
- marcar_como_principal(): garantiza que solo haya UNA imagen principal
  por entidad (desmarca las demás dentro de la misma transacción).
- reordenar(): actualiza el orden de varias imágenes de una sola vez.
"""

from database.conexion import Conexion
from models.imagen import Imagen


class ImagenDAO:
    """DAO con operaciones CRUD y de galería sobre la tabla imagenes."""

    # ------------------------------------------------------------
    # CRUD estándar
    # ------------------------------------------------------------

    def obtener_todo(self, ):
            """Devuelve todas las imágenes registradas (uso administrativo)."""
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()

            registros = cursor.fetchall()
            
            cursor.execute("SELECT * FROM imagenes")

            imagen = []
            for registro in registros:
                imagen = Imagen(
                    id = registro[0],
                    id_establecimiento = registro[1],
                    id_entretenimiento = registro[2],
                    id_evento = registro[3],
                    url_imagen= registro[4],
                    public_id= registro[5],                  
                    admin= registro[6],
            )

            imagen.append(imagen)
            cursor.close()
            conexion.close()
            return imagen                  

    def insertar(self, imagen):
        """Inserta una nueva imagen y devuelve el id generado."""
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        sql = """
            INSERT INTO imagenes (id, id_establecimiento, id_entretenimiento, id_evento, url_imagen, publid_id, admin)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
        """

        cursor.execute(sql, (
                imagen.id, 
                imagen.id_establecimiento,
                imagen.id_entretenimiento, 
                imagen.id_evento, 
                imagen.url_imagen, 
                imagen.publid_id, 
                imagen.admin,
            ))

        conexion.commit()
        cursor.close()
        conexion.close()

    def actualizar(self, imagen):
        """Actualiza una imagen existente (url, orden o si es principal)."""
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        sql = """
            UPDATE imagenes
               SET id = %s, id_establecimiento = %s, id_entretenimiento = %s, id_evento = %s, url_imagen = %s, publid_id = %s, admin = %s)
             WHERE id = %s;
        """

        cursor.execute(sql, (
                imagen.id, 
                imagen.id_establecimiento,
                imagen.id_entretenimiento, 
                imagen.id_evento, 
                imagen.url_imagen, 
                imagen.publid_id, 
                imagen.admin,
            ))
        conexion.commit()
        cursor.close()
        conexion.close()

    def eliminar(self, id_imagen: int) -> bool:
        """Elimina una imagen por id (borra el registro, no el archivo físico)."""
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        
        cursor.execute("DELETE FROM imagenes WHERE id = %s;", (id_imagen,))

        conexion.commit()
        cursor.close()
        conexion.close()


def buscar(self, texto):
    conexion = Conexion.obtener_conexion()
    cursor = conexion.cursor()

    sql = """
    SELECT * FROM imagenes
    WHERE url ILIKE %s
    ORDER BY entidad_tipo, entidad_id, orden
    """

    cursor.execute(sql, (f"%{texto}%",))

    registros = cursor.fetchall()

    imagenes = []
    for registro in registros:
        imagen = Imagen(
            id = registro[0],
            id_establecimiento = registro[1],
            id_entretenimiento = registro[2],
            id_evento = registro[3],
            url_imagen= registro[4],
            public_id= registro[5],                  
            admin= registro[6],
        )

        imagenes.append(imagen)

    cursor.close()
    conexion.close()

    return imagenes

def obtener_ultimo_id(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        
        cursor.execute("SELECT COALESCE(MAX(id), 0) AS ultimo FROM imagenes;")
        resultado = cursor.fetchone()
        
        cursor.close()
        conexion.close()