import flet as ft

from dao.establecimiento_dao import EstablecimientoDAO

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
                ft.Container(
                    content=ft.Row([ft.Icon(ft.Icons.STOREFRONT_OUTLINED, color=GOLD, size=18), ft.Text("Establecimientos", color=GOLD)]),
                    bgcolor=CARD, border_radius=6, padding=ft.padding.symmetric(horizontal=15, vertical=10),
                ),
                item(ft.Icons.CELEBRATION_OUTLINED, "Entretenimiento", "/admin/entretenimiento"),
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


def establecimiento_detalle_view(page: ft.Page) -> ft.View:

    id_sel = page.app_state.get("establecimiento_sel")
    est = None
    try:
        est = next((e for e in EstablecimientoDAO().obtener_todo() if e.id == id_sel), None)
    except Exception:
        est = None

    if est is None:
        cuerpo = ft.Text("No se encontró el establecimiento seleccionado.", color=ft.Colors.RED_300)
    else:
        banner = ft.Container(
            content=ft.Stack(
                [
                    ft.Container(bgcolor="#000000", height=250, border_radius=10),
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Container(content=ft.Text(str(est.categoria), color=BG, size=11), bgcolor=BTN_GREEN,
                                             border_radius=12, padding=ft.padding.symmetric(horizontal=10, vertical=3)),
                                ft.Text(est.nombre_establecimiento, color=TEXT, size=32, weight=ft.FontWeight.BOLD),
                                ft.Text(est.descripcion_corta or "", color=MUTED, size=13, width=500),
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
                    ft.Text("Acerca del establecimiento", color=TEXT, weight=ft.FontWeight.BOLD, size=16),
                    ft.Text(getattr(est, "descripcion_Completa", "—"), color=MUTED),
                    ft.Row([ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE, color=BTN_GREEN, size=16), ft.Text(est.caracteristica_1 or "—", color=MUTED)]),
                    ft.Row([ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE, color=BTN_GREEN, size=16), ft.Text(est.caracteristica_2 or "—", color=MUTED)]),
                    ft.Row([ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE, color=BTN_GREEN, size=16), ft.Text(est.caracteristica_3 or "—", color=MUTED)]),
                ],
                spacing=6,
            ),
            bgcolor=CARD, border_radius=10, border=ft.border.all(1, BORDER), padding=18, expand=True,
        )

        info = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Información del establecimiento", color=TEXT, weight=ft.FontWeight.BOLD, size=16),
                    ft.Row([ft.Icon(ft.Icons.PHONE_OUTLINED, color=GOLD, size=16), ft.Text("Teléfono", color=TEXT), ft.Text(str(est.telefono), color=MUTED)]),
                    ft.Row([ft.Icon(ft.Icons.ACCESS_TIME, color=GOLD, size=16), ft.Text("Horario", color=TEXT), ft.Text(f"{est.horario_inicio} - {est.horario_fin}", color=MUTED)]),
                    ft.Row([ft.Icon(ft.Icons.CATEGORY_OUTLINED, color=GOLD, size=16), ft.Text("Categoría", color=TEXT), ft.Text(str(est.categoria), color=MUTED)]),
                    ft.Row([ft.Icon(ft.Icons.LOCATION_ON_OUTLINED, color=GOLD, size=16), ft.Text("Dirección", color=TEXT), ft.Text(str(est.direccion), color=MUTED)]),
                    ft.ElevatedButton("Ver en Google Maps", icon=ft.Icons.MAP_OUTLINED, style=ft.ButtonStyle(bgcolor=CARD, color=TEXT)),
                ],
                spacing=8,
            ),
            bgcolor=CARD, border_radius=10, border=ft.border.all(1, BORDER), padding=18, width=320,
        )

        galeria = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Galería del establecimiento", color=TEXT, weight=ft.FontWeight.BOLD, size=16),
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
                    ft.Text(f"Servicios: {est.servicios or '—'}", color=MUTED, size=12),
                    ft.Text(f"Precios: {est.rango_precios or '—'}", color=MUTED, size=12),
                ],
                spacing=6,
            ),
            bgcolor=CARD, border_radius=10, border=ft.border.all(1, BORDER), padding=18, width=320,
        )

        menu = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Menu", color=TEXT, weight=ft.FontWeight.BOLD, size=16),
                    ft.Row([ft.Container(bgcolor=BG, border=ft.border.all(1, BORDER), height=110, width=180, border_radius=8)
                            for _ in range(4)], wrap=True, spacing=10),
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
                menu,
            ],
            spacing=15,
        )

    encabezado = ft.Column(
        [
            ft.Row([ft.IconButton(ft.Icons.ARROW_BACK, icon_color=GOLD, on_click=lambda e: page.go("/admin/establecimientos")),
                    ft.Text("Gestión de Evento", color=GOLD, size=22, weight=ft.FontWeight.BOLD)]),
            ft.Text("Eventos > Ver evento", color=MUTED, size=12),
        ],
        spacing=2,
    )

    contenido = ft.Column([encabezado, ft.Divider(color=GOLD), cuerpo], spacing=15, scroll=ft.ScrollMode.AUTO, expand=True)

    return ft.View(
        route="/admin/establecimientos/ver", bgcolor=BG, padding=0,
        controls=[ft.Row([_sidebar(page), ft.Container(content=contenido, padding=25, expand=True)],
                          expand=True, vertical_alignment=ft.CrossAxisAlignment.START)],
    )