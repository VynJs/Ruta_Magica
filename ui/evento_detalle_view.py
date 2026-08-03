import flet as ft

from dao.evento_dao import EventoDAO

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
                item(ft.icons.HOME_OUTLINED, "Inicio", "/home"),
                item(ft.icons.BAR_CHART_OUTLINED, "Reportes", "/admin/reportes"),
                ft.Container(
                    content=ft.Row([ft.Icon(ft.icons.EVENT_OUTLINED, color=GOLD, size=18), ft.Text("Eventos", color=GOLD)]),
                    bgcolor=CARD, border_radius=6, padding=ft.padding.symmetric(horizontal=15, vertical=10),
                ),
                item(ft.icons.STOREFRONT_OUTLINED, "Establecimientos", "/admin/establecimientos"),
                item(ft.icons.CELEBRATION_OUTLINED, "Entretenimiento", "/admin/entretenimiento"),
                ft.Container(expand=True),
                item(ft.icons.SETTINGS_OUTLINED, "Configuración", None),
                ft.Divider(color=BORDER),
                ft.Container(
                    content=ft.Row([ft.Icon(ft.icons.LOGOUT, color=TEXT, size=18), ft.Text("Cerrar sesión", color=TEXT)]),
                    padding=ft.padding.symmetric(horizontal=15, vertical=10), on_click=cerrar_sesion,
                ),
            ],
            expand=True,
        ),
    )


def _dato_destacado(titulo, descripcion) -> ft.Container:
    return ft.Container(
        content=ft.Column(
            [ft.Icon(ft.icons.STAR_BORDER, color=BTN_GREEN),
             ft.Text(titulo, color=TEXT, weight=ft.FontWeight.BOLD, size=13),
             ft.Text(descripcion, color=MUTED, size=11)],
            spacing=4,
        ),
        bgcolor=CARD, border=ft.border.all(1, BORDER), border_radius=10, padding=12, width=230,
    )


def evento_detalle_view(page: ft.Page) -> ft.View:

    id_sel = page.app_state.get("evento_sel")
    evento = None
    try:
        evento = next((ev for ev in EventoDAO().obtener_todo() if ev.id == id_sel), None)
    except Exception:
        evento = None

    if evento is None:
        cuerpo = ft.Text("No se encontró el evento seleccionado.", color=ft.colors.RED_300)
    else:
        banner = ft.Container(
            content=ft.Stack(
                [
                    ft.Container(bgcolor="#000000", height=250, border_radius=10),
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Container(content=ft.Text(str(evento.categoria), color=BG, size=11), bgcolor=BTN_GREEN,
                                             border_radius=12, padding=ft.padding.symmetric(horizontal=10, vertical=3)),
                                ft.Text(evento.nombre_evento, color=TEXT, size=32, weight=ft.FontWeight.BOLD),
                                ft.Text(evento.descripcion_corta or "", color=MUTED, size=13, width=500),
                            ],
                            spacing=8,
                        ),
                        padding=25,
                    ),
                ]
            ),
            height=250,
        )

        destacados = ft.Row(
            [
                _dato_destacado("Característica 1", evento.caracteristica_1 or "—"),
                _dato_destacado("Característica 2", evento.caracteristica_2 or "—"),
                _dato_destacado("Característica 3", evento.caracteristica_3 or "—"),
            ],
            wrap=True, spacing=15,
        )

        acerca = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Acerca del evento", color=TEXT, weight=ft.FontWeight.BOLD, size=16),
                    ft.Text(evento.descripcion_completa or "—", color=MUTED),
                ]
            ),
            bgcolor=CARD, border_radius=10, border=ft.border.all(1, BORDER), padding=18, expand=True,
        )

        info = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Información del evento", color=TEXT, weight=ft.FontWeight.BOLD, size=16),
                    ft.Row([ft.Icon(ft.icons.CALENDAR_TODAY, color=GOLD, size=16), ft.Text("Fecha", color=TEXT), ft.Text(str(evento.fecha), color=MUTED)]),
                    ft.Row([ft.Icon(ft.icons.ACCESS_TIME, color=GOLD, size=16), ft.Text("Horario", color=TEXT), ft.Text(f"{evento.horario_inicio} - {evento.horario_fin}", color=MUTED)]),
                    ft.Row([ft.Icon(ft.icons.CATEGORY_OUTLINED, color=GOLD, size=16), ft.Text("Categoría", color=TEXT), ft.Text(str(evento.categoria), color=MUTED)]),
                    ft.Row([ft.Icon(ft.icons.LOCATION_ON_OUTLINED, color=GOLD, size=16), ft.Text("Ubicación", color=TEXT), ft.Text(str(evento.ubicacion), color=MUTED)]),
                    ft.ElevatedButton("Ver en Google Maps", icon=ft.icons.MAP_OUTLINED,
                                      style=ft.ButtonStyle(bgcolor=CARD, color=TEXT)),
                ],
                spacing=8,
            ),
            bgcolor=CARD, border_radius=10, border=ft.border.all(1, BORDER), padding=18, width=320,
        )

        galeria = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Galería del evento", color=TEXT, weight=ft.FontWeight.BOLD, size=16),
                    ft.Row([ft.Container(bgcolor="#DDDDDD", width=140, height=110, border_radius=8) for _ in range(4)], wrap=True, spacing=10),
                    ft.OutlinedButton("Ver todas las imágenes", icon=ft.icons.IMAGE_OUTLINED, style=ft.ButtonStyle(color=TEXT)),
                ],
                spacing=10,
            ),
            bgcolor=CARD, border_radius=10, border=ft.border.all(1, BORDER), padding=18,
        )

        cuerpo = ft.Column(
            [
                banner,
                destacados,
                ft.Row([acerca, info], vertical_alignment=ft.CrossAxisAlignment.START, spacing=15),
                galeria,
            ],
            spacing=15,
        )

    encabezado = ft.Column(
        [
            ft.Row([ft.IconButton(ft.icons.ARROW_BACK, icon_color=GOLD, on_click=lambda e: page.go("/admin/eventos")),
                    ft.Text("Gestión de Evento", color=GOLD, size=22, weight=ft.FontWeight.BOLD)]),
            ft.Text("Eventos > Ver evento", color=MUTED, size=12),
        ],
        spacing=2,
    )

    contenido = ft.Column([encabezado, ft.Divider(color=GOLD), cuerpo], spacing=15, scroll=ft.ScrollMode.AUTO, expand=True)

    return ft.View(
        route="/admin/eventos/ver", bgcolor=BG, padding=0,
        controls=[ft.Row([_sidebar(page), ft.Container(content=contenido, padding=25, expand=True)],
                          expand=True, vertical_alignment=ft.CrossAxisAlignment.START)],
    )