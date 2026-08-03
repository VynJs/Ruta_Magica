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
ROJO = "#C0564C"


def _sidebar(page: ft.Page, seleccionado: str) -> ft.Container:
    def item(icono, texto, ruta, clave):
        activo = clave == seleccionado
        return ft.Container(
            content=ft.Row([ft.Icon(icono, color=TEXT if not activo else GOLD, size=18),
                             ft.Text(texto, color=TEXT if not activo else GOLD)]),
            padding=ft.padding.symmetric(horizontal=15, vertical=10),
            bgcolor=CARD if activo else None, border_radius=6,
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
                item(ft.Icons.SETTINGS_OUTLINED, "Configuración", None, "config"),
                ft.Divider(color=BORDER),
                ft.Container(
                    content=ft.Row([ft.Icon(ft.Icons.LOGOUT, color=TEXT, size=18), ft.Text("Cerrar sesión", color=TEXT)]),
                    padding=ft.padding.symmetric(horizontal=15, vertical=10), on_click=cerrar_sesion,
                ),
            ],
            expand=True,
        ),
    )


def _tarjeta_stat(icono, titulo, valor, subtitulo) -> ft.Container:
    return ft.Container(
        content=ft.Row(
            [
                ft.Icon(icono, color=GOLD, size=26),
                ft.Column([ft.Text(titulo, color=TEXT, size=12), ft.Text(str(valor), color=TEXT, size=20, weight=ft.FontWeight.BOLD),
                           ft.Text(subtitulo, color=MUTED, size=10)], spacing=0),
            ]
        ),
        bgcolor=CARD, border=ft.border.all(1, BORDER), border_radius=10, padding=12, width=230,
    )


def admin_entretenimiento_view(page: ft.Page) -> ft.View:

    usuario = page.app_state.get("usuario")
    nombre_usuario = getattr(usuario, "nombre", "Administrador") if usuario else "Administrador"

    panel_detalle = ft.Column([ft.Text("Selecciona una experiencia de la lista para ver sus detalles.", color=MUTED)])

    def ir_a_editar(id_ent):
        page.app_state["entretenimiento_sel"] = id_ent
        page.go("/admin/entretenimiento/editar")

    def ir_a_ver(id_ent):
        page.app_state["entretenimiento_sel"] = id_ent
        page.go("/admin/entretenimiento/ver")

    def mostrar_detalle(ent):
        panel_detalle.controls.clear()
        panel_detalle.controls.extend([
            ft.Container(content=ft.Icon(ft.Icons.IMAGE_OUTLINED, size=40, color="#666"),
                         bgcolor="#DDDDDD", height=90, width=90, alignment=ft.alignment.center),
            ft.Text(ent.nombre_entretenimiento, color=TEXT, size=18, weight=ft.FontWeight.BOLD),
            ft.Text(f"ID: {ent.id}", color=MUTED, size=11),
            ft.Divider(color=BORDER),
            ft.Text("Información", color=GOLD, weight=ft.FontWeight.BOLD),
            ft.Row([ft.Text("Categoría:", color=TEXT), ft.Text(str(ent.categoria), color=MUTED)]),
            ft.Row([ft.Text("Dirección:", color=TEXT), ft.Text(str(ent.direccion), color=MUTED)]),
            ft.Row([ft.Text("Capacidad:", color=TEXT), ft.Text(str(ent.capacidad), color=MUTED)]),
            ft.Container(height=10),
            ft.Row([
                ft.ElevatedButton("Editar", icon=ft.Icons.EDIT_OUTLINED,
                                  style=ft.ButtonStyle(bgcolor=GOLD, color=BG), on_click=lambda e: ir_a_editar(ent.id)),
                ft.OutlinedButton("Ver detalle", icon=ft.Icons.VISIBILITY_OUTLINED, style=ft.ButtonStyle(color=TEXT),
                                  on_click=lambda e: ir_a_ver(ent.id)),
            ]),
        ])
        page.update()

    tabla_filas = ft.Column(spacing=0)

    def _fila(ent) -> ft.Container:
        return ft.Container(
            content=ft.Row(
                [
                    ft.Row([ft.Container(bgcolor="#DDDDDD", width=35, height=35, border_radius=6),
                            ft.Text(ent.nombre_entretenimiento, color=TEXT, width=170)]),
                    ft.Text(str(ent.categoria), color=TEXT, width=110),
                    ft.Text(str(ent.direccion), color=MUTED, width=160),
                    ft.Text(str(ent.capacidad), color=MUTED, width=90),
                    ft.Row([
                        ft.IconButton(ft.Icons.VISIBILITY_OUTLINED, icon_color=BTN_GREEN, icon_size=18,
                                      on_click=lambda e, x=ent: mostrar_detalle(x)),
                        ft.IconButton(ft.Icons.EDIT_OUTLINED, icon_color=GOLD, icon_size=18,
                                      on_click=lambda e, x=ent: ir_a_editar(x.id)),
                        ft.IconButton(ft.Icons.DELETE_OUTLINE, icon_color=ROJO, icon_size=18,
                                      on_click=lambda e, x=ent: eliminar(x.id)),
                    ]),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=ft.padding.symmetric(vertical=8),
        )

    def eliminar(id_ent):
        try:
            EntretenimientoDAO().eliminar(id_ent)
            cargar_lista()
        except Exception as ex:
            panel_detalle.controls = [ft.Text(f"No se pudo eliminar: {ex}", color=ft.Colors.RED_300)]
            page.update()

    total = [0]

    def cargar_lista():
        tabla_filas.controls.clear()
        try:
            # OJO: EntretenimientoDAO.obtener_todo() tiene un bug (ver lista de
            # errores) que hace que solo regrese el ÚLTIMO registro dentro de
            # una lista de 1 elemento en vez de todos. Aquí ya se contempla
            # ese resultado tal cual venga, sin corregir el DAO.
            entretenimientos = EntretenimientoDAO().obtener_todo()
            total[0] = len(entretenimientos) if isinstance(entretenimientos, list) else 0
            lista = entretenimientos if isinstance(entretenimientos, list) else [entretenimientos]
            for ent in lista:
                tabla_filas.controls.append(_fila(ent))
                tabla_filas.controls.append(ft.Divider(color=BORDER, height=1))
        except Exception as ex:
            tabla_filas.controls.append(ft.Text(f"No se pudo cargar: {ex}", color=ft.Colors.RED_300))
        page.update()

    cargar_lista()

    encabezado = ft.Row(
        [
            ft.Column([ft.Text("Entretenimiento", color=GOLD, size=26, weight=ft.FontWeight.BOLD),
                       ft.Text("Gestiona y administra las experiencias de entretenimiento", color=MUTED)], spacing=0),
            ft.Row([
                ft.Icon(ft.Icons.ACCOUNT_CIRCLE_OUTLINED, color=GOLD, size=32),
                ft.Column([ft.Text(f"Hola, {nombre_usuario}", color=TEXT), ft.Text("Administrador", color=MUTED, size=11)], spacing=0),
            ]),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    tarjetas = ft.Row(
        [
            _tarjeta_stat(ft.Icons.CELEBRATION_OUTLINED, "Total entretenimiento", total[0], "Registrados en la plataforma"),
            ft.ElevatedButton("+ Agregar", style=ft.ButtonStyle(bgcolor=GOLD, color=BG, shape=ft.RoundedRectangleBorder(radius=8)),
                              on_click=lambda e: page.go("/admin/entretenimiento/agregar"), height=55),
        ],
        wrap=True, spacing=12,
    )

    buscador = ft.TextField(hint_text="Buscar entretenimiento...", prefix_icon=ft.Icons.SEARCH,
                             bgcolor=BG, border_color=BORDER, color=TEXT, border_radius=8, width=260)

    lista_container = ft.Container(
        content=ft.Column(
            [
                ft.Text("Lista de entretenimiento", color=TEXT, size=16, weight=ft.FontWeight.BOLD),
                ft.Row([buscador, ft.Dropdown(hint_text="Categoría", width=140, bgcolor=BG, border_color=BORDER, color=TEXT, options=[]),
                        ft.OutlinedButton("Filtra", icon=ft.Icons.FILTER_ALT_OUTLINED, style=ft.ButtonStyle(color=TEXT))]),
                ft.Divider(color=BORDER),
                tabla_filas,
            ]
        ),
        bgcolor=CARD, border_radius=10, border=ft.border.all(1, BORDER), padding=15, expand=True,
    )

    detalle_container = ft.Container(content=panel_detalle, bgcolor=CARD, border_radius=10,
                                      border=ft.border.all(1, BORDER), padding=15, width=320)

    contenido = ft.Column(
        [
            encabezado, ft.Divider(color=GOLD), tarjetas,
            ft.Row([lista_container, detalle_container], vertical_alignment=ft.CrossAxisAlignment.START),
        ],
        spacing=20, scroll=ft.ScrollMode.AUTO, expand=True,
    )

    return ft.View(
        route="/admin/entretenimiento", bgcolor=BG, padding=0,
        controls=[ft.Row([_sidebar(page, "gestion_entretenimiento"), ft.Container(content=contenido, padding=25, expand=True)],
                          expand=True, vertical_alignment=ft.CrossAxisAlignment.START)],
    )