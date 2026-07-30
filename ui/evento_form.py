import flet as ft

from config.tema import Color
from models.evento import Evento
from dao.evento_dao import EventoDAO
from dao.categoria_dao import CategoriaDAO

def _estilo_campo(control):
    control.border_color = Color.BORDE
    control.focused_border_color = Color.DORADO
    control.color = Color.TEXTO
    control.label_style = ft.TextStyle(color=Color.TEXTO_SECUNDARIO)
    control.bgcolor = Color.TARJETA
    control.border_radius = 8
    return control

def evento_form(regresar, evento_editar=None):
    categoria_dao = CategoriaDAO()
    categorias = categoria_dao.obtener_todo(tipo="evento")
    opciones_categoria = [
        ft.dropdown.Option(key=str(c.id), text=c.nombre) for c in categorias
    ]

    nombre_input = _estilo_campo(ft.TextField(
        label="Nombre del evento: ",
        width=400,
    ))
    categoria_input = _estilo_campo(ft.Dropdown(
        label="Categoria: ",
        width=400,
        options=opciones_categoria
    ))
    fecha_input = _estilo_campo(ft.TextField(
        label="Fecha (AAAA-MM-DD): ",
        width=400,
    ))
    hora_inicio_input = _estilo_campo(ft.TextField(
        label="Hora de inicio: ",
        width=400,
    ))
    hora_fin_input = _estilo_campo(ft.TextField(
        label="Hora de fin: ",
        width=400,
    ))
    ubicacion_input = _estilo_campo(ft.TextField(
        label="Ubicacion: ",
        width=400,
    ))
    organizador_nombre_input = _estilo_campo(ft.TextField(
        label="Nombre del organizador: ",
        width=400,
    ))
    organizador_edad_input = _estilo_campo(ft.TextField(
        label="Edad del organizador: ",
        width=400,
    ))
    organizador_telefono_input = _estilo_campo(ft.TextField(
        label="Telefono del organizador: ",
        width=400,
    ))
    organizador_correo_input = _estilo_campo(ft.TextField(
        label="Correo del organizador: ",
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

    # Si viene un evento a editar, precargamos los campos
    if evento_editar is not None:
        nombre_input.value = evento_editar.nombre
        categoria_input.value = str(evento_editar.categoria_id)
        fecha_input.value = evento_editar.fecha
        hora_inicio_input.value = evento_editar.hora_inicio
        hora_fin_input.value = evento_editar.hora_fin
        ubicacion_input.value = evento_editar.ubicacion
        organizador_nombre_input.value = evento_editar.organizador_nombre
        organizador_edad_input.value = str(evento_editar.organizador_edad)
        organizador_telefono_input.value = evento_editar.organizador_telefono
        organizador_correo_input.value = evento_editar.organizador_correo
        descripcion_input.value = evento_editar.descripcion_corta
        estado_input.value = evento_editar.estado

    def guardar_evento(e):
        # recuperar los valores de los TextField
        nombre = nombre_input.value
        categoria = categoria_input.value
        fecha = fecha_input.value
        hora_inicio = hora_inicio_input.value
        hora_fin = hora_fin_input.value
        ubicacion = ubicacion_input.value
        organizador_nombre = organizador_nombre_input.value
        organizador_edad = organizador_edad_input.value
        organizador_telefono = organizador_telefono_input.value
        organizador_correo = organizador_correo_input.value
        descripcion = descripcion_input.value
        estado = estado_input.value

        # Validar que los campos no esten vacios
        if (nombre == "" or categoria is None or fecha == "" or ubicacion == "" or
                organizador_nombre == "" or organizador_edad == "" or
                organizador_telefono == "" or organizador_correo == ""):
            mensaje.value = "Todos los campos son obligatorios"
            mensaje.color = Color.ERROR
            e.page.update()
            return

        try:
            evento_dao = EventoDAO()

            if evento_editar is None:
                # ---------- Registro nuevo ----------
                id = evento_dao.obtener_ultimo_id() + 1
                nuevo_evento = Evento(
                    id=id,
                    nombre=nombre,
                    categoria_id=int(categoria),
                    fecha=fecha,
                    hora_inicio=hora_inicio,
                    hora_fin=hora_fin,
                    ubicacion=ubicacion,
                    organizador_nombre=organizador_nombre,
                    organizador_edad=int(organizador_edad),
                    organizador_telefono=organizador_telefono,
                    organizador_correo=organizador_correo,
                    descripcion_corta=descripcion,
                    estado=estado,
                )
                evento_dao.insertar(nuevo_evento)
                mensaje.value = f"Evento '{nombre}' ha sido registrado con exito"
            else:
                # ---------- Actualizacion ----------
                evento_editar.nombre = nombre
                evento_editar.categoria_id = int(categoria)
                evento_editar.fecha = fecha
                evento_editar.hora_inicio = hora_inicio
                evento_editar.hora_fin = hora_fin
                evento_editar.ubicacion = ubicacion
                evento_editar.organizador_nombre = organizador_nombre
                evento_editar.organizador_edad = int(organizador_edad)
                evento_editar.organizador_telefono = organizador_telefono
                evento_editar.organizador_correo = organizador_correo
                evento_editar.descripcion_corta = descripcion
                evento_editar.estado = estado
                evento_dao.actualizar(evento_editar)
                mensaje.value = f"Evento '{nombre}' ha sido actualizado con exito"

            mensaje.color = Color.EXITO

            # Limpiar los campos solo si fue un registro nuevo
            if evento_editar is None:
                nombre_input.value = ""
                categoria_input.value = None
                fecha_input.value = ""
                hora_inicio_input.value = ""
                hora_fin_input.value = ""
                ubicacion_input.value = ""
                organizador_nombre_input.value = ""
                organizador_edad_input.value = ""
                organizador_telefono_input.value = ""
                organizador_correo_input.value = ""
                descripcion_input.value = ""

        except ValueError:
            mensaje.value = "La edad del organizador debe ser un numero entero"
            mensaje.color = Color.ERROR

        except Exception as error:
            mensaje.value = f"Error al guardar el evento: {error}"
            mensaje.color = Color.ERROR

        e.page.update()

    return ft.Container(
        padding=30,
        bgcolor=Color.FONDO,
        content=ft.Column(
            controls=[
                ft.Text(
                    "Editar Evento" if evento_editar else "Registro de nuevo Evento",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=Color.DORADO
                ),
                ft.Text(
                    "Capture los datos basicos del evento",
                    size=16,
                    color=Color.TEXTO_SECUNDARIO
                ),

                nombre_input,
                categoria_input,
                fecha_input,
                hora_inicio_input,
                hora_fin_input,
                ubicacion_input,
                organizador_nombre_input,
                organizador_edad_input,
                organizador_telefono_input,
                organizador_correo_input,
                descripcion_input,
                estado_input,

                ft.ElevatedButton(
                    "Actualizar" if evento_editar else "Guardar",
                    icon=ft.Icons.SAVE,
                    bgcolor=Color.OLIVA,
                    color=Color.FONDO,
                    on_click=guardar_evento
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