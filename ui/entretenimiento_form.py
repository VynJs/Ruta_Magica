import flet as ft

from config.tema import Color
from models.entretenimiento import Entretenimiento
from dao.entretenimiento_dao import EntretenimientoDAO
from dao.categoria_dao import CategoriaDAO

def _estilo_campo(control):
    control.border_color = Color.BORDE
    control.focused_border_color = Color.DORADO
    control.color = Color.TEXTO
    control.label_style = ft.TextStyle(color=Color.TEXTO_SECUNDARIO)
    control.bgcolor = Color.TARJETA
    control.border_radius = 8
    return control

def entretenimiento_form(regresar, entretenimiento_editar=None):
    categoria_dao = CategoriaDAO()
    categorias = categoria_dao.obtener_todo(tipo="entretenimiento")
    opciones_categoria = [
        ft.dropdown.Option(key=str(c.id), text=c.nombre) for c in categorias
    ]

    nombre_input = _estilo_campo(ft.TextField(
        label="Nombre de la experiencia: ",
        width=400,
    ))
    categoria_input = _estilo_campo(ft.Dropdown(
        label="Categoria: ",
        width=400,
        options=opciones_categoria
    ))
    ubicacion_input = _estilo_campo(ft.TextField(
        label="Ubicacion: ",
        width=400,
    ))
    horario_apertura_input = _estilo_campo(ft.TextField(
        label="Horario de apertura: ",
        width=400,
    ))
    horario_cierre_input = _estilo_campo(ft.TextField(
        label="Horario de cierre: ",
        width=400,
    ))
    capacidad_min_input = _estilo_campo(ft.TextField(
        label="Capacidad minima: ",
        width=400,
        value="1",
    ))
    capacidad_max_input = _estilo_campo(ft.TextField(
        label="Capacidad maxima: ",
        width=400,
        value="20",
    ))
    nivel_fisico_input = _estilo_campo(ft.Dropdown(
        label="Nivel fisico recomendado: ",
        width=400,
        value="moderado",
        options=[
            ft.dropdown.Option(key="bajo", text="Bajo"),
            ft.dropdown.Option(key="moderado", text="Moderado"),
            ft.dropdown.Option(key="alto", text="Alto"),
        ]
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

    # Si viene un entretenimiento a editar, precargamos los campos
    if entretenimiento_editar is not None:
        nombre_input.value = entretenimiento_editar.nombre
        categoria_input.value = str(entretenimiento_editar.categoria_id)
        ubicacion_input.value = entretenimiento_editar.ubicacion
        horario_apertura_input.value = entretenimiento_editar.horario_apertura
        horario_cierre_input.value = entretenimiento_editar.horario_cierre
        capacidad_min_input.value = str(entretenimiento_editar.capacidad_min)
        capacidad_max_input.value = str(entretenimiento_editar.capacidad_max)
        nivel_fisico_input.value = entretenimiento_editar.nivel_fisico
        descripcion_input.value = entretenimiento_editar.descripcion_corta
        estado_input.value = entretenimiento_editar.estado

    def guardar_entretenimiento(e):
        # recuperar los valores de los TextField
        nombre = nombre_input.value
        categoria = categoria_input.value
        ubicacion = ubicacion_input.value
        horario_apertura = horario_apertura_input.value
        horario_cierre = horario_cierre_input.value
        capacidad_min = capacidad_min_input.value
        capacidad_max = capacidad_max_input.value
        nivel_fisico = nivel_fisico_input.value
        descripcion = descripcion_input.value
        estado = estado_input.value

        # Validar que los campos no esten vacios
        if (nombre == "" or categoria is None or ubicacion == "" or
                capacidad_min == "" or capacidad_max == ""):
            mensaje.value = "Todos los campos son obligatorios"
            mensaje.color = Color.ERROR
            e.page.update()
            return

        try:
            entretenimiento_dao = EntretenimientoDAO()

            if entretenimiento_editar is None:
                # ---------- Registro nuevo ----------
                id = entretenimiento_dao.obtener_ultimo_id() + 1
                nuevo_entretenimiento = Entretenimiento(
                    id=id,
                    nombre=nombre,
                    categoria_id=int(categoria),
                    ubicacion=ubicacion,
                    horario_apertura=horario_apertura,
                    horario_cierre=horario_cierre,
                    capacidad_min=int(capacidad_min),
                    capacidad_max=int(capacidad_max),
                    nivel_fisico=nivel_fisico,
                    descripcion_corta=descripcion,
                    estado=estado,
                )
                entretenimiento_dao.insertar(nuevo_entretenimiento)
                mensaje.value = f"Entretenimiento '{nombre}' ha sido registrado con exito"
            else:
                # ---------- Actualizacion ----------
                entretenimiento_editar.nombre = nombre
                entretenimiento_editar.categoria_id = int(categoria)
                entretenimiento_editar.ubicacion = ubicacion
                entretenimiento_editar.horario_apertura = horario_apertura
                entretenimiento_editar.horario_cierre = horario_cierre
                entretenimiento_editar.capacidad_min = int(capacidad_min)
                entretenimiento_editar.capacidad_max = int(capacidad_max)
                entretenimiento_editar.nivel_fisico = nivel_fisico
                entretenimiento_editar.descripcion_corta = descripcion
                entretenimiento_editar.estado = estado
                entretenimiento_dao.actualizar(entretenimiento_editar)
                mensaje.value = f"Entretenimiento '{nombre}' ha sido actualizado con exito"

            mensaje.color = Color.EXITO

            # Limpiar los campos solo si fue un registro nuevo
            if entretenimiento_editar is None:
                nombre_input.value = ""
                categoria_input.value = None
                ubicacion_input.value = ""
                horario_apertura_input.value = ""
                horario_cierre_input.value = ""
                capacidad_min_input.value = "1"
                capacidad_max_input.value = "20"
                descripcion_input.value = ""

        except ValueError:
            mensaje.value = "La capacidad minima y maxima deben ser numeros enteros"
            mensaje.color = Color.ERROR

        except Exception as error:
            mensaje.value = f"Error al guardar el entretenimiento: {error}"
            mensaje.color = Color.ERROR

        e.page.update()

    return ft.Container(
        padding=30,
        bgcolor=Color.FONDO,
        content=ft.Column(
            controls=[
                ft.Text(
                    "Editar Entretenimiento" if entretenimiento_editar else "Registro de nuevo Entretenimiento",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=Color.DORADO
                ),
                ft.Text(
                    "Capture los datos basicos de la experiencia",
                    size=16,
                    color=Color.TEXTO_SECUNDARIO
                ),

                nombre_input,
                categoria_input,
                ubicacion_input,
                horario_apertura_input,
                horario_cierre_input,
                capacidad_min_input,
                capacidad_max_input,
                nivel_fisico_input,
                descripcion_input,
                estado_input,

                ft.ElevatedButton(
                    "Actualizar" if entretenimiento_editar else "Guardar",
                    icon=ft.Icons.SAVE,
                    bgcolor=Color.OLIVA,
                    color=Color.FONDO,
                    on_click=guardar_entretenimiento
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