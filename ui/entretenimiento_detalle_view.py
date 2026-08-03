import flet as ft

from dao.entretenimiento_dao import EntretenimientoDAO

BG = "#173029"
CARD = "#28453A"
SIDEBAR = "#0F2620"
BORDER = "#4C6B5A"
GOLD = "#E3A94A"
BTN_GREEN = "#93BE72"
TEXT = "#ECECE3"
MUTED = "#AFC2B3"


def _sidebar(page: ft.Page) -> ft.Container:
    def item(icono, texto, ruta):
        return ft.Container(
            content=ft.Row([ft.Icon(icono, color=TEXT, size=18), ft.Text(texto, color=TEXT)]),
            padding=ft.padding.symmetric(horizontal=15, vertical=10),
            on_click=(lambda e: page.go(ruta)) if ruta else None,
        )

    def cerrar_sesion(e):
        page.app_state["usuario"] = None
        page.go("/login")

    return ft.Container(
        width=210, bgcolor=SIDEBAR, padding=15,
        content=ft.Column(
            [
                ft.Text("R⁘M", color=BTN_GREEN, size=22, weight=ft.FontWeight.BOLD),
                ft.Text("Ruta Mágica", color=TEXT, size=12, italic=True),
                ft.Container(height=15),
                item(ft.Icons.HOME_OUTLINED, "Inicio", "/home"),
                item(ft.Icons.BAR_CHART_OUTLINED, "Reportes", "/admin/reportes"),
                item(ft.Icons.EVENT_OUTLINED, "Eventos", "/admin/eventos"),
                item(ft.Icons.STOREFRONT_OUTLINED, "Establecimientos", "/admin/establecimientos"),
                ft.Container(
                    content=ft.Row([ft.Icon(ft.Icons.CELEBRATION_OUTLINED, color=GOLD, size=18), ft.Text("Entretenimiento", color=GOLD)]),
                    bgcolor=CARD, border_radius=6, padding=ft.padding.symmetric(horizontal=15, vertical=10),
                ),
                ft.Container(expand=True),
                item(ft.Icons.SETTINGS_OUTLINED, "Configuración", None),
                ft.Divider(color=BORDER),
                ft.Container(
                    content=ft.Row([ft.Icon(ft.Icons.LOGOUT, color=TEXT, size=18), ft.Text("Cerrar sesión", color=TEXT)]),
                    padding=ft.padding.symmetric(horizontal=15, vertical=10), on_click=cerrar_sesion,
                ),
            ],
            expand=True,
        ),
    )


def _recomendacion(texto) -> ft.Container:
    return ft.Container(
        content=ft.Column(
            [ft.Icon(ft.Icons.HIKING, color=BTN_GREEN), ft.Text(texto or "—", color=TEXT, size=12, text_align=ft.TextAlign.CENTER)],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=6,
        ),
        bgcolor=CARD, border=ft.border.all(1, BORDER), border_radius=10, padding=12, width=200,
    )


def entretenimiento_detalle_view(page: ft.Page) -> ft.View:

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
                    ft.Row([ft.Icon(ft.Icons.GROUPS_OUTLINED, color=GOLD, size=16), ft.Text("Capacidad Rec.", color=TEXT), ft.Text(str(ent.capacidad), color=MUTED)]),
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
                    ft.OutlinedButton("Ver todas las imágenes", icon=ft.Icons.IMAGE_OUTLINED, style=ft.ButtonStyle(color=TEXT)),
                ],
                spacing=10,
            ),
            bgcolor=CARD, border_radius=10, border=ft.border.all(1, BORDER), padding=18, expand=True,
        )

        adicional = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Información adicional", color=TEXT, weight=ft.FontWeight.BOLD, size=16),
                    ft.Text("Servicios:", color=MUTED, size=12),
                    ft.Row([ft.Icon(ft.Icons.CHECK, color=BTN_GREEN, size=16) for _ in range(3)]),
                    ft.Text(f"Precios: {ent.precio or '—'}", color=MUTED, size=12),
                ],
                spacing=6,
            ),
            bgcolor=CARD, border_radius=10, border=ft.border.all(1, BORDER), padding=18, width=320,
        )

        recomendaciones = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Recomendaciones para visitantes", color=TEXT, weight=ft.FontWeight.BOLD, size=16),
                    ft.Row([
                        _recomendacion(ent.recomendacion_1), _recomendacion(ent.recomendacion_2),
                        _recomendacion(ent.recomendacion_3), _recomendacion(ent.recomendacion_4),
                    ], wrap=True, spacing=12),
                ],
                spacing=10,
            ),
            bgcolor=CARD, border_radius=10, border=ft.border.all(1, BORDER), padding=18,
        )

        cuerpo = ft.Column(
            [
                banner,
                ft.Row([acerca, info], vertical_alignment=ft.CrossAxisAlignment.START, spacing=15),
                ft.Row([galeria, adicional], vertical_alignment=ft.CrossAxisAlignment.START, spacing=15),
                recomendaciones,
            ],
            spacing=15,
        )

    encabezado = ft.Column(
        [
            ft.Row([ft.IconButton(ft.Icons.ARROW_BACK, icon_color=GOLD, on_click=lambda e: page.go("/admin/entretenimiento")),
                    ft.Text("Gestión de entretenimiento", color=GOLD, size=22, weight=ft.FontWeight.BOLD)]),
            ft.Text("Entretenimiento > ver entretenimiento", color=MUTED, size=12),
        ],
        spacing=2,
    )

    contenido = ft.Column([encabezado, ft.Divider(color=GOLD), cuerpo], spacing=15, scroll=ft.ScrollMode.AUTO, expand=True)

    return ft.View(
        route="/admin/entretenimiento/ver", bgcolor=BG, padding=0,
        controls=[ft.Row([_sidebar(page), ft.Container(content=contenido, padding=25, expand=True)],
                          expand=True, vertical_alignment=ft.CrossAxisAlignment.START)],
    )