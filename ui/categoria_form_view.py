import flet as ft

from dao.categoria_dao import CategoriaDAO
from models.categoria import Categoria

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
                ft.Image(src="logo.png", width=33, height=33),
                ft.Text("Ruta Mágica", color=TEXT, size=12, italic=True),
                ft.Container(height=15),
                item(ft.Icons.HOME_OUTLINED, "Inicio", "/home"),
                item(ft.Icons.BAR_CHART_OUTLINED, "Reportes", "/admin/reportes"),
                item(ft.Icons.EVENT_OUTLINED, "Gestión Eventos", "/admin/eventos"),
                item(ft.Icons.STOREFRONT_OUTLINED, "Gestión Estable.", "/admin/establecimientos"),
                item(ft.Icons.CELEBRATION_OUTLINED, "Gestión Entre.", "/admin/entretenimiento"),
                ft.Container(
                    content=ft.Row([ft.Icon(ft.Icons.CATEGORY_OUTLINED, color=GOLD, size=18), ft.Text("Gestión Cat.", color=GOLD)]),
                    bgcolor=CARD, border_radius=6, padding=ft.padding.symmetric(horizontal=15, vertical=10),
                ),
                ft.Divider(color=BORDER),
                item(ft.Icons.STOREFRONT, "Establecimientos", "/establecimientos"),
                item(ft.Icons.EVENT, "Eventos", "/eventos"),
                item(ft.Icons.STAR_BORDER, "Entretenimiento", "/entretenimiento"),
                ft.Container(expand=True),
                item(ft.Icons.SETTINGS_OUTLINED, "Configuración", None),
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


def categoria_form_view(page: ft.Page, modo: str = "agregar") -> ft.View:
    """modo: 'agregar' o 'editar'. Si es editar, usa page.app_state['categoria_sel']."""

    dao = CategoriaDAO()
    categoria_existente = None

    if modo == "editar":
        id_sel = page.app_state.get("categoria_sel")
        try:
            categoria_existente = next((c for c in dao.obtener_todo() if c.id == id_sel), None)
        except Exception:
            categoria_existente = None

    nombre_field = ft.TextField(
        hint_text="Ej. Restaurantes",
        bgcolor=BG, border_color=BORDER, color=TEXT,
        value=categoria_existente.nombre if categoria_existente else "",
    )
    tipo_field = ft.TextField(
        hint_text="Ej. Establecimientos",
        bgcolor=BG, border_color=BORDER, color=TEXT,
        value=categoria_existente.tipo_categoria if categoria_existente else "",
    )
    descripcion_field = ft.TextField(
        hint_text="...", multiline=True, min_lines=3,
        bgcolor=BG, border_color=BORDER, color=TEXT,
        value=categoria_existente.descripcion if categoria_existente else "",
    )
    estado_field = ft.Dropdown(
        bgcolor=BG, border_color=BORDER, color=TEXT,
        options=[ft.dropdown.Option("Activo"), ft.dropdown.Option("Inactivo")],
        value=("Activo" if (not categoria_existente or categoria_existente.estado in (True, "true", "Activo", 1))
               else "Inactivo"),
    )

    mensaje = ft.Text("", color=ft.Colors.RED_300)

    resumen_nombre = ft.Text("—", color=MUTED)
    resumen_tipo = ft.Text("—", color=MUTED)
    resumen_desc = ft.Text("—", color=MUTED)

    def actualizar_resumen(e=None):
        resumen_nombre.value = nombre_field.value or "—"
        resumen_tipo.value = tipo_field.value or "—"
        resumen_desc.value = descripcion_field.value or "—"
        page.update()

    nombre_field.on_change = actualizar_resumen
    tipo_field.on_change = actualizar_resumen
    descripcion_field.on_change = actualizar_resumen

    def guardar(e):
        if not nombre_field.value or not tipo_field.value or not descripcion_field.value:
            mensaje.value = "Completa todos los campos obligatorios."
            page.update()
            return
        try:
            # La columna 'estado' en la base de datos es booleana, así que
            # convertimos el texto del dropdown ("Activo"/"Inactivo") a True/False.
            estado_bool = estado_field.value == "Activo"

            if modo == "agregar":
                nuevo_id = dao.obtener_ultimo_id() + 1
                categoria = Categoria(nuevo_id, nombre_field.value, tipo_field.value,
                                      descripcion_field.value, estado_bool)
                dao.insertar(categoria)
            else:
                categoria = Categoria(categoria_existente.id, nombre_field.value, tipo_field.value,
                                      descripcion_field.value, estado_bool)
                dao.actualizar(categoria)
            page.go("/admin/categorias")
        except Exception as ex:
            mensaje.value = f"Error al guardar: {ex}"
            page.update()

    encabezado = ft.Column(
        [
            ft.Row([
                ft.IconButton(ft.Icons.ARROW_BACK, icon_color=GOLD, on_click=lambda e: page.go("/admin/categorias")),
                ft.Text("Gestión de Categoría", color=GOLD, size=22, weight=ft.FontWeight.BOLD),
            ]),
            ft.Text(f"Categoría > {'Agregar categoría' if modo == 'agregar' else 'Editar categoría'}", color=MUTED, size=12),
        ],
        spacing=2,
    )

    form_info = ft.Container(
        content=ft.Column(
            [
                ft.Row([ft.Icon(ft.Icons.CATEGORY_OUTLINED, color=TEXT), ft.Text("Información categoría", color=TEXT, weight=ft.FontWeight.BOLD)]),
                ft.Text("Nombre categoria *", color=TEXT), nombre_field,
                ft.Text("Tipo categoria *", color=TEXT), tipo_field,
                ft.Text("Descripción *", color=TEXT), descripcion_field,
                ft.Text("Estado *", color=TEXT), estado_field,
                mensaje,
            ],
            spacing=6,
        ),
        bgcolor=CARD, border_radius=10, border=ft.border.all(1, BORDER), padding=20, expand=True,
    )

    resumen_box = ft.Container(
        content=ft.Column(
            [
                ft.Row([ft.Icon(ft.Icons.DESCRIPTION_OUTLINED, color=TEXT), ft.Text("Resumen de la categoría", color=TEXT, weight=ft.FontWeight.BOLD)]),
                ft.Row([ft.Text("Nombre Categoría:", color=TEXT), resumen_nombre]),
                ft.Row([ft.Text("Tipo categoría:", color=TEXT), resumen_tipo]),
                ft.Row([ft.Text("Descripción:", color=TEXT), resumen_desc]),
            ],
            spacing=8,
        ),
        bgcolor=CARD, border_radius=10, border=ft.border.all(1, BORDER), padding=20, width=320,
    )

    columna_derecha = ft.Column([resumen_box], width=320, spacing=15)

    botones = ft.Row(
        [
            ft.OutlinedButton("Cancelar", style=ft.ButtonStyle(color=TEXT), on_click=lambda e: page.go("/admin/categorias")),
            ft.Row([
                ft.OutlinedButton("Guardar borrador", style=ft.ButtonStyle(color=TEXT)),
                ft.ElevatedButton(
                    "Guardar categoría" if modo == "agregar" else "Guardar cambios",
                    style=ft.ButtonStyle(bgcolor=GOLD, color=BG), on_click=guardar,
                ),
            ]),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    contenido = ft.Column(
        [
            encabezado,
            ft.Divider(color=GOLD),
            ft.Row([form_info, columna_derecha], vertical_alignment=ft.CrossAxisAlignment.START, spacing=15),
            botones,
        ],
        spacing=20,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    return ft.View(
        route="/admin/categorias/agregar" if modo == "agregar" else "/admin/categorias/editar",
        bgcolor=BG,
        padding=0,
        controls=[
            ft.Row(
                [_sidebar(page), ft.Container(content=contenido, padding=25, expand=True)],
                expand=True,
                vertical_alignment=ft.CrossAxisAlignment.START,
            )
        ],
    )