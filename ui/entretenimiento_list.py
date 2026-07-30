import flet as ft

from config.tema import Color
from dao.entretenimiento_dao import EntretenimientoDAO

def entretenimientos_list(regresar, editar, agregar):
    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID", color=Color.TEXTO_SECUNDARIO)),
            ft.DataColumn(ft.Text("Nombre", color=Color.TEXTO_SECUNDARIO)),
            ft.DataColumn(ft.Text("Ubicacion", color=Color.TEXTO_SECUNDARIO)),
            ft.DataColumn(ft.Text("Capacidad", color=Color.TEXTO_SECUNDARIO)),
            ft.DataColumn(ft.Text("Estado", color=Color.TEXTO_SECUNDARIO)),
            ft.DataColumn(ft.Text("")),
            ft.DataColumn(ft.Text(""))
        ],
        rows=[],
        heading_row_color=Color.FONDO,
        data_row_color={ft.ControlState.DEFAULT: Color.TARJETA},
    )

    mensaje = ft.Text()

    def eliminar_entretenimiento(e, entretenimiento):
        try:
            entretenimiento_dao = EntretenimientoDAO()
            entretenimiento_dao.eliminar(entretenimiento.id)
            mensaje.value = f"Entretenimiento '{entretenimiento.nombre}' eliminado con exito"
            mensaje.color = Color.EXITO
            cargar_entretenimientos()
        except Exception as error:
            mensaje.value = f"Error al eliminar el entretenimiento: {error}"
            mensaje.color = Color.ERROR
        e.page.update()

    def cargar_entretenimientos():
        try:
            entretenimiento_dao = EntretenimientoDAO()
            entretenimientos = entretenimiento_dao.obtener_todo()

            tabla.rows.clear()

            for entretenimiento in entretenimientos:
                tabla.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(entretenimiento.id), color=Color.TEXTO)),
                            ft.DataCell(ft.Text(entretenimiento.nombre, color=Color.TEXTO)),
                            ft.DataCell(ft.Text(entretenimiento.ubicacion, color=Color.TEXTO)),
                            ft.DataCell(ft.Text(f"{entretenimiento.capacidad_min}-{entretenimiento.capacidad_max}", color=Color.TEXTO)),
                            ft.DataCell(ft.Text(entretenimiento.estado, color=Color.TEXTO)),
                            ft.DataCell(
                                ft.IconButton(
                                    icon=ft.Icons.EDIT,
                                    icon_color=Color.DORADO,
                                    on_click=lambda e, ent=entretenimiento: editar(ent)
                                )
                            ),
                            ft.DataCell(
                                ft.IconButton(
                                    icon=ft.Icons.DELETE,
                                    icon_color=Color.ERROR,
                                    on_click=lambda e, ent=entretenimiento: eliminar_entretenimiento(e, ent)
                                )
                            ),
                        ]
                    )
                )
        except Exception as error:
            mensaje.value = f"Error al consultar entretenimiento: {error}"
            mensaje.color = Color.ERROR

    cargar_entretenimientos()

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
                                    "Entretenimiento Registrado",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color=Color.DORADO
                                ),
                                ft.Text(
                                    "Consulta de actividades y experiencias turisticas",
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