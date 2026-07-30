class Entretenimiento:

    #constructor

    def _init_(self, id, nombre_entretenimeinto, categoria, horario_inicio, horario_fin, direccion, latitud, longitud, nombre_responsable, telefono, correo, descripcion_corta, descripcion_completa, caracteristica_1, caracteristica_2, caracteristica_3, capacidad, precio, servicio_1, servicio_2, servicio_3, servicio_4, servicio_5, recomendacion_1, recomendacion_2, recomendacion_3,recomendacion_4, instagram, facebook, pagina_web):
        self.id = id
        self.nombre_entretenimiento = nombre_entretenimeinto
        self.categoria = categoria
        self.horario_inicio = horario_inicio
        self.horario_fin = horario_fin
        self.direccion = direccion
        self.latitud = latitud
        self.longitud = longitud
        self.nombre_responsable = nombre_responsable
        self.telefono = telefono
        self.correo = correo
        self.descripcion_corta = descripcion_corta
        self.descripcion_completa = descripcion_completa
        self.caracteristica_1 = caracteristica_1
        self.caracteristica_2 = caracteristica_2
        self.caracteristica_3 = caracteristica_3
        self.capacidad = capacidad
        self.precio = precio
        self.servicio_1 = servicio_1
        self.servicio_2 = servicio_2
        self.servicio_3 = servicio_3
        self.servicio_4 = servicio_4
        self.servicio_5 = servicio_5
        self.recomendacion_1 = recomendacion_1
        self.recomendacion_2 = recomendacion_2
        self.recomendacion_3 = recomendacion_3
        self.recomendacion_4 = recomendacion_4
        self.instagram = instagram
        self.facebook = facebook
        self.pagina_web = pagina_web

        
    def mostrar_info(self):
            return f"ID: {self.id}, Nombre :{self.nombre_entretenimiento}, Categoria: {self.categoria}, Horario : {self.horario_inicio}, - {self.horario_fin},  Dirección: {self.direccion}, Mapa: {self.longitud}, - {self.latitud}, Nombre del responsable: {self.nombre_responsable}, Telefono:{self.telefono}, Correo: {self.correo}, Descripción corta: {self.descripcion_corta}, Descripción completa:{self.descripcion_completa}, Caracteristica 1: {self.caracteristica_1}, Caracteristica 2: {self.caracteristica_2}, Caracteristica 3: {self.caracteristica_3}, Capacidad: {self.capacidad}, Precios: {self.precio}, Servicio 1:{self.servicio_1}, Servicio 2:{self.servicio_2}, Servicio 3:{self.servicio_3}, Servicio 4:{self.servicio_4}, Servicio 5:{self.servicio_5}, Recomendacion 1: {self.recomendacion_1}, Recomendacion 2: {self.recomendacion_2}, Recomendacion 3: {self.recomendacion_3}, Recomendacion 4: {self.recomendacion_4},  Instagram: {self.instagram}, FacebooK: {self.facebook}, Pagina Web: {self.pagina_web}, Archivo: {self.archivo}" 