class Categoria:

    #constructor

    def __init_(self, id, nombre,tipo_categoria, descripcion, estado):
        self.id = id
        self.nombre = nombre
        self.tipo_categoria = tipo_categoria
        self.descripcion = descripcion
        self.estado = estado

    def activar(self):
            self.estado = True
            
    def desactivar(self):
            self.estado = False
    
    def mostrar_info(self):
            return f"ID: {self.id}, Nombre de la categoria:{self.nombre}, Tipo de categoria: {self.tipo_categoria}, Descripcion: {self.descripcion}, Estado: {self.estado}"