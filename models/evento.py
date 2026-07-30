class Evento:

    #constructor
    def _init_(self, id, nombre_evento, categoria, fecha, horario_inicio, horario_fin, ubicacion, mapa, nombre_organizador, edad, telefono, correo, descripcion_corta, descripcion_completa, caracteristica_1, caracteristica_2, caracteristica_3, instagram, facebook, pagina_web, estado, datos_destacados):
        self.id = id
        self.nombre_evento = nombre_evento
        self.categoria = categoria
        self.fecha = fecha
        self.horario_inicio = horario_inicio
        self.horario_fin =  horario_fin
        self.ubicacion = ubicacion
        self.mapa = mapa
        self.nombre_organizador = nombre_organizador
        self.edad = edad
        self.telefono = telefono
        self.correo = correo
        self.descripcion_corta = descripcion_corta
        self.descripcion_completa = descripcion_completa
        self.caracteristica_1 = caracteristica_1
        self.caracteristica_2 = caracteristica_2
        self.caracteristica_3 = caracteristica_3
        self.instagram = instagram
        self.facebook = facebook
        self.pagina_web - pagina_web
        self.estado = estado
        self.datos_destacados = datos_destacados

    def activar(self):
            self.estado = True
        
    def desactivar(self):
            self.estado = False

    def mostrar_info(self):
            return f"ID: {self.id}, Nombre del evento:{self.nombre_evento}, Categoria: {self.categoria}, Fecha del evento: {self.fecha}, Horario: {self.horario_inicio} - {self.horario_fin},  Ubicación: {self.ubicacion}, Mapa: {self.mapa}, Nombre del organizador: {self.nombre_organizador}, Edad: {self.edad}, Telefono:{self.telefono}, Correo: {self.correo}, Descripción corta: {self.descripcion_corta}, Descripción completa:{self.descripcion_completa}, Caracteristica 1: {self.caracteristica_1}, Caracteristica 2: {self.caracteristica_2}, Caracteristica 3: {self.caracteristica_3}, Instagram: {self.instagram}, FacebooK: {self.facebook}, Pagina Web: {self.pagina_web}, Estado: {self.estado}, Archivo: {self.archivo} "