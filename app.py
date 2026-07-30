from dao.admin_dao import AdminDAO
from models.admin import Admin
from dao.archivo_dao import ArchivoDAO
from models.archivo import Archivo
from dao.categoria_dao import CategoriaDAO
from models.categoria import Categoria

#==========================================================================================
#==========================================================================================

#ADMINISTRADORES

def ver_admins():
    try:
        admin_dao = AdminDAO()
        admins = admin_dao.obtener_todo()

        if len(admins) == 0:
            print("No hay administradores registrados")
        else:
            for admin in admins:
                print (f"| {admin.id} | {admin.nombre} | {admin.correo} |")
        print("\n Conexion esxitosa con la base de datos")

    except Exception as e:
        print("Existe un error")
        print(e)

#==========================================================================================

def actualizar_admin():
    try:
        admin_dao = AdminDAO()
        print("Lista de administradores disponibles")
        ver_admins()
        id = int(input("Seleccione el id del administrador a actualizar"))
        nombre = input("Escribe el nombre del administrador:")
        apellido_p = input("Escribe el apellido paterno:")
        apellido_m = input("Escribe el apellido materno:")
        correo = input("Escribe correo electronico:")
        password = input("Escribe la contraseña:")
        admin = Admin(id, nombre, apellido_p, apellido_m, correo, password)
        admin_dao.actualizar(admin)
        print("El administrador fue actualizado con exito")
    except Exception as e:
        print("Error al actualizar el administrador")
        print(e)

#==========================================================================================

def eliminar_admin():
    try:
        admin_dao = AdminDAO()
        print("Lista de administradores disponibles")
        ver_admins()
        id = int(input("Escribe el id del administrador a eliminar:"))
        admin_dao.eliminar(id)
        print(f"El administrador {id} ha sido eliminado con exito")
    except Exception as e:
        print(f"Error al aliminar el administrador {id}")
        print(e)


#==========================================================================================
#==========================================================================================

#ARCHIVOS

def ver_archivos():
    try:
        archivo_dao = ArchivoDAO()
        archivos = archivo_dao.obtener_todo()

        if len(archivos) == 0:
            print("No hay archivos registrados")
        else:
            for archivo in archivos:
                print (f"| {archivo.id} | {archivo.id_establecimiento} | {archivo.id_entretenimiento} | {archivo.id_evento} | {archivo.nombre_archivo} | {archivo.extencion} | {archivo.tipo_archivo} | {archivo.url_archivo} | {archivo.public_id} | {archivo.fecha_subida} ")
        print("\n Conexion exitosa con la base de datos")

    except Exception as e:
        print("Existe un error")
        print(e)

#==========================================================================================
    
def insertar_archivos():
    print("INSERTAR UN NUVEO archivo")
    print("Escribe -- si tu id no pertenece al establecimiento, entretenimiento o evento")
    print("Escoje 1 establecimiento, entretenimiento o evento")
    id_establecimiento = int(input("Escribe el id al un establecimiento al que pertenece:"))
    id_entretenimiento = int(input("Escribe el id al entretenimiento al que pertenece:"))
    id_evento = int(input("Escribe el id al evento al que pertenece:"))
    nombre_archivo = input("Escribe el nombre del archivo:")
    extencion = input("Escribe la abreviaturas de la extencion del archivo (JPG, PDF, PNG, WORD, ect.):")
    tipo_archivo = input("Escribe el tipo del archivo (INE, PERMISO, CARTA RESPONSIVA, etc.):")
    url_archivo = input("Escribe el url o ruta del archivo:")
    public_id = input("Escribe el public_id del archivo:")
    fecha_subida = input("Escribe la fecha de hoy:")
    
    try:
        archivo_dao = ArchivoDAO()
        ultimo_id = archivo_dao.obtener_ultimo_id() + 1
        archivo = Archivo(ultimo_id, id_entretenimiento, id_establecimiento, id_evento, nombre_archivo, extencion, tipo_archivo, url_archivo, public_id, fecha_subida)
        archivo_dao.insertar(archivo)
        print("Insercion del nuevo archivo fue existosa")
    except Exception as e:
        print("Error al insertar el archivo")
        print(e)

#==========================================================================================

def actualizar_archivo():
    try:

        archivo_dao = ArchivoDAO()
        print("Lista de archivos disponibles")
        ver_archivos()
        id = int(input("Seleccione el id del archivo a actualizar"))
        id_establecimiento = int(input("Escribe el id al un establecimiento al que pertenece:"))
        id_entretenimiento = int(input("Escribe el id al entretenimiento al que pertenece:"))
        id_evento = int(input("Escribe el id al evento al que pertenece:"))
        nombre_archivo = input("Escribe el nombre del archivo:")
        extencion = input("Escribe la abreviaturas de la extencion del archivo (JPG, PDF, PNG, WORD, ect.):")
        tipo_archivo = input("Escribe el tipo del archivo (INE, PERMISO, CARTA RESPONSIVA, etc.):")
        url_archivo = input("Escribe el url o ruta del archivo:")
        fecha_subida = input("Escribe la fecha de hoy:")
        archivo = Archivo(id, id_entretenimiento, id_establecimiento, id_evento, nombre_archivo, extencion, tipo_archivo, url_archivo, fecha_subida)
        archivo_dao.actualizar(archivo)
        print("El archivo fue actualizado con exito")
    except Exception as e:
        print("Error al actualizar el archivo")
        print(e)

    #==========================================================================================

def eliminar_archivo():
    try:
        archivo_dao = ArchivoDAO()
        print("Lista de archivos disponibles")
        ver_archivos()
        id = int(input("Escribe el id del archivo a eliminar:"))
        archivo_dao.eliminar(id)
        print(f"El archivo {id} ha sido eliminado con exito")
    except Exception as e:
        print(f"Error al eliminar el archivo {id}")
        print(e)

#==========================================================================================
#==========================================================================================

#CATEGORIAS

def ver_categorias():
    try:
        categoria_dao = CategoriaDAO()
        categorias = categoria_dao.obtener_todo()

        if len(categorias) == 0:
            print("No hay categorias registradas")
        else:
            for categoria in categorias:
                print (f"| {categoria.id} | {categoria.nombre} | {categoria.tipo_categoria} | {categoria.descripcion} | {categoria.estado} | ")
        print("\n Conexion esxitosa con la base de datos")

    except Exception as e:
        print("Existe un error")
        print(e)

#==========================================================================================

def insertar_categorias():
    print("INSERTAR UNA NUEVA CATEGORIA")
    nombre = input("Escribe el mombre de la categoria:")
    tipo_categoria = input("Escribe el tipo de categoria:")
    descripcion = input("Escribe una breve descripcion sobre esta categoria:")
    estado = input("Escribe el estado de la categoria:")
    try:
        categoria_dao = CategoriaDAO()
        ultimo_id = categoria_dao.obtener_ultimo_id() + 1
        categoria = Categoria(ultimo_id, nombre, tipo_categoria, descripcion, estado)
        categoria_dao.insertar(categoria)
        print("Insercion de la nueva categoria fue existosa")
    except Exception as e:
        print("Error al insertar la categoria")
        print(e)

#==========================================================================================

def actualizar_categoria():
    try:
        categoria_dao = CategoriaDAO()
        print("Lista de categorias disponibles")
        ver_categorias()
        id = int(input("Seleccione el id de la categoria a actualizar"))
        nombre = input("Escribe el nombre de la categoria:")
        tipo_categoria = input("Escribe el tipo de categoria:")
        descripcion = input("Escribe una breve descripcion de la categoria:")
        estado = input("Escribe correo electronico:")
        categoria = Categoria(id, nombre, tipo_categoria, descripcion, estado)
        categoria_dao.actualizar(categoria)
        print("La categoria fue actualizada con exito")
    except Exception as e:
        print("Error al actualizar la categoria")
        print(e)

#==========================================================================================

def eliminar_categoria():
    try:
        categoria_dao = CategoriaDAO()
        print("Lista de categorias disponibles")
        ver_categorias()
        id = int(input("Escribe el id de la categoria a eliminar:"))
        categoria_dao.eliminar(id)
        print(f"La categoria {id} ha sido eliminada con exito")
    except Exception as e:
        print(f"Error al aliminar la categoria {id}")
        print(e)


#==========================================================================================
    #MENUS
#==========================================================================================
def menu_Admin():
    print("1. ver administradores")
    print("2. Actualizar administradores")
    print("3. Eliminar administradores")
    
    opcion = int(input("Selecciona una opcion (1-9):"))

    match opcion:
        case 1:
            ver_admins()
        case 2:
            actualizar_admin()
        case 3:
            eliminar_admin()
        

#==========================================================================================

def menu_archivos():
    print("1. Ver archivos")
    print("2. Insertar archivo")
    print("3. Actualizar archivos")
    print("4. Eliminar archivos")
    opcion = int(input("Selecciona una opcion (1-4):"))

    match opcion:
        case 1:
            ver_archivos()
        case 2:
            insertar_archivos()
        case 3:
            actualizar_archivo()
        case 4:
            eliminar_archivo()

#==========================================================================================

def menu_categorias():
    print("1. Ver categorias")
    print("2. Insertar categoria")
    print("3. Actualizar categorias")
    print("4. Eliminar categorias")
    opcion = int(input("Selecciona una opcion (1-4):"))

    match opcion:
        case 1:
            ver_categorias()
        case 2:
            insertar_categorias()
        case 3:
            actualizar_categoria()
        case 4:
            eliminar_categoria()

#==========================================================================================

def main():
    print("=== Menu Ruta Magica ===")
    print("Menu de opciones:")
    print("1. Establecimientos")
    print("2. Entretenimiento")
    print("3. Evento")
    print("4. Administradores")
    print("5. Archivos")
    print("6. Categorias")
    print("7. Imagenes")
    opcion = int(input("Escribe tu opcion: "))
    match opcion:
        case 4: menu_Admin()
        case 5: menu_archivos()
        case 6: menu_categorias()

    print("Saliendo del sistema de Ruta Magica ....")


if __name__ == "__main__":
    main()