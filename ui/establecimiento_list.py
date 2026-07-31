import flet as ft

from config.tema import Color
from dao.establecimiento_dao import EstablecimientoDAO

def establecimiento_list(regresar, editar, agregar):
    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID", color=Color.TEXTO_SECUNDARIO)),
            ft.DataColumn(ft.Text("Nombre", color=Color.TEXTO_SECUNDARIO)),
            ft.DataColumn(ft.Text("Propietario", color=Color.TEXTO_SECUNDARIO)),
            ft.DataColumn(ft.Text("Direccion", color=Color.TEXTO_SECUNDARIO)),
            ft.DataColumn(ft.Text("Estado", color=Color.TEXTO_SECUNDARIO)),
            ft.DataColumn(ft.Text("")),
            ft.DataColumn(ft.Text(""))
        ],
        rows=[],
        heading_row_color=Color.FONDO,
        data_row_color={ft.ControlState.DEFAULT: Color.TARJETA},
    )

    mensaje = ft.Text()

    def eliminar_establecimiento(e, establecimiento):
        try:
            establecimiento_dao = EstablecimientoDAO()
            establecimiento_dao.eliminar(establecimiento.id)
            mensaje.value = f"Establecimiento '{establecimiento.nombre}' eliminado con exito"
            mensaje.color = Color.EXITO
            cargar_establecimientos()
        except Exception as error:
            mensaje.value = f"Error al eliminar el establecimiento: {error}"
            mensaje.color = Color.ERROR
        e.page.update()

    def cargar_establecimientos():
        try:
            establecimiento_dao = EstablecimientoDAO()
            establecimientos = establecimiento_dao.obtener_todo()

            tabla.rows.clear()

            for establecimiento in establecimientos:
                tabla.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(establecimiento.id), color=Color.TEXTO)),
                            ft.DataCell(ft.Text(establecimiento.nombre, color=Color.TEXTO)),
                            ft.DataCell(ft.Text(establecimiento.propietario_nombre, color=Color.TEXTO)),
                            ft.DataCell(ft.Text(establecimiento.direccion, color=Color.TEXTO)),
                            ft.DataCell(ft.Text(establecimiento.estado, color=Color.TEXTO)),
                            ft.DataCell(
                                ft.IconButton(
                                    icon=ft.Icons.EDIT,
                                    icon_color=Color.DORADO,
                                    on_click=lambda e, est=establecimiento: editar(est)
                                )
                            ),
                            ft.DataCell(
                                ft.IconButton(
                                    icon=ft.Icons.DELETE,
                                    icon_color=Color.ERROR,
                                    on_click=lambda e, est=establecimiento: eliminar_establecimiento(e, est)
                                )
                            ),
                        ]
                    )
                )
        except Exception as error:
            mensaje.value = f"Error al consultar establecimientos: {error}"
            mensaje.color = Color.ERROR

    cargar_establecimientos()

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
                                    "Establecimientos Registrados",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color=Color.DORADO
                                ),
                                ft.Text(
                                    "Consulta de restaurantes, cafeterias, hoteles, etc.",
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