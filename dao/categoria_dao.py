from database.conexion import Conexion
from models.categoria import Categoria


class CategoriaDAO:

    #SELCT * from
    #==========================================================================================
    
    def obtener_todo(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM vista_categoria")
        registros = cursor.fetchall()

        categorias = []
        for registro in registros:
            categoria = Categoria(
                id = registro[0],
                nombre= registro[1],
                tipo_categoria = registro[2],
                descripcion = registro[3],
                estado= registro[4]
            )
            categorias.append(categoria)
        cursor.close()
        conexion.close()
        return categorias 

    #==========================================================================================

    def insertar(self, categoria):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
            INSERT INTO categoria(id, nombre, tipo_categoria, descripcion, estado)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (
            categoria.id,
            categoria.nombre,
            categoria.tipo_categoria,
            categoria.descripcion,
            categoria.estado
        ))

        conexion.commit()
        cursor.close()
        conexion.close()

    #UPDATE
    #==========================================================================================

    def actualizar(self, categoria):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        UPDATE categoria
        SET nombre = %s, tipo_categoria = %s, descripcion = %s, estado = %s
        WHERE id = %s;
        """
        cursor.execute(sql, (
                        categoria.nombre,
                        categoria.tipo_categoria,
                        categoria.descripcion,
                        categoria.estado,
                        categoria.id
                        ))

        conexion.commit()
        cursor.close()
        conexion.close()

    # DELATE
    #==========================================================================================

    def eliminar(self, id):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("DELETE FROM categoria WHERE id = %s", (id,))

        conexion.commit()
        cursor.close()
        conexion.close()

    #==========================================================================================
    
    def obtener_ultimo_id(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT MAX(id) FROM categoria")
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
        SELECT * FROM categoria
        WHERE nombre ILIKE %s
        ORDER BY nombre
        """

        cursor.execute(sql, (f"%{texto}%",))

        registros = cursor.fetchall()

        categorias = []
        for registro in registros:
            categoria = Categoria(
                id=registro[0],
                nombre=registro[1],
                tipo_categoria=registro[2],
                descripcion=registro[3],
                estado=registro[4]
            )
            categorias.append(categoria)

        cursor.close()
        conexion.close()

        return categorias
    
    #ESTADO
    #==========================================================================================
    def cambiar_estado(self, categoria):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        UPDATE categoria
        SET activo = %s
        WHERE id = %s
        """

        cursor.execute(sql, (
                        categoria.estado,
                        categoria.id
        ))

        conexion.commit()
        cursor.close()
        conexion.close()