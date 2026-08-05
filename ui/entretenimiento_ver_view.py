import flet as ft

from dao.entretenimiento_dao import EntretenimientoDAO

BG = "#173029"
CARD = "#28453A"
BORDER = "#4C6B5A"
GOLD = "#E3A94A"
BTN_GREEN = "#93BE72"
TEXT = "#ECECE3"
MUTED = "#AFC2B3"


def _encabezado(page: ft.Page) -> ft.Row:
    return ft.Row(
        [
            ft.IconButton(ft.Icons.ARROW_BACK, icon_color=GOLD, on_click=lambda e: page.go("/entretenimiento")),
            ft.Column(
                [ft.Image(src="logo.png", width=33, height=33),
                 ft.Text("Ruta Mágica", size=12, color=TEXT, italic=True)],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            ft.Row([
                ft.Column([ft.Icon(ft.Icons.FAVORITE_BORDER, color=GOLD), ft.Text("Favoritos", color=TEXT, size=11)]),
                ft.Column([ft.Icon(ft.Icons.ACCOUNT_CIRCLE_OUTLINED, color=GOLD), ft.Text("Cuenta", color=TEXT, size=11)]),
            ], spacing=15),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )


def _footer() -> ft.Column:
    return ft.Column(
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


def entretenimiento_ver_view(page: ft.Page) -> ft.View:

    id_sel = page.app_state.get("entretenimiento_sel")
    ent = None
    try:
        resultado = EntretenimientoDAO().obtener_todo()
        lista = resultado if isinstance(resultado, list) else [resultado]
        ent = next((x for x in lista if getattr(x, "id", None) == id_sel), None)
    except Exception:
        ent = None

    if ent is None:
        cuerpo = ft.Text("No se encontró la experiencia seleccionada.", color=ft.Colors.RED_300)
    else:
        banner = ft.Container(
            content=ft.Stack(
                [
                    ft.Container(bgcolor="#000000", height=250, border_radius=10),
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Container(content=ft.Text(str(ent.categoria), color=BG, size=11), bgcolor=BTN_GREEN,
                                             border_radius=12, padding=ft.padding.symmetric(horizontal=10, vertical=3)),
                                ft.Text(ent.nombre_entretenimiento, color=TEXT, size=32, weight=ft.FontWeight.BOLD),
                                ft.Text(ent.descripcion_corta or "", color=MUTED, size=13, width=500),
                            ],
                            spacing=8,
                        ),
                        padding=25,
                    ),
                ]
            ),
            height=250,
        )

        acerca = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Acerca de esta experiencia", color=TEXT, weight=ft.FontWeight.BOLD, size=16),
                    ft.Text(ent.descripcion_completa or "—", color=MUTED),
                    ft.Row([ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE, color=BTN_GREEN, size=16), ft.Text(ent.caracteristica_1 or "—", color=MUTED)]),
                    ft.Row([ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE, color=BTN_GREEN, size=16), ft.Text(ent.caracteristica_2 or "—", color=MUTED)]),
                    ft.Row([ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE, color=BTN_GREEN, size=16), ft.Text(ent.caracteristica_3 or "—", color=MUTED)]),
                ],
                spacing=6,
            ),
            bgcolor=CARD, border_radius=10, border=ft.border.all(1, BORDER), padding=18, expand=True,
        )

        info = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Información del entretenimiento", color=TEXT, weight=ft.FontWeight.BOLD, size=16),
                    ft.Row([ft.Icon(ft.Icons.LOCATION_ON_OUTLINED, color=GOLD, size=16), ft.Text("Ubicación", color=TEXT), ft.Text(str(ent.direccion), color=MUTED)]),
                    ft.Row([ft.Icon(ft.Icons.ACCESS_TIME, color=GOLD, size=16), ft.Text("Horario", color=TEXT), ft.Text(f"{ent.horario_inicio} - {ent.horario_fin}", color=MUTED)]),
                    ft.Row([ft.Icon(ft.Icons.CATEGORY_OUTLINED, color=GOLD, size=16), ft.Text("Categoría", color=TEXT), ft.Text(str(ent.categoria), color=MUTED)]),
                    ft.Row([ft.Icon(ft.Icons.GROUPS_OUTLINED, color=GOLD, size=16), ft.Text("Capacidad", color=TEXT), ft.Text(str(ent.capacidad), color=MUTED)]),
                    ft.ElevatedButton("Ver ruta en Google Maps", icon=ft.Icons.MAP_OUTLINED, style=ft.ButtonStyle(bgcolor=CARD, color=TEXT)),
                ],
                spacing=8,
            ),
            bgcolor=CARD, border_radius=10, border=ft.border.all(1, BORDER), padding=18, width=320,
        )

        galeria = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Galería de la experiencia", color=TEXT, weight=ft.FontWeight.BOLD, size=16),
                    ft.Row([ft.Container(bgcolor="#DDDDDD", width=140, height=110, border_radius=8) for _ in range(4)], wrap=True, spacing=10),
                ],
                spacing=10,
            ),
            bgcolor=CARD, border_radius=10, border=ft.border.all(1, BORDER), padding=18,
        )

        cuerpo = ft.Column(
            [
                banner,
                ft.Row([acerca, info], vertical_alignment=ft.CrossAxisAlignment.START, spacing=15),
                galeria,
            ],
            spacing=15,
        )

    return ft.View(
        route="/entretenimiento/ver",
        bgcolor=BG,
        padding=25,
        controls=[
            _encabezado(page),
            ft.Divider(color=BORDER),
            cuerpo,
            ft.Container(height=20),
            _footer(),
        ],
        scroll=ft.ScrollMode.AUTO,
    )