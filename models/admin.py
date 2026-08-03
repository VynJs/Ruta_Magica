class Admin:

    #constructor

    def __init__(self, id, nombre, apellido_p="", apellido_m="", correo="", password=None):
        self.id = id
        self.nombre = nombre
        self.apellido_p = apellido_p
        self.apellido_m = apellido_m
        self.correo = correo
        self.password = password