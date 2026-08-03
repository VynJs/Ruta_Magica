import flet as ft

from dao.categoria_dao import CategoriaDAO

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
                    padding=ft.padding.symmetric(horizontal=15, vertical=10),
                    on_click=cerrar_sesion,
                ),
            ],
            expand=True,
        ),
    )


def _tarjeta_stat(icono, titulo, valor, subtitulo, destacada=False) -> ft.Container:
    return ft.Container(
        content=ft.Row(
            [
                ft.Icon(icono, color=BG if destacada else GOLD, size=26),
                ft.Column(
                    [
                        ft.Text(titulo, color=BG if destacada else TEXT, size=12),
                        ft.Text(str(valor), color=BG if destacada else TEXT, size=20, weight=ft.FontWeight.BOLD),
                        ft.Text(subtitulo, color=BG if destacada else MUTED, size=10),
                    ],
                    spacing=0,
                ),
            ]
        ),
        bgcolor=BTN_GREEN if destacada else CARD,
        border=ft.border.all(1, BORDER),
        border_radius=10,
        padding=12,
        width=240,
    )


def admin_categorias_view(page: ft.Page) -> ft.View:

    usuario = page.app_state.get("usuario")
    nombre_usuario = getattr(usuario, "nombre", "Administrador") if usuario else "Administrador"

    panel_detalle = ft.Column(
        [ft.Text("Selecciona una categoría de la lista para ver sus detalles.", color=MUTED)]
    )

    def mostrar_detalle(categoria):
        panel_detalle.controls.clear()
        panel_detalle.controls.extend([
            ft.Container(
                content=ft.Icon(ft.Icons.IMAGE_OUTLINED, size=40, color="#666"),
                bgcolor="#DDDDDD", height=90, width=90, alignment=ft.alignment.center,
            ),
            ft.Text(categoria.nombre, color=TEXT, size=18, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=ft.Text(str(categoria.estado), color=BG, size=11),
                bgcolor=BTN_GREEN, border_radius=12, padding=ft.padding.symmetric(horizontal=10, vertical=3),
            ),
            ft.Text(f"ID: {categoria.id}", color=MUTED, size=11),
            ft.Divider(color=BORDER),
            ft.Text("Información", color=GOLD, weight=ft.FontWeight.BOLD),
            ft.Row([ft.Text("Nombre de la categoría:", color=TEXT), ft.Text(categoria.nombre, color=MUTED)]),
            ft.Row([ft.Text("Tipo:", color=TEXT), ft.Text(str(categoria.tipo_categoria), color=MUTED)]),
            ft.Row([ft.Text("Descripción:", color=TEXT), ft.Text(categoria.descripcion or "—", color=MUTED)]),
            ft.Row([ft.Text("Estado:", color=TEXT), ft.Text(str(categoria.estado), color=MUTED)]),
            ft.Container(height=10),
            ft.ElevatedButton(
                "Editar información",
                icon=ft.Icons.EDIT_OUTLINED,
                style=ft.ButtonStyle(bgcolor=GOLD, color=BG),
                on_click=lambda e: ir_a_editar(categoria.id),
            ),
        ])
        page.update()

    def ir_a_editar(id_categoria):
        page.app_state["categoria_sel"] = id_categoria
        page.go("/admin/categorias/editar")

    tabla_filas = ft.Column(spacing=0)

    def _fila(categoria) -> ft.Container:
        color_estado = BTN_GREEN if str(categoria.estado).lower() in ("activo", "true", "1") else ROJO
        return ft.Container(
            content=ft.Row(
                [
                    ft.Row([
                        ft.Container(bgcolor="#DDDDDD", width=35, height=35, border_radius=6),
                        ft.Text(categoria.nombre, color=TEXT, width=140),
                    ]),
                    ft.Text(str(categoria.tipo_categoria), color=TEXT, width=110),
                    ft.Text(categoria.descripcion or "—", color=MUTED, width=260, size=12),
                    ft.Container(
                        content=ft.Text(str(categoria.estado), color=BG, size=11),
                        bgcolor=color_estado, border_radius=10, padding=ft.padding.symmetric(horizontal=8, vertical=2),
                        width=80,
                    ),
                    ft.Row([
                        ft.IconButton(ft.Icons.VISIBILITY_OUTLINED, icon_color=BTN_GREEN, icon_size=18,
                                      on_click=lambda e, c=categoria: mostrar_detalle(c)),
                        ft.IconButton(ft.Icons.EDIT_OUTLINED, icon_color=GOLD, icon_size=18,
                                      on_click=lambda e, c=categoria: ir_a_editar(c.id)),
                        ft.IconButton(ft.Icons.DELETE_OUTLINE, icon_color=ROJO, icon_size=18,
                                      on_click=lambda e, c=categoria: eliminar(c.id)),
                    ]),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=ft.padding.symmetric(vertical=8),
        )

    def eliminar(id_categoria):
        try:
            CategoriaDAO().eliminar(id_categoria)
            cargar_lista()
        except Exception as ex:
            panel_detalle.controls = [ft.Text(f"No se pudo eliminar: {ex}", color=ft.Colors.RED_300)]
            page.update()

    total_categorias = [0]

    def cargar_lista():
        tabla_filas.controls.clear()
        try:
            categorias = CategoriaDAO().obtener_todo()
            total_categorias[0] = len(categorias)
            for cat in categorias:
                tabla_filas.controls.append(_fila(cat))
                tabla_filas.controls.append(ft.Divider(color=BORDER, height=1))
        except Exception as ex:
            tabla_filas.controls.append(ft.Text(f"No se pudo cargar: {ex}", color=ft.Colors.RED_300))
        page.update()

    cargar_lista()

    encabezado = ft.Row(
        [
            ft.Column(
                [
                    ft.Text("Categorías", color=GOLD, size=26, weight=ft.FontWeight.BOLD),
                    ft.Text("Gestiona y administra todo el contenido de las categorías", color=MUTED),
                ],
                spacing=0,
            ),
            ft.Row([
                ft.Icon(ft.Icons.ACCOUNT_CIRCLE_OUTLINED, color=GOLD, size=32),
                ft.Column([ft.Text(f"Hola, {nombre_usuario}", color=TEXT), ft.Text("Administrador", color=MUTED, size=11)], spacing=0),
            ]),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    tarjetas = ft.Row(
        [
            _tarjeta_stat(ft.Icons.STOREFRONT_OUTLINED, "Total categorías (Establecimientos)", total_categorias[0], "Registrados en la plataforma"),
            _tarjeta_stat(ft.Icons.EVENT_OUTLINED, "Total categorías (Eventos)", total_categorias[0], "Registrados en la plataforma"),
            _tarjeta_stat(ft.Icons.CELEBRATION_OUTLINED, "Total categorías (Entretenimiento)", total_categorias[0], "Activos y visibles"),
            ft.ElevatedButton(
                "+ Agregar",
                style=ft.ButtonStyle(bgcolor=GOLD, color=BG, shape=ft.RoundedRectangleBorder(radius=8)),
                on_click=lambda e: page.go("/admin/categorias/agregar"),
                height=55,
            ),
        ],
        wrap=True,
        spacing=15,
    )

    buscador = ft.TextField(hint_text="Buscar categoría...", prefix_icon=ft.Icons.SEARCH,
                             bgcolor=BG, border_color=BORDER, color=TEXT, border_radius=8, width=280)

    lista_container = ft.Container(
        content=ft.Column(
            [
                ft.Row([ft.Text("Lista de categorías", color=TEXT, size=16, weight=ft.FontWeight.BOLD)]),
                ft.Row([buscador, ft.Dropdown(hint_text="Tipo", width=140, bgcolor=BG, border_color=BORDER, color=TEXT, options=[]),
                        ft.OutlinedButton("Filtra", icon=ft.Icons.FILTER_ALT_OUTLINED, style=ft.ButtonStyle(color=TEXT))]),
                ft.Divider(color=BORDER),
                tabla_filas,
            ]
        ),
        bgcolor=CARD, border_radius=10, border=ft.border.all(1, BORDER), padding=15, expand=True,
    )

    detalle_container = ft.Container(
        content=panel_detalle,
        bgcolor=CARD, border_radius=10, border=ft.border.all(1, BORDER), padding=15, width=320,
    )

    contenido = ft.Column(
        [
            encabezado,
            ft.Divider(color=GOLD),
            tarjetas,
            ft.Row([lista_container, detalle_container], vertical_alignment=ft.CrossAxisAlignment.START),
        ],
        spacing=20,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    return ft.View(
        route="/admin/categorias",
        bgcolor=BG,
        padding=0,
        controls=[
            ft.Row(
                [_sidebar(page, "gestion_categorias"), ft.Container(content=contenido, padding=25, expand=True)],
                expand=True,
                vertical_alignment=ft.CrossAxisAlignment.START,
            )
        ],
    )