import flet as ft

from dao.entretenimiento_dao import EntretenimientoDAO

BG = "#173029"
CARD = "#28453A"
BORDER = "#4C6B5A"
GOLD = "#E3A94A"
BTN_GREEN = "#93BE72"
TEXT = "#ECECE3"
MUTED = "#AFC2B3"


def _tarjeta(nombre: str, on_click=None) -> ft.Container:
    return ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Icon(ft.Icons.IMAGE_OUTLINED, size=45, color="#666"),
                    bgcolor="#DDDDDD",
                    height=150,
                    alignment=ft.alignment.center,
                ),
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Text(nombre, color=TEXT, size=14),
                            ft.Icon(ft.Icons.CHEVRON_RIGHT, color=GOLD),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    bgcolor=BG,
                    border=ft.border.all(1, GOLD),
                    padding=10,
                ),
            ],
            spacing=0,
        ),
        width=300,
        border=ft.border.all(1, BORDER),
        on_click=on_click,
        ink=True,
    )


def entretenimiento_view(page: ft.Page) -> ft.View:

    buscador = ft.TextField(
        hint_text="Buscar entretenimiento...",
        prefix_icon=ft.Icons.SEARCH,
        bgcolor=BG, border_color=BORDER, color=TEXT, border_radius=8,
        width=300,
    )
    categoria_dd = ft.Dropdown(
        hint_text="Categoria",
        bgcolor=BG, border_color=BORDER, color=TEXT,
        width=160,
        options=[],
    )

    filas_por_categoria = ft.Column(spacing=25)

    def ir_a_detalle(id_ent):
        page.app_state["entretenimiento_sel"] = id_ent
        page.go("/entretenimiento/ver")

    def cargar():
        filas_por_categoria.controls.clear()
        try:
            resultado = EntretenimientoDAO().obtener_todo()
            entretenimientos = resultado if isinstance(resultado, list) else [resultado]
        except Exception as ex:
            filas_por_categoria.controls.append(
                ft.Text(f"No se pudo cargar la información: {ex}", color=ft.Colors.RED_300)
            )
            return

        if not entretenimientos:
            filas_por_categoria.controls.append(
                ft.Text("No hay experiencias de entretenimiento registradas todavía.", color=MUTED)
            )
            return

        agrupados = {}
        for ent in entretenimientos:
            clave = ent.categoria if ent.categoria else "Sin categoría"
            agrupados.setdefault(clave, []).append(ent)

        for categoria_nombre, lista in agrupados.items():
            filas_por_categoria.controls.append(
                ft.Row([ft.Icon(ft.Icons.CELEBRATION_OUTLINED, color=BTN_GREEN),
                        ft.Text(categoria_nombre, color=BTN_GREEN, size=18, weight=ft.FontWeight.BOLD)])
            )
            filas_por_categoria.controls.append(
                ft.Row(
                    [_tarjeta(ent.nombre_entretenimiento, on_click=lambda e, id_e=ent.id: ir_a_detalle(id_e)) for ent in lista],
                    wrap=True,
                    spacing=20,
                )
            )

    cargar()

    encabezado = ft.Row(
        [
            ft.IconButton(ft.Icons.MENU, icon_color=GOLD, on_click=lambda e: page.go("/home")),
            ft.Column(
                [
                    ft.Text("R⁘M", size=22, color=BTN_GREEN, weight=ft.FontWeight.BOLD),
                    ft.Text("Ruta Mágica", size=12, color=TEXT, italic=True),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            ft.Row(
                [
                    ft.Column([ft.Icon(ft.Icons.FAVORITE_BORDER, color=GOLD), ft.Text("Favoritos", color=TEXT, size=11)]),
                    ft.Column([ft.Icon(ft.Icons.ACCOUNT_CIRCLE_OUTLINED, color=GOLD), ft.Text("Cuenta", color=TEXT, size=11)]),
                ],
                spacing=15,
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    titulo = ft.Row([ft.Icon(ft.Icons.CELEBRATION_OUTLINED, color=TEXT, size=26),
                     ft.Text("Entretenimiento", color=TEXT, size=26, weight=ft.FontWeight.BOLD)])

    barra_filtros = ft.Row(
        [buscador, categoria_dd, ft.OutlinedButton("Filtros", icon=ft.Icons.FILTER_ALT_OUTLINED,
                                                     style=ft.ButtonStyle(color=TEXT))],
        alignment=ft.MainAxisAlignment.END,
    )

    footer = ft.Column(
        [
            ft.Divider(color=BORDER),
            ft.Row(
                [
                    ft.Text("Ruta Mágica", color=GOLD),
                    ft.Row([
                        ft.TextButton("Ayuda", style=ft.ButtonStyle(color=MUTED)),
                        ft.TextButton("Términos y Condiciones", style=ft.ButtonStyle(color=MUTED)),
                        ft.TextButton("Privacidad", style=ft.ButtonStyle(color=MUTED)),
                        ft.TextButton("Contáctanos", style=ft.ButtonStyle(color=MUTED)),
                    ]),
                    ft.Row([
                        ft.IconButton(ft.Icons.FACEBOOK, icon_color=GOLD),
                        ft.IconButton(ft.Icons.CAMERA_ALT_OUTLINED, icon_color=GOLD),
                        ft.IconButton(ft.Icons.EMAIL_OUTLINED, icon_color=GOLD),
                        ft.IconButton(ft.Icons.CHAT_OUTLINED, icon_color=GOLD),
                    ]),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
        ]
    )

    return ft.View(
        route="/entretenimiento",
        bgcolor=BG,
        padding=25,
        controls=[
            encabezado,
            ft.Divider(color=BORDER),
            titulo,
            ft.Divider(color=BORDER),
            barra_filtros,
            ft.Container(height=10),
            filas_por_categoria,
            ft.Container(height=20),
            footer,
        ],
        scroll=ft.ScrollMode.AUTO,
    )