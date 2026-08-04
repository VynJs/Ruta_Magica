import flet as ft

from dao.evento_dao import EventoDAO
from dao.categoria_dao import CategoriaDAO
from models.evento import Evento

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
                ft.Container(
                    content=ft.Row([ft.Icon(ft.Icons.EVENT_OUTLINED, color=GOLD, size=18), ft.Text("Gestión Eventos", color=GOLD)]),
                    bgcolor=CARD, border_radius=6, padding=ft.padding.symmetric(horizontal=15, vertical=10),
                ),
                item(ft.Icons.STOREFRONT_OUTLINED, "Gestión Estable.", "/admin/establecimientos"),
                item(ft.Icons.CELEBRATION_OUTLINED, "Gestión Entre.", "/admin/entretenimiento"),
                item(ft.Icons.CATEGORY_OUTLINED, "Gestión Cat.", "/admin/categorias"),
                ft.Divider(color=BORDER),
                item(ft.Icons.STOREFRONT, "Establecimientos", "/establecimientos"),
                item(ft.Icons.EVENT, "Eventos", "/eventos"),
                item(ft.Icons.STAR_BORDER, "Entretenimiento", "/entretenimiento"),
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


def _campo(label, hint="", multiline=False, value="") -> tuple:
    field = ft.TextField(hint_text=hint, bgcolor=BG, border_color=BORDER, color=TEXT,
                          multiline=multiline, min_lines=3 if multiline else 1, value=value)
    return ft.Column([ft.Text(label, color=TEXT, size=12), field], spacing=3), field


def evento_form_view(page: ft.Page, modo: str = "agregar") -> ft.View:

    dao = EventoDAO()
    evento_existente = None
    if modo == "editar":
        id_sel = page.app_state.get("evento_sel")
        try:
            evento_existente = next((ev for ev in dao.obtener_todo() if ev.id == id_sel), None)
        except Exception:
            evento_existente = None

    ex = evento_existente

    col_nombre, nombre_field = _campo("Nombre del evento*", "Ej. Huamantlada", value=getattr(ex, "nombre_evento", ""))
    try:
        categorias_registradas = CategoriaDAO().obtener_todo()
    except Exception:
        categorias_registradas = []
    opciones_categoria = [ft.dropdown.Option(c.nombre) for c in categorias_registradas
                          if str(getattr(c, "tipo_categoria", "")).strip().lower() in ("eventos", "evento")]
    if not opciones_categoria:
        opciones_categoria = [ft.dropdown.Option(c.nombre) for c in categorias_registradas]

    categoria_field = ft.Dropdown(hint_text="Selecciona una categoria", bgcolor=BG, border_color=BORDER, color=TEXT,
                                   options=opciones_categoria,
                                   value=str(getattr(ex, "categoria", "")) or None)
    fecha_field = ft.TextField(hint_text="10/08/2026", bgcolor=BG, border_color=BORDER, color=TEXT,
                                value=str(getattr(ex, "fecha", "")))
    hora_inicio_field = ft.TextField(hint_text="Ej. 10:00 am", bgcolor=BG, border_color=BORDER, color=TEXT,
                                      value=str(getattr(ex, "horario_inicio", "")))
    hora_fin_field = ft.TextField(hint_text="Ej. 02:00 pm", bgcolor=BG, border_color=BORDER, color=TEXT,
                                   value=str(getattr(ex, "horario_fin", "")))
    col_ubicacion, ubicacion_field = _campo("Ubicación*", "Ej. Calle 5Pte. #123 Huamantla Tlaxcala",
                                             value=getattr(ex, "ubicacion", ""))

    col_organizador, organizador_field = _campo("Nombre del organizador *", "Ej. Jose Luis Ortiz Huerta",
                                                  value=getattr(ex, "nombre_organizador", ""))
    edad_field = ft.TextField(hint_text="Ej. 26", bgcolor=BG, border_color=BORDER, color=TEXT,
                               value=str(getattr(ex, "edad", "")))
    telefono_field = ft.TextField(hint_text="Ej. 247 124 2456", bgcolor=BG, border_color=BORDER, color=TEXT,
                                   value=str(getattr(ex, "telefono", "")))
    correo_field = ft.TextField(hint_text="Ej. contacto@gmail.com", bgcolor=BG, border_color=BORDER, color=TEXT,
                                 value=getattr(ex, "correo", ""))

    col_desc_corta, desc_corta_field = _campo("Descripción corta *", "Cuéntanos sobre tu evento...", True,
                                                value=getattr(ex, "descripcion_corta", ""))
    col_desc_completa, desc_completa_field = _campo("Descripción completa *", "Describe con detalle el evento...", True,
                                                      value=getattr(ex, "descripcion_completa", ""))

    caract1 = ft.TextField(hint_text="Característica de tu evento...", bgcolor=BG, border_color=BORDER, color=TEXT,
                            value=getattr(ex, "caracteristica_1", ""))
    caract2 = ft.TextField(hint_text="Característica de tu evento...", bgcolor=BG, border_color=BORDER, color=TEXT,
                            value=getattr(ex, "caracteristica_2", ""))
    caract3 = ft.TextField(hint_text="Característica de tu evento...", bgcolor=BG, border_color=BORDER, color=TEXT,
                            value=getattr(ex, "caracteristica_3", ""))

    instagram_field = ft.TextField(hint_text="@usuario", prefix_icon=ft.Icons.CAMERA_ALT_OUTLINED,
                                    bgcolor=BG, border_color=BORDER, color=TEXT, value=getattr(ex, "instagram", ""))
    facebook_field = ft.TextField(hint_text="@usuario", prefix_icon=ft.Icons.FACEBOOK,
                                   bgcolor=BG, border_color=BORDER, color=TEXT, value=getattr(ex, "facebook", ""))
    web_field = ft.TextField(hint_text="https://sitio.web.com", prefix_icon=ft.Icons.LANGUAGE,
                              bgcolor=BG, border_color=BORDER, color=TEXT, value=getattr(ex, "pagina_web", ""))

    estado_field = ft.Dropdown(bgcolor=BG, border_color=BORDER, color=TEXT,
                                options=[ft.dropdown.Option("Activo"), ft.dropdown.Option("En revisión"),
                                         ft.dropdown.Option("Aprobado"), ft.dropdown.Option("Rechazado")],
                                value=str(getattr(ex, "estado", "Activo")) or "Activo")

    mensaje = ft.Text("", color=ft.Colors.RED_300)

    def guardar(e):
        if not nombre_field.value or not categoria_field.value or not ubicacion_field.value:
            mensaje.value = "Completa los campos obligatorios de Información del evento."
            page.update()
            return
        try:
            if modo == "agregar":
                nuevo_id = dao.obtener_ultimo_id() + 1
                evento = Evento(
                    nuevo_id, nombre_field.value, categoria_field.value, fecha_field.value,
                    hora_inicio_field.value, hora_fin_field.value, ubicacion_field.value, "",
                    organizador_field.value, edad_field.value, telefono_field.value, correo_field.value,
                    desc_corta_field.value, desc_completa_field.value, caract1.value, caract2.value, caract3.value,
                    instagram_field.value, facebook_field.value, web_field.value, estado_field.value, {},
                )
                dao.insertar(evento)
            else:
                evento = Evento(
                    ex.id, nombre_field.value, categoria_field.value, fecha_field.value,
                    hora_inicio_field.value, hora_fin_field.value, ubicacion_field.value, "",
                    organizador_field.value, edad_field.value, telefono_field.value, correo_field.value,
                    desc_corta_field.value, desc_completa_field.value, caract1.value, caract2.value, caract3.value,
                    instagram_field.value, facebook_field.value, web_field.value, estado_field.value, {},
                )
                dao.actualizar(evento)
            page.go("/admin/eventos")
        except Exception as ex2:
            mensaje.value = f"Error al guardar: {ex2}"
            page.update()

    info_evento = ft.Container(
        content=ft.Column(
            [
                ft.Row([ft.Icon(ft.Icons.EVENT_OUTLINED, color=TEXT), ft.Text("Información del evento", color=TEXT, weight=ft.FontWeight.BOLD)]),
                ft.Row([col_nombre, ft.Column([ft.Text("Categoría *", color=TEXT, size=12), categoria_field], spacing=3)]),
                ft.Row([
                    ft.Column([ft.Text("Horario del evento *", color=TEXT, size=12),
                               ft.Row([hora_inicio_field, ft.Text("-", color=TEXT), hora_fin_field])], spacing=3, expand=True),
                    ft.Column([ft.Text("Fecha *", color=TEXT, size=12), fecha_field], spacing=3),
                ]),
                col_ubicacion,
                ft.OutlinedButton("Seleccionar en mapa", icon=ft.Icons.MAP_OUTLINED, style=ft.ButtonStyle(color=TEXT)),
            ],
            spacing=8,
        ),
        bgcolor=CARD, border_radius=10, border=ft.border.all(1, BORDER), padding=18,
    )

    info_organizador = ft.Container(
        content=ft.Column(
            [
                ft.Row([ft.Icon(ft.Icons.PERSON_OUTLINE, color=TEXT), ft.Text("Información del organizador", color=TEXT, weight=ft.FontWeight.BOLD)]),
                ft.Row([col_organizador, ft.Column([ft.Text("Edad *", color=TEXT, size=12), edad_field], spacing=3, width=100)]),
                ft.Row([ft.Column([ft.Text("Teléfono *", color=TEXT, size=12), telefono_field], spacing=3, expand=True),
                        ft.Column([ft.Text("Correo eléctronico *", color=TEXT, size=12), correo_field], spacing=3, expand=True)]),
            ],
            spacing=8,
        ),
        bgcolor=CARD, border_radius=10, border=ft.border.all(1, BORDER), padding=18,
    )

    descripcion = ft.Container(
        content=ft.Column(
            [
                ft.Row([ft.Icon(ft.Icons.DESCRIPTION_OUTLINED, color=TEXT), ft.Text("Descripción del evento", color=TEXT, weight=ft.FontWeight.BOLD)]),
                ft.Row([col_desc_corta, col_desc_completa]),
                ft.Text("Características del evento *", color=TEXT, size=12),
                caract1, caract2, caract3,
            ],
            spacing=8,
        ),
        bgcolor=CARD, border_radius=10, border=ft.border.all(1, BORDER), padding=18,
    )

    redes = ft.Container(
        content=ft.Column(
            [
                ft.Row([ft.Icon(ft.Icons.EDIT_OUTLINED, color=TEXT), ft.Text("Redes Sociales", color=TEXT, weight=ft.FontWeight.BOLD)]),
                ft.Row([instagram_field, facebook_field]),
                web_field,
                ft.Divider(color=BORDER),
                ft.Text("Documentos requeridos", color=TEXT, weight=ft.FontWeight.BOLD),
                ft.Row([
                    ft.Column([ft.Text("Permiso de evento *\nPDF, JPG o PNG (Máx. 5mb)", color=MUTED, size=11),
                               ft.OutlinedButton("Subir archivo", icon=ft.Icons.UPLOAD_FILE, style=ft.ButtonStyle(color=TEXT))]),
                    ft.Column([ft.Text("Identificación oficial del organizador *\nPDF, JPG o PNG (Máx. 5mb)", color=MUTED, size=11),
                               ft.OutlinedButton("Subir archivo", icon=ft.Icons.UPLOAD_FILE, style=ft.ButtonStyle(color=TEXT))]),
                ]),
            ],
            spacing=8,
        ),
        bgcolor=CARD, border_radius=10, border=ft.border.all(1, BORDER), padding=18,
    )

    adicional = ft.Container(
        content=ft.Column(
            [
                ft.Row([ft.Icon(ft.Icons.INFO_OUTLINE, color=TEXT), ft.Text("Información del adicional", color=TEXT, weight=ft.FontWeight.BOLD)]),
                ft.Text("Estado *", color=TEXT, size=12), estado_field,
                ft.Text("Datos destacados del evento *", color=TEXT, size=12),
                ft.Row([
                    ft.TextField(hint_text="Ej. Tradicion y adrenalina", bgcolor=BG, border_color=BORDER, color=TEXT, expand=True),
                    ft.TextField(hint_text="Titulo", bgcolor=BG, border_color=BORDER, color=TEXT, expand=True),
                    ft.TextField(hint_text="Titulo", bgcolor=BG, border_color=BORDER, color=TEXT, expand=True),
                    ft.TextField(hint_text="Titulo", bgcolor=BG, border_color=BORDER, color=TEXT, expand=True),
                ]),
                ft.Text("Una vez guardado, el evento quedará en revisión antes de publicarse", color=MUTED, size=11),
            ],
            spacing=8,
        ),
        bgcolor=CARD, border_radius=10, border=ft.border.all(1, BORDER), padding=18,
    )

    imagen_box = ft.Container(
        content=ft.Column(
            [
                ft.Row([ft.Icon(ft.Icons.CAMERA_ALT_OUTLINED, color=TEXT), ft.Text("Imagen del evento", color=TEXT, weight=ft.FontWeight.BOLD)]),
                ft.Container(
                    content=ft.Column(
                        [ft.Icon(ft.Icons.CLOUD_UPLOAD_OUTLINED, size=35, color=TEXT),
                         ft.Text("Subir imagen principal", color=TEXT, size=12),
                         ft.Text("JPG, PNG o WEB (máx. 5MB)", color=MUTED, size=10),
                         ft.ElevatedButton("Seleccionar archivo", style=ft.ButtonStyle(bgcolor=GOLD, color=BG))],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    bgcolor=BG, border=ft.border.all(1, BORDER), border_radius=10, padding=15,
                    alignment=ft.alignment.center, height=170,
                ),
                ft.Row([ft.Container(bgcolor="#DDDDDD", width=60, height=60, border_radius=6) for _ in range(3)]),
            ],
            spacing=10,
        ),
        bgcolor=CARD, border_radius=10, border=ft.border.all(1, BORDER), padding=18, width=300,
    )

    resumen_box = ft.Container(
        content=ft.Column(
            [
                ft.Row([ft.Icon(ft.Icons.DESCRIPTION_OUTLINED, color=TEXT), ft.Text("Resumen de la información", color=TEXT, weight=ft.FontWeight.BOLD)]),
                ft.Text("Nombre del evento:", color=TEXT, size=12),
                ft.Text("Categoría:", color=TEXT, size=12),
                ft.Text("Fecha:", color=TEXT, size=12),
                ft.Text("Horario del evento:", color=TEXT, size=12),
                ft.Text("Ubicación:", color=TEXT, size=12),
                ft.Text("Nombre del organizador:", color=TEXT, size=12),
                ft.Text("Estado:", color=TEXT, size=12),
                ft.Text("Datos destacados:", color=TEXT, size=12),
            ],
            spacing=6,
        ),
        bgcolor=CARD, border_radius=10, border=ft.border.all(1, BORDER), padding=18, width=300,
    )

    encabezado = ft.Column(
        [
            ft.Row([ft.IconButton(ft.Icons.ARROW_BACK, icon_color=GOLD, on_click=lambda e: page.go("/admin/eventos")),
                    ft.Text("Gestión de Evento", color=GOLD, size=22, weight=ft.FontWeight.BOLD)]),
            ft.Text(f"Eventos > {'Agregar evento' if modo == 'agregar' else 'Editar evento'}", color=MUTED, size=12),
        ],
        spacing=2,
    )

    botones = ft.Row(
        [
            ft.OutlinedButton("Cancelar", style=ft.ButtonStyle(color=TEXT), on_click=lambda e: page.go("/admin/eventos")),
            ft.Row([
                ft.OutlinedButton("Ver evento", style=ft.ButtonStyle(color=TEXT),
                                  on_click=lambda e: page.go("/admin/eventos/ver")),
                ft.OutlinedButton("Guardar borrador", style=ft.ButtonStyle(color=TEXT)),
                ft.ElevatedButton("Guardar evento" if modo == "agregar" else "Guardar cambios",
                                  style=ft.ButtonStyle(bgcolor=GOLD, color=BG), on_click=guardar),
            ]),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    contenido = ft.Column(
        [
            encabezado, ft.Divider(color=GOLD),
            ft.Row(
                [
                    ft.Column([info_evento, info_organizador, descripcion, redes, adicional], expand=True, spacing=15),
                    ft.Column([imagen_box, resumen_box], spacing=15, width=300),
                ],
                vertical_alignment=ft.CrossAxisAlignment.START, spacing=15,
            ),
            mensaje,
            botones,
        ],
        spacing=20, scroll=ft.ScrollMode.AUTO, expand=True,
    )

    return ft.View(
        route="/admin/eventos/agregar" if modo == "agregar" else "/admin/eventos/editar",
        bgcolor=BG, padding=0,
        controls=[ft.Row([_sidebar(page), ft.Container(content=contenido, padding=25, expand=True)],
                          expand=True, vertical_alignment=ft.CrossAxisAlignment.START)],
    )