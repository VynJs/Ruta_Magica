from dao.admin_dao import AdminDAO
from models.admin import Admin
from dao.archivo_dao import ArchivoDAO
from models.archivo import Archivo
from dao.categoria_dao import CategoriaDAO
from models.categoria import Categoria
from dao.establecimiento_dao import EstablecimientoDAO
from models.establecimiento import Establecimiento
from dao.entretenimiento_dao import EntretenimientoDAO
from models.entretenimiento import Entretenimiento
from dao.evento_dao import EventoDAO
from models.evento import Evento
from dao.imagen_dao import ImagenDAO
from models.imagen import Imagen
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
        print("\n Conexión exitosa con la base de datos")

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
        correo = input("Escribe correo electrónico:")
        password = input("Escribe la contraseña:")
        admin = Admin(id, nombre, apellido_p, apellido_m, correo, password)
        admin_dao.actualizar(admin)
        print("El administrador fue actualizado con éxito")
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
        print(f"El administrador {id} ha sido eliminado con éxito")
    except Exception as e:
        print(f"Error al eliminar el administrador {id}")
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
        print("\n Conexión exitosa con la base de datos")

    except Exception as e:
        print("Existe un error")
        print(e)

#==========================================================================================
    
def insertar_archivos():
    print("Insertar un nuevo archivo")
    print("Escribe -- si tu id no pertenece al establecimiento, entretenimiento o evento")
    print("Escoje 1 establecimiento, entretenimiento o evento")
    id_establecimiento = int(input("Escribe el id al un establecimiento al que pertenece:"))
    id_entretenimiento = int(input("Escribe el id al entretenimiento al que pertenece:"))
    id_evento = int(input("Escribe el id al evento al que pertenece:"))
    nombre_archivo = input("Escribe el nombre del archivo:")
    extencion = input("Escribe la abreviaturas de la extención del archivo (JPG, PDF, PNG, WORD, ect.):")
    tipo_archivo = input("Escribe el tipo del archivo (INE, PERMISO, CARTA RESPONSIVA, etc.):")
    url_archivo = input("Escribe el url o ruta del archivo:")
    public_id = input("Escribe el public_id del archivo:")
    fecha_subida = input("Escribe la fecha de hoy:")
    
    try:
        archivo_dao = ArchivoDAO()
        ultimo_id = archivo_dao.obtener_ultimo_id() + 1
        archivo = Archivo(ultimo_id, id_entretenimiento, id_establecimiento, id_evento, nombre_archivo, extencion, tipo_archivo, url_archivo, public_id, fecha_subida)
        archivo_dao.insertar(archivo)
        print("Inserción del nuevo archivo fue existosa")
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
        extencion = input("Escribe la abreviaturas de la extención del archivo (JPG, PDF, PNG, WORD, ect.):")
        tipo_archivo = input("Escribe el tipo del archivo (INE, PERMISO, CARTA RESPONSIVA, etc.):")
        url_archivo = input("Escribe el url o ruta del archivo:")
        fecha_subida = input("Escribe la fecha de hoy:")
        archivo = Archivo(id, id_entretenimiento, id_establecimiento, id_evento, nombre_archivo, extencion, tipo_archivo, url_archivo, fecha_subida)
        archivo_dao.actualizar(archivo)
        print("El archivo fue actualizado con éxito")
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
        print(f"El archivo {id} ha sido eliminado con éxito")
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
            print("No hay categorías registradas")
        else:
            for categoria in categorias:
                print (f"| {categoria.id} | {categoria.nombre} | {categoria.tipo_categoria} | {categoria.descripcion} | {categoria.estado} | ")
        print("\n Conexión exitosa con la base de datos")

    except Exception as e:
        print("Existe un error")
        print(e)

#==========================================================================================

def insertar_categorias():
    print("Insertar una nueva categoría")
    nombre = input("Escribe el mombre de la categoría:")
    tipo_categoria = input("Escribe el tipo de categoría:")
    descripcion = input("Escribe una breve descripción sobre esta categoría:")
    estado = input("Escribe el estado de la categoría:")
    try:
        categoria_dao = CategoriaDAO()
        ultimo_id = categoria_dao.obtener_ultimo_id() + 1
        categoria = Categoria(ultimo_id, nombre, tipo_categoria, descripcion, estado)
        categoria_dao.insertar(categoria)
        print("Inserción de la nueva categoría fue existosa")
    except Exception as e:
        print("Error al insertar la categoría")
        print(e)

#==========================================================================================

def actualizar_categoria():
    try:
        categoria_dao = CategoriaDAO()
        print("Lista de categorías disponibles")
        ver_categorias()
        id = int(input("Seleccione el id de la categoría a actualizar"))
        nombre = input("Escribe el nombre de la categoría:")
        tipo_categoria = input("Escribe el tipo de categoría:")
        descripcion = input("Escribe una breve descripción de la categoría:")
        estado = input("Escribe correo electrónico:")
        categoria = Categoria(id, nombre, tipo_categoria, descripcion, estado)
        categoria_dao.actualizar(categoria)
        print("La categoría fue actualizada con éxito")
    except Exception as e:
        print("Error al actualizar la categoría")
        print(e)

#==========================================================================================

def eliminar_categoria():
    try:
        categoria_dao = CategoriaDAO()
        print("Lista de categorías disponibles")
        ver_categorias()
        id = int(input("Escribe el id de la categoría a eliminar:"))
        categoria_dao.eliminar(id)
        print(f"La categoría {id} ha sido eliminada con éxito")
    except Exception as e:
        print(f"Error al eliminar la categoría {id}")
        print(e)


#==========================================================================================

#ESTABLECIMIENTO

def ver_establecimiento():
    try:
        establecimiento_dao = EstablecimientoDAO()
        establecimientos = establecimiento_dao.obtener_todo()

        if len(establecimientos) == 0:
            print("No hay establecimientos registradas")
        else:
            for establecimiento in establecimientos:
                print (f"| {establecimiento.id} | {establecimiento.nombre_establecimiento} | {establecimiento.tipo_categoria} | {establecimiento.horario_inicio} | {establecimiento.horario_fin} | {establecimiento.direccion} | {establecimiento.mapa} | {establecimiento.nombre_propietario} | {establecimiento.edad} | {establecimiento.telefono} | {establecimiento.correo} | {establecimiento.descripcion_corta} | {establecimiento.descripcion_completa} | {establecimiento.caracteristica_1} | {establecimiento.caracteristica_2} | {establecimiento.caracteristica_3} | {establecimiento.instagram} | {establecimiento.facebook} | {establecimiento.pagina_web} | {establecimiento.estado} | {establecimiento.servicios} | {establecimiento.rango_precios} | {establecimiento.productos_ofrecer} |")
        print("\n Conexión exitosa con la base de datos")

    except Exception as e:
        print("Existe un error")
        print(e)

#==========================================================================================

def insertar_establecimientos():
    print("Insertar una nueva establecimiento")
    nombre_establecimiento = input("Escribe el mombre del establecimiento:")
    tipo_categoria = int(input("Escribe el id de la categoría:"))
    horario_inicio = input("Escribe la hora de inicio:")
    horario_fin = input("Escribe la hora de cierre:")
    direccion = input("Escribe la dirección:")
    mapa = input("Escribe el mapa:")
    nombre_propieatrio = input("Escribe el nombre del propietario:")
    telefono = input("Escribe el numero del teléfono:")
    correo = input("Escribe el correo electrónico:")
    descripcion_corta = input("Escribe una corta descripción:")
    descripcion_completa = input("Escribe una completa descripción:")
    caracteristica_1 = input("Escribe la primer carateristica:")
    caracteristica_2 = input("Escribe la segunda carateristica:")
    caracteristica_3 = input("Escribe la tercera carateristica:")
    instagram = input("Escribe el instagram del establecimiento:")
    facebook = input("Escribe el facebook del establecimiento:")
    pagina_web = input("Escribe la página web del establecimiento:")
    estado = input("Escribe el estado del establecimiento:")
    servicios = input("Escribe los servicios que ofrece el establecimiento:")
    rango_precios = input("Escribe el rango de precion para el establecimiento:")
    productos_ofrecen = input("Escribe los prodcutos que ofrece el establecimiento:")
    
    try:
        establecimiento_dao = EstablecimientoDAO()
        ultimo_id = establecimiento_dao.obtener_ultimo_id() + 1
        establecimiento = Establecimiento(ultimo_id, nombre_establecimiento, tipo_categoria, horario_inicio, horario_fin, direccion, mapa, nombre_propieatrio, telefono, correo, descripcion_corta, descripcion_completa, caracteristica_1, caracteristica_2, caracteristica_3, instagram, facebook, pagina_web, estado, servicios, rango_precios, productos_ofrecen)
        establecimiento_dao.insertar(establecimiento)
        print("Inserción del establecimiento fue existosa")
    except Exception as e:
        print("Error al insertar el establecimiento")
        print(e)

#==========================================================================================

def actualizar_establecimiento():
    try:
        establecimiento_dao = EstablecimientoDAO()
        print("Lista de establecimientos disponibles")
        ver_establecimiento()
        id = int(input("Seleccione el id del establecimiento a actualizar"))
        nombre_establecimiento = input("Escribe el mombre del establecimiento:")
        tipo_categoria = int(input("Escribe el id de la categoría:"))
        horario_inicio = input("Escribe la hora de inicio:")
        horario_fin = input("Escribe la hora de cierre:")
        direccion = input("Escribe la dirección:")
        mapa = input("Escribe el mapa:")
        nombre_propieatrio = input("Escribe el nombre del propietario:")
        telefono = input("Escribe el numero del teléfono:")
        correo = input("Escribe el correo electrónico:")
        descripcion_corta = input("Escribe una corta descripción:")
        descripcion_completa = input("Escribe una completa descripción:")
        caracteristica_1 = input("Escribe la primer carateristica:")
        caracteristica_2 = input("Escribe la segunda carateristica:")
        caracteristica_3 = input("Escribe la tercera carateristica:")
        instagram = input("Escribe el instagram del establecimiento:")
        facebook = input("Escribe el facebook del establecimiento:")
        pagina_web = input("Escribe la página web del establecimiento:")
        estado = input("Escribe el estado del establecimiento:")
        servicios = input("Escribe los servicios que ofrece el establecimiento:")
        rango_precios = input("Escribe el rango de precion para el establecimiento:")
        productos_ofrecen = input("Escribe los prodcutos que ofrece el establecimiento:")
        establecimiento = Establecimiento(id, nombre_establecimiento, tipo_categoria, horario_inicio, horario_fin, direccion, mapa, nombre_propieatrio, telefono, correo, descripcion_corta, descripcion_completa, caracteristica_1, caracteristica_2, caracteristica_3, instagram, facebook, pagina_web, estado, servicios, rango_precios, productos_ofrecen)
        establecimiento_dao.actualizar(establecimiento)
        print("El establecimiento fue actualizada con éxito")
    except Exception as e:
        print("Error al actualizar el establecimiento")
        print(e)

#==========================================================================================

def eliminar_establecimiento():
    try:
        establecimiento_dao = EstablecimientoDAO()
        print("Lista de establecimientos disponibles")
        ver_establecimiento()
        id = int(input("Escribe el id del establecimiento a eliminar:"))
        establecimiento_dao.eliminar(id)
        print(f"El establecimiento {id} ha sido eliminado con éxito")
    except Exception as e:
        print(f"Error al eliminar el establecimiento {id}")
        print(e)
    #MENUS
#==========================================================================================
def menu_Admin():
    print("1. Ver administradores")
    print("2. Actualizar administradores")
    print("3. Eliminar administradores")
    
    opcion = int(input("Selecciona una opción (1-3):"))

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
    print("4. Eliminar archivo(s)")
    opcion = int(input("Selecciona una opción (1-4):"))

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
    print("1. Ver categorías")
    print("2. Insertar categoría")
    print("3. Actualizar categorías")
    print("4. Eliminar categorías")
    opcion = int(input("Selecciona una opción (1-4):"))

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
#==========================================================================================

#ENTRETENIMIENTO

def ver_entretenimientos():
    try:
        entretenimiento_dao = EntretenimientoDAO()
        entretenimientos = entretenimiento_dao.obtener_todo()

        if len(entretenimientos) == 0:
            print("No hay entretenimientos registrados")
        else:
            for entretenimiento in entretenimientos:
                print (f"| {entretenimiento.id} | {entretenimiento.nombre_entretenimiento} | {entretenimiento.categoria} | {entretenimiento.horario_inicio} | {entretenimiento.horario_fin} | {entretenimiento.direccion} | {entretenimiento.mapa} | {entretenimiento.nombre_responsable} | {entretenimiento.telefono} | {entretenimiento.correo} | {entretenimiento.descripcion_corta} | {entretenimiento.descripcion_completa} | {entretenimiento.caracteristica_1} | {entretenimiento.caracteristica_2} | {entretenimiento.caracteristica_3} |  {entretenimiento.capacidad} | {entretenimiento.precio} |  {entretenimiento.servicio_1} |  {entretenimiento.servicio_2} |   {entretenimiento.servicio_3} |  {entretenimiento.servicio_4} |  {entretenimiento.servicio_5} | {entretenimiento.recomendacion_1} | {entretenimiento.recomendacion_2} | {entretenimiento.recomendacion_3} | {entretenimiento.recomendacion_4} | {entretenimiento.instagram} | {entretenimiento.facebook} | {entretenimiento.pagina_web} | ")
        print("\n Conexion exitosa con la base de datos")

    except Exception as e:
        print("Existe un error")
        print(e)

#==========================================================================================

def insertar_entretenimientos():
    print("INSERTAR UN NUEVO entretenimiento")
    nombre_entretenimiento = input("Escribe el nombre del entretenimiento:")
    categoria = int(input("Escribe el id de la categoria:"))
    horario_inicio = input("Escribe la hora de inicio:")
    horario_fin = input("Escribe la hora de cierre:")
    direccion = input("Escribe la direccion:")
    mapa = input("Escribe el mapa:")
    nombre_responsable = input("Escribe el nombre del responsable:")
    telefono = input("Escribe el numero del telefono:")
    correo = input("Escribe el correo electronico:")
    descripcion_corta = input("Escribe una corta descripcion:")
    descripcion_completa = input("Escribe una completa descripcion:")
    caracteristica_1 = input("Escribe la primer carateristica:")
    caracteristica_2 = input("Escribe la segunda carateristica:")
    caracteristica_3 = input("Escribe la tercera carateristica:")
    capacidad = input("Escribe la capacidad que tiene el lugar:")
    precio = input("Escribe los precios:")
    servicio_1 = input("Escribe el primer servicio que ofrece")
    servicio_2 = input("Escribe el segundo servicio que ofrece:")
    servicio_3 = input("Escribe el tercer servicio que ofrece:")
    servicio_4 = input("Escribe el cuarto servicio que ofrece:")
    servicio_5 = input("Escribe el quinto servicio que ofrece:")
    recomendacion_1 = input("Escribe la primerrecomendacion:")
    recomendacion_2 = input("Escribe la segunda recomendacion:")
    recomendacion_3 = input("Escribe la tercera recomendacion:")
    recomendacion_4 = input("Escribe la cuarta recomendacion:")
    instagram = input("Escribe el instagram del entretenimeinto:")
    facebook = input("Escribe el facebook del entretenimeinto:")
    pagina_web = input("Escribe la pagina web del entreteniminto:")
    
    
    try:
        entretenimiento_dao = EntretenimientoDAO()
        ultimo_id = entretenimiento_dao.obtener_ultimo_id() + 1
        entretenimiento = Entretenimiento(ultimo_id, nombre_entretenimiento, categoria, horario_inicio, horario_fin, direccion, mapa, nombre_responsable, telefono, correo, descripcion_corta, descripcion_completa, caracteristica_1, caracteristica_2, caracteristica_3, capacidad, precio, servicio_1, servicio_2, servicio_3, servicio_4, servicio_5,  recomendacion_1,  recomendacion_2,  recomendacion_3,  recomendacion_4, instagram, facebook, pagina_web )
        entretenimiento_dao.insertar(entretenimiento)
        print("Insercion del nuevo entretenimiento fue existosa")
    except Exception as e:
        print("Error al insertar entretenimiento")
        print(e)

#==========================================================================================



def actualizar_entretenimiento():
    try:
        entretenimiento_dao = EntretenimientoDAO()
        print("Lista de entretenimientos disponibles")
        ver_entretenimientos()

        id = int(input("Seleccione el id del entretenimiento a actualizar"))
        nombre_entretenimiento = input("Escribe el nombre del entretenimiento:")
        categoria = int(input("Escribe el id de la categoria:"))
        horario_inicio = input("Escribe la hora de inicio:")
        horario_fin = input("Escribe la hora de cierre:")
        direccion = input("Escribe la direccion:")
        mapa = input("Escribe el mapa:")
        nombre_responsable = input("Escribe el nombre del responsable:")
        telefono = input("Escribe el numero del telefono:")
        correo = input("Escribe el correo electronico:")
        descripcion_corta = input("Escribe una corta descripcion:")
        descripcion_completa = input("Escribe una completa descripcion:")
        caracteristica_1 = input("Escribe la primer carateristica:")
        caracteristica_2 = input("Escribe la segunda carateristica:")
        caracteristica_3 = input("Escribe la tercera carateristica:")
        capacidad = input("Escribe la capacidad que tiene el lugar:")
        precio = input("Escribe los precios:")
        servicio_1 = input("Escribe el primer servicio que ofrece")
        servicio_2 = input("Escribe el segundo servicio que ofrece:")
        servicio_3 = input("Escribe el tercer servicio que ofrece:")
        servicio_4 = input("Escribe el cuarto servicio que ofrece:")
        servicio_5 = input("Escribe el quinto servicio que ofrece:")
        recomendacion_1 = input("Escribe la primerrecomendacion:")
        recomendacion_2 = input("Escribe la segunda recomendacion:")
        recomendacion_3 = input("Escribe la tercera recomendacion:")
        recomendacion_4 = input("Escribe la cuarta recomendacion:")
        instagram = input("Escribe el instagram del entretenimeinto:")
        facebook = input("Escribe el facebook del entretenimeinto:")
        pagina_web = input("Escribe la pagina web del entreteniminto:")

        entretenimiento = Entretenimiento (id, nombre_entretenimiento, categoria, horario_inicio, horario_fin, direccion, mapa, nombre_responsable, telefono, correo, descripcion_corta, descripcion_completa, caracteristica_1, caracteristica_2, caracteristica_3, capacidad, precio, servicio_1, servicio_2, servicio_3, servicio_4, servicio_5,  recomendacion_1,  recomendacion_2,  recomendacion_3,  recomendacion_4, instagram, facebook, pagina_web )
        entretenimiento_dao.actualizar(entretenimiento)
        print("El entretenimiento fue actualizado con exito")
    except Exception as e:
        print("Error al actualizar entretenimiento")
        print(e)

#==========================================================================================

def eliminar_entretenimeinto():
    try:
        entretenimiento_dao = EntretenimientoDAO()
        print("Lista de entretenimientos disponibles")
        ver_entretenimientos()
        id = int(input("Escribe el id del entretenimeinto a eliminar:"))
        entretenimiento_dao.eliminar(id)
        print(f"El entretenimeinto{id} ha sido eliminado con exito")
    except Exception as e:
        print(f"Error al eliminar el entretenimiento {id}")
        print(e)

#==========================================================================================
#==========================================================================================

#EVENTOS

def ver_eventos():
    try:
        evento_dao = EventoDAO()
        eventos = evento_dao.obtener_todo()

        if len(eventos) == 0:
            print("No hay eventos registrados")
        else:
            for evento in eventos:
                print (f"| {evento.id} | {evento.nombre_evento} | {evento.categoria} | {evento.fecha} | {evento.horario_inicio} | {evento.horario_fin} | {evento.ubicacion} | {evento.mapa} | {evento.nombre_organizador} | {evento.edad} | {evento.telefono} | {evento.correo} | {evento.descripcion_corta} | {evento.descripcion_completa} | {evento.caracteristica_1} | {evento.caracteristica_2} | {evento.caracteristica_3} | {evento.instagram} | {evento.facebook} | {evento.pagina_web} | {evento.estado} | {evento.datos_destacados} | ")
        print("\n Conexion exitosa con la base de datos")

    except Exception as e:
        print("Existe un error")
        print(e)

#==========================================================================================

def insertar_eventos():
    print("INSERTAR UN NUEVO EVENTO")
    nombre_evento = input("Escribe el nombre del evento:")
    categoria = int(input("Escribe el id de la categoria:"))
    fecha = input("Escribe la fecha del evento:")
    horario_inicio = input("Escribe la hora de inicio:")
    horario_fin = input("Escribe la hora de cierre:")
    ubicacion = input("Escribe la ubicacion:")
    mapa = input("Escribe el mapa:")
    nombre_organizador = input("Escribe el nombre del organizador:")
    edad = input("Escribe la edad del organizador:")
    telefono = input("Escribe el numero del telefono:")
    correo = input("Escribe el correo electronico:")
    descripcion_corta = input("Escribe una corta descripcion:")
    descripcion_completa = input("Escribe una completa descripcion:")
    caracteristica_1 = input("Escribe la primer carateristica:")
    caracteristica_2 = input("Escribe la segunda carateristica:")
    caracteristica_3 = input("Escribe la tercera carateristica:")
    instagram = input("Escribe el instagram del entretenimeinto:")
    facebook = input("Escribe el facebook del entretenimeinto:")
    pagina_web = input("Escribe la pagina web del entreteniminto:")
    estado = input("Escribe el estado del evento:")
    datos_destacados = input("Escribe los datos destacados del evento:")
    try:
        evento_dao = EventoDAO()
        ultimo_id = evento_dao.obtener_ultimo_id() + 1
        evento = Evento(ultimo_id, nombre_evento, categoria, fecha, horario_inicio, horario_fin, ubicacion, mapa, nombre_organizador, edad, telefono, correo, descripcion_corta, descripcion_completa, caracteristica_1, caracteristica_2, caracteristica_3, instagram, facebook, pagina_web, estado, datos_destacados )
        evento_dao.insertar(evento)
        print("Insercion del nuevo evento fue existosa")
    except Exception as e:
        print("Error al insertar evento")
        print(e)

#==========================================================================================

def actualizar_evento():
    try:
        evento_dao = EventoDAO()
        print("Lista de eventos disponibles")
        ver_eventos()
        id = int(input("Seleccione el id del evento a actualizar"))
        nombre_evento = input("Escribe el nombre del evento:")
        categoria = int(input("Escribe el id de la categoria:"))
        fecha = input("Escribe la fecha del evento:")
        horario_inicio = input("Escribe la hora de inicio:")
        horario_fin = input("Escribe la hora de cierre:")
        ubicacion = input("Escribe la ubicacion:")
        mapa = input("Escribe el mapa:")
        nombre_organizador = input("Escribe el nombre del organizador:")
        edad = input("Escribe la edad del organizador:")
        telefono = input("Escribe el numero del telefono:")
        correo = input("Escribe el correo electronico:")
        descripcion_corta = input("Escribe una corta descripcion:")
        descripcion_completa = input("Escribe una completa descripcion:")
        caracteristica_1 = input("Escribe la primer carateristica:")
        caracteristica_2 = input("Escribe la segunda carateristica:")
        caracteristica_3 = input("Escribe la tercera carateristica:")
        instagram = input("Escribe el instagram del entretenimeinto:")
        facebook = input("Escribe el facebook del entretenimeinto:")
        pagina_web = input("Escribe la pagina web del entreteniminto:")
        estado = input("Escribe el estado del evento:")
        datos_destacados = input("Escribe los datos destacados del evento:")

        evento = Evento(id, nombre_evento, categoria, fecha, horario_inicio, horario_fin, ubicacion, mapa, nombre_organizador, edad, telefono, correo, descripcion_corta, descripcion_completa, caracteristica_1, caracteristica_2, caracteristica_3, instagram, facebook, pagina_web, estado, datos_destacados)
        evento_dao.actualizar(evento)
        print("El evento fue actualizado con exito")
    except Exception as e:
        print("Error al actualizar evento")
        print(e)

#==========================================================================================

def eliminar_evento():
    try:
        evento_dao = EventoDAO()
        print("Lista de eventos disponibles")
        ver_eventos()
        id = int(input("Escribe el id del evento a eliminar:"))
        evento_dao.eliminar(id)
        print(f"El evento {id} ha sido eliminado con exito")
    except Exception as e:
        print(f"Error al eliminar evento {id}")
        print(e)

#==========================================================================================
#==========================================================================================

#IMAGEN

def ver_imagenes():
    try:
        imagen_dao = ImagenDAO()
        imagenes = imagen_dao.obtener_todo()

        if len(imagenes) == 0:
            print("No hay imagenes registrados")
        else:
            for imagen in imagenes:
                print (f"| {imagen.id} | {imagen.id_establecimiento} | {imagen.id_entretenimiento} | {imagen.id_evento} | {imagen.url_imagen} | {imagen.public_id} |")
        print("\n Conexión exitosa con la base de datos")

    except Exception as e:
        print("Existe un error")
        print(e)

#==========================================================================================
    
def insertar_imagenes():
    print("Insertar una nueva imagen")
    print("Escoje 1 establecimiento, entretenimiento o evento")
    id_establecimiento = int(input("Escribe el id de un establecimiento al que pertenece:"))
    id_entretenimiento = int(input("Escribe el id de entretenimiento al que pertenece:"))
    id_evento = int(input("Escribe el id al evento al que pertenece:"))
    url_imagen = input("Escribe el url o ruta de la imagen:")
    public_id = input("Escribe el public_id de la imagen:")
    
    try:
        imagen_dao = ImagenDAO()
        ultimo_id = imagen_dao.obtener_ultimo_id() + 1
        imagen = Imagen(ultimo_id, id_entretenimiento, id_establecimiento, id_evento, url_imagen, public_id)
        imagen_dao.insertar(imagen)
        print("Inserción de la nueva imagen fue existosa")
    except Exception as e:
        print("Error al insertar la imagen")
        print(e)

#==========================================================================================

def actualizar_imagen():
    try:

        imagen_dao = ImagenDAO()
        print("Lista de imagenes disponibles")
        ver_imagenes()
        id = int(input("Seleccione el id de la imagen a actualizar"))
        id_establecimiento = int(input("Escribe el id del establecimiento al que pertenece:"))
        id_entretenimiento = int(input("Escribe el id de entretenimiento al que pertenece:"))
        id_evento = int(input("Escribe el id del evento al que pertenece:"))
        url_imagen = input("Escribe el url o ruta de la imagen:")
        public_id = input("Escribe el public_id de la imagen:")

        imagen = Imagen(id, id_entretenimiento, id_establecimiento, id_evento, url_imagen, public_id)
        imagen_dao.actualizar(imagen)
        print("La imagen fue actualizada con éxito")
    except Exception as e:
        print("Error al actualizar la imagen")
        print(e)

    #==========================================================================================

def eliminar_imagen():
    try:
        imagen_dao = ImagenDAO()
        print("Lista de imagenes disponibles")
        ver_imagenes()
        id = int(input("Escribe el id de la imagen a eliminar:"))
        imagen_dao.eliminar(id)
        print(f"La imagen {id} ha sido eliminado con éxito")
    except Exception as e:
        print(f"Error al eliminar la imagen {id}")
        print(e)

#==========================================================================================
#==========================================================================================

def menu_establecimientos():
    print("1. Ver establecimientos")
    print("2. Insertar establecimiento")
    print("3. Actualizar establecimientos")
    print("4. Eliminar establecimientos")
    opcion = int(input("Selecciona una opción (1-4):"))

    match opcion:
        case 1:
            ver_establecimiento()
        case 2:
            insertar_establecimientos()
        case 3:
            actualizar_establecimiento()
        case 4:
            eliminar_establecimiento()

#==========================================================================================

def menu_entrenimientos():
    print("1. Ver entretenimientos")
    print("2. Insertar entretenimiento")
    print("3. Actualizar entretenimientos")
    print("4. Eliminar entretenimientos")
    opcion = int(input("Selecciona una opción (1-4):"))

    match opcion:
        case 1:
            ver_entretenimientos()
        case 2:
            insertar_entretenimientos()
        case 3:
            actualizar_entretenimiento()
        case 4:
            eliminar_entretenimeinto()

#==========================================================================================

#==========================================================================================

def menu_archivos():
    print("1. Ver archivos")
    print("2. Insertar archivo")
    print("3. Actualizar archivos")
    print("4. Eliminar archivo(s)")
    opcion = int(input("Selecciona una opción (1-4):"))

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
    print("1. Ver categorías")
    print("2. Insertar categoría")
    print("3. Actualizar categorías")
    print("4. Eliminar categorías")
    opcion = int(input("Selecciona una opción (1-4):"))

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
#==========================================================================================

def menu_imagenes():
    print("1. Ver imágenes")
    print("2. Insertar imagen")
    print("3. Actualizar imágenes")
    print("4. Eliminar imágenes")
    opcion = int(input("Selecciona una opción (1-4):"))

    match opcion:
        case 1:
            ver_imagenes()
        case 2:
            insertar_imagenes()
        case 3:
            actualizar_imagen()
        case 4:
            eliminar_imagen()

#==========================================================================================

#==========================================================================================

def menu_eventos():
    print("1. Ver eventos")
    print("2. Insertar evento")
    print("3. Actualizar eventos")
    print("4. Eliminar eventos")
    opcion = int(input("Selecciona una opción (1-4):"))

    match opcion:
        case 1:
            ver_imagenes()
        case 2:
            insertar_imagenes()
        case 3:
            actualizar_imagen()
        case 4:
            eliminar_imagen()

#==========================================================================================

def main():
    print("=== Menú Ruta Mágica ===")
    print("Menu de opciones:")
    print("1. Establecimientos")
    print("2. Entretenimientos")
    print("3. Eventos")
    print("4. Administradores")
    print("5. Archivos")
    print("6. Categorías")
    print("7. Imágenes")
    opcion = int(input("Escribe tu opción: "))
    match opcion:
        case 1: menu_establecimientos()
        case 2: menu_entrenimientos()
        case 3: menu_eventos()
        case 4: menu_Admin()
        case 5: menu_archivos()
        case 6: menu_categorias()
        case 7: menu_imagenes

    print("Saliendo del sistema de Ruta Mágica ....")


if __name__ == "__main__":
    main()