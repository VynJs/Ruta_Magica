class Establecimiento:

    #constructor
    def _init_(self, id, nombre_establecimiento, categoria, horario_inicio, horario_fin, direccion, mapa, nombre_propietario, edad, telefono, correo, descripcion_corta, descripcion_completa, caracteristica_1, caracteristica_2, caracteristica_3, instagram, facebook, pagina_web, estado, servicios, rango_precios, productos_ofrecer):
        self.id = id
        self.nombre_establecimiento = nombre_establecimiento
        self.categoria = categoria
        self.horario_inicio = horario_inicio
        self.horario_fin = horario_fin
        self.direccion = direccion
        self.mapa = mapa
        self.nombre_propietario = nombre_propietario
        self.edad = edad
        self.telefono = telefono
        self.correo = correo
        self.descripcion_corta = descripcion_corta
        self.descripcion_Completa = descripcion_completa
        self.caracteristica_1 =  caracteristica_1
        self.caracteristica_2 = caracteristica_2
        self.caracteristica_3 = caracteristica_3
        self.instagram = instagram
        self.facebook = facebook
        self.pagina_web = pagina_web
        self.estado = estado
        self.servicios = servicios
        self.rango_precios = rango_precios
        self.productos_ofrecer = productos_ofrecer

    def activar(self):
            self.estado = True
            
    def desactivar(self):
            self.estado = False
    
    def mostrar_info(self):
            return f"ID: {self.id}, Nombre del establecimiento:{self.nombre_establecimiento}, Categoria: {self.categoria}, Horario de atención: {self.horario_inicio} - {self.horario_fin},  Dirección: {self.direccion}, Mapa: {self.mapa}, Nombre del propietario: {self.nombre_propietario}, Edad: {self.edad}, Telefono:{self.telefono}, Correo: {self.correo}, Descripción corta: {self.descripcion_corta}, Descripción completa:{self.descripcion_completa}, Caracteristica 1: {self.caracteristica_1}, Caracteristica 2: {self.caracteristica_2}, Caracteristica 3: {self.caracteristica_3}, Instagram: {self.instagram}, FacebooK: {self.facebook}, Pagina Web: {self.pagina_web}, Archivo: {self.archivo}, Estado: {self.estado}, Servicios que ofrece: {self.servicios}, Rango de precios: {self.rango_precios}, Productos a ofrecer: {self.productos_ofrecer} "