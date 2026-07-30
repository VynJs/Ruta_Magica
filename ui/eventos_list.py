import flet as ft

from config.tema import Color
from dao.evento_dao import EventoDAO

def eventos_list(regresar, editar, agregar):
    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID", color=Color.TEXTO_SECUNDARIO)),
            ft.DataColumn(ft.Text("Nombre", color=Color.TEXTO_SECUNDARIO)),
            ft.DataColumn(ft.Text("Fecha", color=Color.TEXTO_SECUNDARIO)),
            ft.DataColumn(ft.Text("Ubicacion", color=Color.TEXTO_SECUNDARIO)),
            ft.DataColumn(ft.Text("Estado", color=Color.TEXTO_SECUNDARIO)),
            ft.DataColumn(ft.Text("")),
            ft.DataColumn(ft.Text(""))
        ],
        rows=[],
        heading_row_color=Color.FONDO,
        data_row_color={ft.ControlState.DEFAULT: Color.TARJETA},
    )

    mensaje = ft.Text()

    def eliminar_evento(e, evento):
        try:
            evento_dao = EventoDAO()
            evento_dao.eliminar(evento.id)
            mensaje.value = f"Evento '{evento.nombre}' eliminado con exito"
            mensaje.color = Color.EXITO
            cargar_eventos()
        except Exception as error:
            mensaje.value = f"Error al eliminar el evento: {error}"
            mensaje.color = Color.ERROR
        e.page.update()

    def cargar_eventos():
        try:
            evento_dao = EventoDAO()
            eventos = evento_dao.obtener_todo()

            tabla.rows.clear()

            for evento in eventos:
                tabla.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(evento.id), color=Color.TEXTO)),
                            ft.DataCell(ft.Text(evento.nombre, color=Color.TEXTO)),
                            ft.DataCell(ft.Text(evento.fecha, color=Color.TEXTO)),
                            ft.DataCell(ft.Text(evento.ubicacion, color=Color.TEXTO)),
                            ft.DataCell(ft.Text(evento.estado, color=Color.TEXTO)),
                            ft.DataCell(
                                ft.IconButton(
                                    icon=ft.Icons.EDIT,
                                    icon_color=Color.DORADO,
                                    on_click=lambda e, ev=evento: editar(ev)
                                )
                            ),
                            ft.DataCell(
                                ft.IconButton(
                                    icon=ft.Icons.DELETE,
                                    icon_color=Color.ERROR,
                                    on_click=lambda e, ev=evento: eliminar_evento(e, ev)
                                )
                            ),
                        ]
                    )
                )
        except Exception as error:
            mensaje.value = f"Error al consultar eventos: {error}"
            mensaje.color = Color.ERROR

    cargar_eventos()

    return ft.Container(
        padding=30,
        bgcolor=Color.FONDO,
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text(
                                    "Eventos Registrados",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color=Color.DORADO
                                ),
                                ft.Text(
                                    "Consulta de eventos culturales, deportivos y sociales",
                                    color=Color.TEXTO_SECUNDARIO
                                )
                            ]
                        ),
                        ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    "Agregar",
                                    icon=ft.Icons.ADD,
                                    bgcolor=Color.DORADO,
                                    color=Color.FONDO,
                                    on_click=lambda e: agregar()
                                ),
                                ft.OutlinedButton(
                                    "Regresar",
                                    icon=ft.Icons.ARROW_BACK,
                                    style=ft.ButtonStyle(color=Color.TEXTO, side=ft.BorderSide(1, Color.BORDE)),
                                    on_click=regresar
                                )
                            ]
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),

                ft.Divider(color=Color.BORDE),

                ft.Container(
                    content=tabla,
                    bgcolor=Color.TARJETA,
                    border=ft.border.all(
                        1,
                        Color.BORDE
                    ),
                    border_radius=10,
                    padding=10
                ),

                mensaje
            ],
            spacing=20,
            scroll=ft.ScrollMode.AUTO
        )
    )