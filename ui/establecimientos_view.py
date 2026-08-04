import flet as ft

from dao.establecimiento_dao import EstablecimientoDAO

BG = "#173029"
CARD = "#28453A"
BORDER = "#4C6B5A"
GOLD = "#E3A94A"
BTN_GREEN = "#93BE72"
TEXT = "#ECECE3"
MUTED = "#AFC2B3"


def _tarjeta(nombre: str, estrellas: int = 5, on_click=None) -> ft.Container:
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
                            ft.Column(
                                [
                                    ft.Text(nombre, color=TEXT, size=14),
                                    ft.Text("★" * estrellas, color=GOLD, size=12),
                                ],
                                spacing=2,
                            ),
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


def establecimientos_view(page: ft.Page) -> ft.View:

    buscador = ft.TextField(
        hint_text="Buscar establecimiento...",
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

    def ir_a_detalle(id_est):
        page.app_state["establecimiento_sel"] = id_est
        page.go("/establecimiento/ver")

    def cargar():
        filas_por_categoria.controls.clear()
        try:
            dao = EstablecimientoDAO()
            establecimientos = dao.obtener_todo()
        except Exception as ex:
            filas_por_categoria.controls.append(
                ft.Text(f"No se pudo cargar la información: {ex}", color=ft.Colors.RED_300)
            )
            return

        if not establecimientos:
            filas_por_categoria.controls.append(
                ft.Text("No hay establecimientos registrados todavía.", color=MUTED)
            )
            return

        # Agrupa por el campo 'categoria' (nombre de la categoría en la vista)
        agrupados = {}
        for est in establecimientos:
            clave = est.categoria if est.categoria else "Sin categoría"
            agrupados.setdefault(clave, []).append(est)

        for categoria_nombre, lista in agrupados.items():
            filas_por_categoria.controls.append(
                ft.Row([ft.Icon(ft.Icons.RESTAURANT_MENU, color=BTN_GREEN),
                        ft.Text(categoria_nombre, color=BTN_GREEN, size=18, weight=ft.FontWeight.BOLD)])
            )
            filas_por_categoria.controls.append(
                ft.Row(
                    [_tarjeta(e.nombre_establecimiento, on_click=lambda ev, id_e=e.id: ir_a_detalle(id_e)) for e in lista],
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
                    ft.Image(src="logo.png", width=33, height=33),
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

    titulo = ft.Row([ft.Icon(ft.Icons.STOREFRONT_OUTLINED, color=TEXT, size=26),
                     ft.Text("Establecimientos", color=TEXT, size=26, weight=ft.FontWeight.BOLD)])

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
                    ft.Row([ft.Image(src="logo.png", width=20, height=20), ft.Text("Ruta Mágica", color=GOLD)], spacing=6),
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
        route="/establecimientos",
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