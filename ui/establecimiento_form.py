import flet as ft

from config.tema import Color
from models.establecimiento import Establecimiento
from dao.establecimiento_dao import EstablecimientoDAO
from dao.categoria_dao import CategoriaDAO

# Estilo compartido de los TextField y Dropdown (fondo oscuro, borde
# verde oliva, texto claro), tomado de la paleta del mockup.
def _estilo_campo(control):
    control.border_color = Color.BORDE
    control.focused_border_color = Color.DORADO
    control.color = Color.TEXTO
    control.label_style = ft.TextStyle(color=Color.TEXTO_SECUNDARIO)
    control.bgcolor = Color.TARJETA
    control.border_radius = 8
    return control

def establecimiento_form(regresar, establecimiento_editar=None):
    categoria_dao = CategoriaDAO()
    categorias = categoria_dao.obtener_todo(tipo="establecimiento")
    opciones_categoria = [
        ft.dropdown.Option(key=str(c.id), text=c.nombre) for c in categorias
    ]

    nombre_input = _estilo_campo(ft.TextField(
        label="Nombre del establecimiento: ",
        width=400,
    ))
    categoria_input = _estilo_campo(ft.Dropdown(
        label="Categoria: ",
        width=400,
        options=opciones_categoria
    ))
    direccion_input = _estilo_campo(ft.TextField(
        label="Direccion: ",
        width=400,
    ))
    horario_apertura_input = _estilo_campo(ft.TextField(
        label="Horario de apertura (ej. 10:00 am): ",
        width=400,
    ))
    horario_cierre_input = _estilo_campo(ft.TextField(
        label="Horario de cierre (ej. 08:00 pm): ",
        width=400,
    ))
    propietario_nombre_input = _estilo_campo(ft.TextField(
        label="Nombre del propietario: ",
        width=400,
    ))
    propietario_edad_input = _estilo_campo(ft.TextField(
        label="Edad del propietario: ",
        width=400,
    ))
    propietario_telefono_input = _estilo_campo(ft.TextField(
        label="Telefono del propietario: ",
        width=400,
    ))
    propietario_correo_input = _estilo_campo(ft.TextField(
        label="Correo del propietario: ",
        width=400,
    ))
    descripcion_input = _estilo_campo(ft.TextField(
        label="Descripcion corta: ",
        width=400,
        multiline=True,
    ))
    estado_input = _estilo_campo(ft.Dropdown(
        label="Estado: ",
        width=400,
        value="en_revision",
        options=[
            ft.dropdown.Option(key="en_revision", text="En revision"),
            ft.dropdown.Option(key="aprobado", text="Aprobado"),
            ft.dropdown.Option(key="rechazado", text="Rechazado"),
        ]
    ))
    mensaje = ft.Text(
        "",
        color=Color.EXITO,
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # Si viene un establecimiento a editar, precargamos los campos
    if establecimiento_editar is not None:
        nombre_input.value = establecimiento_editar.nombre
        categoria_input.value = str(establecimiento_editar.categoria_id)
        direccion_input.value = establecimiento_editar.direccion
        horario_apertura_input.value = establecimiento_editar.horario_apertura
        horario_cierre_input.value = establecimiento_editar.horario_cierre
        propietario_nombre_input.value = establecimiento_editar.propietario_nombre
        propietario_edad_input.value = str(establecimiento_editar.propietario_edad)
        propietario_telefono_input.value = establecimiento_editar.propietario_telefono
        propietario_correo_input.value = establecimiento_editar.propietario_correo
        descripcion_input.value = establecimiento_editar.descripcion_corta
        estado_input.value = establecimiento_editar.estado

    def guardar_establecimiento(e):
        # recuperar los valores de los TextField
        nombre = nombre_input.value
        categoria = categoria_input.value
        direccion = direccion_input.value
        horario_apertura = horario_apertura_input.value
        horario_cierre = horario_cierre_input.value
        propietario_nombre = propietario_nombre_input.value
        propietario_edad = propietario_edad_input.value
        propietario_telefono = propietario_telefono_input.value
        propietario_correo = propietario_correo_input.value
        descripcion = descripcion_input.value
        estado = estado_input.value

        # Validar que los campos no esten vacios
        if (nombre == "" or categoria is None or direccion == "" or
                propietario_nombre == "" or propietario_edad == "" or
                propietario_telefono == "" or propietario_correo == ""):
            mensaje.value = "Todos los campos son obligatorios"
            mensaje.color = Color.ERROR
            e.page.update()
            return

        try:
            establecimiento_dao = EstablecimientoDAO()

            if establecimiento_editar is None:
                # ---------- Registro nuevo ----------
                id = establecimiento_dao.obtener_ultimo_id() + 1
                nuevo_establecimiento = Establecimiento(
                    id=id,
                    nombre=nombre,
                    categoria_id=int(categoria),
                    direccion=direccion,
                    horario_apertura=horario_apertura,
                    horario_cierre=horario_cierre,
                    propietario_nombre=propietario_nombre,
                    propietario_edad=int(propietario_edad),
                    propietario_telefono=propietario_telefono,
                    propietario_correo=propietario_correo,
                    descripcion_corta=descripcion,
                    estado=estado,
                )
                establecimiento_dao.insertar(nuevo_establecimiento)
                mensaje.value = f"Establecimiento '{nombre}' ha sido registrado con exito"
            else:
                # ---------- Actualizacion ----------
                establecimiento_editar.nombre = nombre
                establecimiento_editar.categoria_id = int(categoria)
                establecimiento_editar.direccion = direccion
                establecimiento_editar.horario_apertura = horario_apertura
                establecimiento_editar.horario_cierre = horario_cierre
                establecimiento_editar.propietario_nombre = propietario_nombre
                establecimiento_editar.propietario_edad = int(propietario_edad)
                establecimiento_editar.propietario_telefono = propietario_telefono
                establecimiento_editar.propietario_correo = propietario_correo
                establecimiento_editar.descripcion_corta = descripcion
                establecimiento_editar.estado = estado
                establecimiento_dao.actualizar(establecimiento_editar)
                mensaje.value = f"Establecimiento '{nombre}' ha sido actualizado con exito"

            mensaje.color = Color.EXITO

            # Limpiar los campos solo si fue un registro nuevo
            if establecimiento_editar is None:
                nombre_input.value = ""
                categoria_input.value = None
                direccion_input.value = ""
                horario_apertura_input.value = ""
                horario_cierre_input.value = ""
                propietario_nombre_input.value = ""
                propietario_edad_input.value = ""
                propietario_telefono_input.value = ""
                propietario_correo_input.value = ""
                descripcion_input.value = ""

        except ValueError:
            # Manejo del error cuando el usuario escribe texto donde va un numero
            mensaje.value = "La edad del propietario debe ser un numero entero"
            mensaje.color = Color.ERROR

        except Exception as error:
            mensaje.value = f"Error al guardar el establecimiento: {error}"
            mensaje.color = Color.ERROR

        e.page.update()

    return ft.Container(
        padding=30,
        bgcolor=Color.FONDO,
        content=ft.Column(
            controls=[
                ft.Text(
                    "Editar Establecimiento" if establecimiento_editar else "Registro de nuevo Establecimiento",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=Color.DORADO
                ),
                ft.Text(
                    "Capture los datos basicos del establecimiento",
                    size=16,
                    color=Color.TEXTO_SECUNDARIO
                ),

                nombre_input,
                categoria_input,
                direccion_input,
                horario_apertura_input,
                horario_cierre_input,
                propietario_nombre_input,
                propietario_edad_input,
                propietario_telefono_input,
                propietario_correo_input,
                descripcion_input,
                estado_input,

                ft.ElevatedButton(
                    "Actualizar" if establecimiento_editar else "Guardar",
                    icon=ft.Icons.SAVE,
                    bgcolor=Color.OLIVA,
                    color=Color.FONDO,
                    on_click=guardar_establecimiento
                ),

                ft.OutlinedButton(
                    "Regresar",
                    icon=ft.Icons.ARROW_BACK,
                    style=ft.ButtonStyle(color=Color.TEXTO, side=ft.BorderSide(1, Color.BORDE)),
                    on_click=lambda e: regresar()
                ),

                mensaje
            ],
            spacing=15,
            scroll=ft.ScrollMode.AUTO
        )
    )