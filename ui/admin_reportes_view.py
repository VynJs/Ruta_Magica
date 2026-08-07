import flet as ft

from dao.evento_dao import EventoDAO
from dao.establecimiento_dao import EstablecimientoDAO
from dao.entretenimiento_dao import EntretenimientoDAO
from dao.categoria_dao import CategoriaDAO

BG = "#173029"
CARD = "#28453A"
SIDEBAR = "#0F2620"
BORDER = "#4C6B5A"
GOLD = "#E3A94A"
BTN_GREEN = "#93BE72"
TEXT = "#ECECE3"
MUTED = "#AFC2B3"


def _sidebar(page: ft.Page, seleccionado: str) -> ft.Container:

    def item(icono, texto, ruta, clave):
        activo = clave == seleccionado
        return ft.Container(
            content=ft.Row([ft.Icon(icono, color=TEXT if not activo else GOLD, size=18),
                             ft.Text(texto, color=TEXT if not activo else GOLD)]),
            padding=ft.padding.symmetric(horizontal=15, vertical=10),
            bgcolor=CARD if activo else None,
            border_radius=6,
            on_click=(lambda e: page.go(ruta)) if ruta else None,
        )

    def cerrar_sesion(e):
        page.app_state["usuario"] = None
        page.app_state["rol"] = None
        page.go("/login")

    return ft.Container(
        width=210,
        bgcolor=SIDEBAR,
        padding=15,
        content=ft.Column(
            [
                ft.Row([ft.Image(src="logo.png", width=33, height=33)]),
                ft.Text("Ruta Mágica", color=TEXT, size=12, italic=True),
                ft.Container(height=15),
                item(ft.Icons.HOME_OUTLINED, "Inicio", "/home", "inicio"),
                item(ft.Icons.BAR_CHART_OUTLINED, "Reportes", "/admin/reportes", "reportes"),
                item(ft.Icons.EVENT_OUTLINED, "Gestión Eventos", "/admin/eventos", "gestion_eventos"),
                item(ft.Icons.STOREFRONT_OUTLINED, "Gestión Estable.", "/admin/establecimientos", "gestion_establecimientos"),
                item(ft.Icons.CELEBRATION_OUTLINED, "Gestión Entre.", "/admin/entretenimiento", "gestion_entretenimiento"),
                item(ft.Icons.CATEGORY_OUTLINED, "Gestión Cat.", "/admin/categorias", "gestion_categorias"),
                ft.Divider(color=BORDER),
                item(ft.Icons.STOREFRONT, "Establecimientos", "/establecimientos", "establecimientos"),
                item(ft.Icons.EVENT, "Eventos", "/eventos", "eventos"),
                item(ft.Icons.STAR_BORDER, "Entretenimiento", "/entretenimiento", "entretenimiento"),
                ft.Container(expand=True),
                item(ft.Icons.SETTINGS_OUTLINED, "Configuración", "/configuracion", "config"),
                ft.Container(height=10),
                ft.Divider(color=BORDER),
                ft.Container(
                    content=ft.Row([ft.Icon(ft.Icons.LOGOUT, color=TEXT, size=18), ft.Text("Cerrar sesión", color=TEXT)]),
                    padding=ft.padding.symmetric(horizontal=15, vertical=10),
                    on_click=cerrar_sesion,
                ),
                ft.Text("Ayuda", color=MUTED, size=12),
                ft.Text("Términos y condiciones", color=MUTED, size=12),
                ft.Text("Privacidad", color=MUTED, size=12),
                ft.Row([
                    ft.IconButton(ft.Icons.FACEBOOK, icon_color=GOLD, icon_size=16),
                    ft.IconButton(ft.Icons.CAMERA_ALT_OUTLINED, icon_color=GOLD, icon_size=16),
                    ft.IconButton(ft.Icons.EMAIL_OUTLINED, icon_color=GOLD, icon_size=16),
                    ft.IconButton(ft.Icons.CHAT_OUTLINED, icon_color=GOLD, icon_size=16),
                ]),
            ],
            expand=True,
        ),
    )


def _tarjeta_stat(icono, titulo, valor, subtitulo, destacada=False) -> ft.Container:
    return ft.Container(
        content=ft.Row(
            [
                ft.Icon(icono, color=BG if destacada else GOLD, size=30),
                ft.Column(
                    [
                        ft.Text(titulo, color=BG if destacada else TEXT, size=13),
                        ft.Text(str(valor), color=BG if destacada else TEXT, size=22, weight=ft.FontWeight.BOLD),
                        ft.Text(subtitulo, color=BG if destacada else MUTED, size=11),
                    ],
                    spacing=0,
                ),
            ]
        ),
        bgcolor=BTN_GREEN if destacada else CARD,
        border=ft.border.all(1, BORDER),
        border_radius=10,
        padding=15,
        width=270,
    )


def admin_reportes_view(page: ft.Page) -> ft.View:

    usuario = page.app_state.get("usuario")
    nombre_usuario = getattr(usuario, "nombre", "Administrador") if usuario else "Administrador"

    total_eventos = total_establecimientos = total_entretenimiento = total_categorias = 0
    try:
        total_eventos = len(EventoDAO().obtener_todo())
    except Exception:
        pass
    try:
        total_establecimientos = len(EstablecimientoDAO().obtener_todo())
    except Exception:
        pass
    try:
        total_entretenimiento = len(EntretenimientoDAO().obtener_todo())
    except Exception:
        pass
    try:
        total_categorias = len(CategoriaDAO().obtener_todo())
    except Exception:
        pass

    # --- GROUP BY: establecimientos agrupados por categoría (para la dona) ---
    try:
        establecimientos_por_categoria = EstablecimientoDAO().contar_por_categoria()
    except Exception:
        establecimientos_por_categoria = []

    # --- GROUP BY: eventos agrupados por estado (Aprobado / En revisión / Rechazado) ---
    try:
        eventos_por_estado = EventoDAO().contar_por_estado()
    except Exception:
        eventos_por_estado = []
    mapa_estados_evento = {str(estado).lower(): cantidad for estado, cantidad in eventos_por_estado}
    eventos_aprobados = mapa_estados_evento.get("aprobado", 0)
    eventos_revision = mapa_estados_evento.get("en revisión", 0) + mapa_estados_evento.get("en revision", 0)
    eventos_rechazados = mapa_estados_evento.get("rechazado", 0)

    encabezado = ft.Row(
        [
            ft.Column(
                [
                    ft.Text("Reportes", color=GOLD, size=26, weight=ft.FontWeight.BOLD),
                    ft.Text("Revisa los reportes.", color=MUTED),
                ],
                spacing=0,
            ),
            ft.Row(
                [
                    ft.Icon(ft.Icons.ACCOUNT_CIRCLE_OUTLINED, color=GOLD, size=32),
                    ft.Column(
                        [ft.Text(f"Hola, {nombre_usuario}", color=TEXT), ft.Text("Administrador", color=MUTED, size=11)],
                        spacing=0,
                    ),
                ]
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    tarjetas = ft.Row(
        [
            _tarjeta_stat(ft.Icons.EVENT_OUTLINED, "Eventos", total_eventos, "Activos"),
            _tarjeta_stat(ft.Icons.STOREFRONT_OUTLINED, "Establecimientos", total_establecimientos, "Activos"),
            _tarjeta_stat(ft.Icons.CELEBRATION_OUTLINED, "Entretenimiento", total_entretenimiento, "Activos"),
            _tarjeta_stat(ft.Icons.CATEGORY_OUTLINED, "Categorías", total_categorias, "Registrados", destacada=True),
        ],
        wrap=True,
        spacing=15,
    )

    desglose_eventos = ft.Container(
        content=ft.Column(
            [
                ft.Text("Eventos por estado", color=TEXT, size=13, weight=ft.FontWeight.BOLD),
                ft.Text("GROUP BY estado", color=MUTED, size=10, italic=True),
                ft.Row(
                    [
                        ft.Row([ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE, color=BTN_GREEN, size=16),
                                ft.Text(f"Aprobados: {eventos_aprobados}", color=TEXT, size=12)]),
                        ft.Row([ft.Icon(ft.Icons.AUTORENEW, color=GOLD, size=16),
                                ft.Text(f"En revisión: {eventos_revision}", color=TEXT, size=12)]),
                        ft.Row([ft.Icon(ft.Icons.CANCEL_OUTLINED, color="#C0564C", size=16),
                                ft.Text(f"Rechazados: {eventos_rechazados}", color=TEXT, size=12)]),
                    ],
                    spacing=20, wrap=True,
                ),
            ],
            spacing=4,
        ),
        bgcolor=CARD, border_radius=10, border=ft.border.all(1, BORDER), padding=12,
    )

    grafica = ft.Container(
        content=ft.Column(
            [
                ft.Text("Tendencia por categoría", color=TEXT, size=16, weight=ft.FontWeight.BOLD),
                ft.LineChart(
                    data_series=[],
                    height=220,
                    border=ft.border.all(1, BORDER),
                ),
            ]
        ),
        bgcolor=CARD,
        border_radius=10,
        border=ft.border.all(1, BORDER),
        padding=15,
        expand=True,
    )

    _colores_dona = [GOLD, BTN_GREEN, "#6FA8DC", "#C77DFF", "#E39A9A", "#8FD9C4"]
    secciones_dona = []
    leyenda_dona = []
    for idx, (nombre_cat, cantidad) in enumerate(establecimientos_por_categoria):
        color = _colores_dona[idx % len(_colores_dona)]
        secciones_dona.append(
            ft.PieChartSection(value=cantidad, color=color, radius=45)
        )
        leyenda_dona.append(
            ft.Row([
                ft.Container(width=10, height=10, bgcolor=color, border_radius=3),
                ft.Text(f"{nombre_cat} ({cantidad})", color=TEXT, size=11),
            ], spacing=6)
        )

    donut = ft.Container(
        content=ft.Column(
            [
                ft.Text("Establecimientos por categoría", color=TEXT, size=16, weight=ft.FontWeight.BOLD),
                ft.Text("GROUP BY categoria — agrupa y cuenta con una sola consulta", color=MUTED, size=10, italic=True),
                ft.PieChart(sections=secciones_dona, center_space_radius=40, height=160) if secciones_dona
                else ft.Text("Sin establecimientos registrados todavía.", color=MUTED, size=12),
                ft.Column(leyenda_dona, spacing=4),
            ]
        ),
        bgcolor=CARD,
        border_radius=10,
        border=ft.border.all(1, BORDER),
        padding=15,
        width=300,
    )

    columnas_tabla = ["Nombre del propietario", "Establecimiento", "Número Del Establecimiento", "Dirección", "Categoría", ""]
    filas = []
    try:
        establecimientos = EstablecimientoDAO().obtener_todo()[:6]
        for est in establecimientos:
            filas.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(getattr(est, "nombre_propietario", "—"), color=TEXT)),
                    ft.DataCell(ft.Text(getattr(est, "nombre_establecimiento", "—"), color=TEXT)),
                    ft.DataCell(ft.Text(str(getattr(est, "telefono", "—")), color=TEXT)),
                    ft.DataCell(ft.Text(getattr(est, "direccion", "—"), color=TEXT)),
                    ft.DataCell(ft.Text(str(getattr(est, "categoria", "—")), color=TEXT)),
                    ft.DataCell(ft.TextButton("Detalles", style=ft.ButtonStyle(color=GOLD))),
                ])
            )
    except Exception:
        pass

    tabla = ft.Container(
        content=ft.Column(
            [
                ft.Text("Propietarios Recientes", color=TEXT, size=16, weight=ft.FontWeight.BOLD),
                ft.Row(
                    [ft.DataTable(
                        columns=[ft.DataColumn(ft.Text(c, color=MUTED)) for c in columnas_tabla],
                        rows=filas,
                    )],
                    scroll=ft.ScrollMode.AUTO,
                ),
            ]
        ),
        bgcolor=CARD,
        border_radius=10,
        border=ft.border.all(1, BORDER),
        padding=15,
    )

    contenido = ft.Column(
        [
            encabezado,
            ft.Divider(color=GOLD),
            tarjetas,
            desglose_eventos,
            ft.Row([grafica, donut], vertical_alignment=ft.CrossAxisAlignment.START),
            tabla,
        ],
        spacing=20,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    return ft.View(
        route="/admin/reportes",
        bgcolor=BG,
        padding=0,
        controls=[
            ft.Row(
                [_sidebar(page, "reportes"), ft.Container(content=contenido, padding=25, expand=True)],
                expand=True,
                vertical_alignment=ft.CrossAxisAlignment.START,
            )
        ],
    )