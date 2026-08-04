import flet as ft

from dao.entretenimiento_dao import EntretenimientoDAO
from dao.categoria_dao import CategoriaDAO
from models.entretenimiento import Entretenimiento

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
                ft.Container(
                    content=ft.Row([ft.Icon(ft.Icons.CELEBRATION_OUTLINED, color=GOLD, size=18), ft.Text("Gestión Entre.", color=GOLD)]),
                    bgcolor=CARD, border_radius=6, padding=ft.padding.symmetric(horizontal=15, vertical=10),
                ),
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


def entretenimiento_form_view(page: ft.Page, modo: str = "agregar") -> ft.View:

    dao = EntretenimientoDAO()
    ex = None
    if modo == "editar":
        id_sel = page.app_state.get("entretenimiento_sel")
        try:
            resultado = dao.obtener_todo()
            lista = resultado if isinstance(resultado, list) else [resultado]
            ex = next((x for x in lista if getattr(x, "id", None) == id_sel), None)
        except Exception:
            ex = None

    nombre_field = ft.TextField(hint_text="Ej. La Malinche", bgcolor=BG, border_color=BORDER, color=TEXT,
                                 value=getattr(ex, "nombre_entretenimiento", ""))
    try:
        categorias_registradas = CategoriaDAO().obtener_todo()
    except Exception:
        categorias_registradas = []
    opciones_categoria = [ft.dropdown.Option(c.nombre) for c in categorias_registradas
                          if str(getattr(c, "tipo_categoria", "")).strip().lower() in ("entretenimiento",)]
    if not opciones_categoria:
        opciones_categoria = [ft.dropdown.Option(c.nombre) for c in categorias_registradas]

    categoria_field = ft.Dropdown(hint_text="Selecciona una categoria", bgcolor=BG, border_color=BORDER, color=TEXT,
                                   options=opciones_categoria,
                                   value=str(getattr(ex, "categoria", "")) or None)
    hora_inicio_field = ft.TextField(hint_text="Ej. 10:00 am", bgcolor=BG, border_color=BORDER, color=TEXT,
                                      value=str(getattr(ex, "horario_inicio", "")))
    hora_fin_field = ft.TextField(hint_text="Ej. 02:00 pm", bgcolor=BG, border_color=BORDER, color=TEXT,
                                   value=str(getattr(ex, "horario_fin", "")))
    direccion_field = ft.TextField(hint_text="Ej. Parque Nacional La Malinche", bgcolor=BG, border_color=BORDER, color=TEXT,
                                    value=getattr(ex, "direccion", ""))

    responsable_field = ft.TextField(hint_text="Ej. Jose Luis Ortiz Huerta", bgcolor=BG, border_color=BORDER, color=TEXT,
                                      value=getattr(ex, "nombre_responsable", ""))
    telefono_field = ft.TextField(hint_text="Ej. 247 124 2456", bgcolor=BG, border_color=BORDER, color=TEXT,
                                   value=str(getattr(ex, "telefono", "")))
    correo_field = ft.TextField(hint_text="Ej. contacto@gmail.com", bgcolor=BG, border_color=BORDER, color=TEXT,
                                 value=getattr(ex, "correo", ""))

    desc_corta_field = ft.TextField(hint_text="Cuéntanos sobre esta experiencia...", multiline=True, min_lines=3,
                                     bgcolor=BG, border_color=BORDER, color=TEXT,
                                     value=getattr(ex, "descripcion_corta", ""))
    desc_completa_field = ft.TextField(hint_text="Describe con detalle la experiencia...", multiline=True, min_lines=3,
                                        bgcolor=BG, border_color=BORDER, color=TEXT,
                                        value=getattr(ex, "descripcion_completa", ""))
    caract1 = ft.TextField(hint_text="Característica...", bgcolor=BG, border_color=BORDER, color=TEXT,
                            value=getattr(ex, "caracteristica_1", ""))
    caract2 = ft.TextField(hint_text="Característica...", bgcolor=BG, border_color=BORDER, color=TEXT,
                            value=getattr(ex, "caracteristica_2", ""))
    caract3 = ft.TextField(hint_text="Característica...", bgcolor=BG, border_color=BORDER, color=TEXT,
                            value=getattr(ex, "caracteristica_3", ""))

    capacidad_field = ft.TextField(hint_text="Ej. 1-20 personas", bgcolor=BG, border_color=BORDER, color=TEXT,
                                    value=str(getattr(ex, "capacidad", "")))
    precio_field = ft.TextField(hint_text="Ej. $30 - $120", bgcolor=BG, border_color=BORDER, color=TEXT,
                                 value=str(getattr(ex, "precio", "")))

    servicio_fields = [ft.TextField(hint_text=f"Servicio {i}", bgcolor=BG, border_color=BORDER, color=TEXT,
                                     value=str(getattr(ex, f"servicio_{i}", "") or "")) for i in range(1, 6)]
    recomendacion_fields = [ft.TextField(hint_text=f"Recomendación {i}", bgcolor=BG, border_color=BORDER, color=TEXT,
                                          value=str(getattr(ex, f"recomendacion_{i}", "") or "")) for i in range(1, 5)]

    instagram_field = ft.TextField(hint_text="@usuario", prefix_icon=ft.Icons.CAMERA_ALT_OUTLINED,
                                    bgcolor=BG, border_color=BORDER, color=TEXT, value=getattr(ex, "instagram", ""))
    facebook_field = ft.TextField(hint_text="@usuario", prefix_icon=ft.Icons.FACEBOOK,
                                   bgcolor=BG, border_color=BORDER, color=TEXT, value=getattr(ex, "facebook", ""))
    web_field = ft.TextField(hint_text="https://sitio.web.com", prefix_icon=ft.Icons.LANGUAGE,
                              bgcolor=BG, border_color=BORDER, color=TEXT, value=getattr(ex, "pagina_web", ""))

    mensaje = ft.Text("", color=ft.Colors.RED_300)

    def guardar(e):
        if not nombre_field.value or not categoria_field.value or not direccion_field.value:
            mensaje.value = "Completa los campos obligatorios de Información del entretenimiento."
            page.update()
            return
        try:
            valores_servicio = [f.value for f in servicio_fields]
            valores_recomendacion = [f.value for f in recomendacion_fields]

            if modo == "agregar":
                nuevo_id = dao.obtener_ultimo_id() + 1
                if nuevo_id is None:
                    nuevo_id = 1
                ent = Entretenimiento(
                    nuevo_id, nombre_field.value, categoria_field.value, hora_inicio_field.value, hora_fin_field.value,
                    direccion_field.value, "", "", responsable_field.value, telefono_field.value, correo_field.value,
                    desc_corta_field.value, desc_completa_field.value, caract1.value, caract2.value, caract3.value,
                    capacidad_field.value, precio_field.value, *valores_servicio, *valores_recomendacion,
                    instagram_field.value, facebook_field.value, web_field.value,
                )
                dao.insertar(ent)
            else:
                ent = Entretenimiento(
                    ex.id, nombre_field.value, categoria_field.value, hora_inicio_field.value, hora_fin_field.value,
                    direccion_field.value, "", "", responsable_field.value, telefono_field.value, correo_field.value,
                    desc_corta_field.value, desc_completa_field.value, caract1.value, caract2.value, caract3.value,
                    capacidad_field.value, precio_field.value, *valores_servicio, *valores_recomendacion,
                    instagram_field.value, facebook_field.value, web_field.value,
                )
                dao.actualizar(ent)
            page.go("/admin/entretenimiento")
        except Exception as ex2:
            mensaje.value = f"Error al guardar: {ex2}"
            page.update()

    info_entretenimiento = ft.Container(
        content=ft.Column(
            [
                ft.Row([ft.Icon(ft.Icons.CELEBRATION_OUTLINED, color=TEXT), ft.Text("Información del entretenimiento", color=TEXT, weight=ft.FontWeight.BOLD)]),
                ft.Row([
                    ft.Column([ft.Text("Nombre *", color=TEXT, size=12), nombre_field], expand=True, spacing=3),
                    ft.Column([ft.Text("Categoría *", color=TEXT, size=12), categoria_field], expand=True, spacing=3),
                ]),
                ft.Row([hora_inicio_field, ft.Text("-", color=TEXT), hora_fin_field]),
                ft.Column([ft.Text("Dirección*", color=TEXT, size=12), direccion_field], spacing=3),
                ft.OutlinedButton("Seleccionar en mapa", icon=ft.Icons.MAP_OUTLINED, style=ft.ButtonStyle(color=TEXT)),
            ],
            spacing=8,
        ),
        bgcolor=CARD, border_radius=10, border=ft.border.all(1, BORDER), padding=18,
    )

    info_responsable = ft.Container(
        content=ft.Column(
            [
                ft.Row([ft.Icon(ft.Icons.PERSON_OUTLINE, color=TEXT), ft.Text("Información del responsable", color=TEXT, weight=ft.FontWeight.BOLD)]),
                ft.Column([ft.Text("Nombre del responsable *", color=TEXT, size=12), responsable_field], spacing=3),
                ft.Row([telefono_field, correo_field]),
            ],
            spacing=8,
        ),
        bgcolor=CARD, border_radius=10, border=ft.border.all(1, BORDER), padding=18,
    )

    descripcion = ft.Container(
        content=ft.Column(
            [
                ft.Row([ft.Icon(ft.Icons.DESCRIPTION_OUTLINED, color=TEXT), ft.Text("Descripción de la experiencia", color=TEXT, weight=ft.FontWeight.BOLD)]),
                ft.Row([
                    ft.Column([ft.Text("Descripción corta *", color=TEXT, size=12), desc_corta_field], expand=True, spacing=3),
                    ft.Column([ft.Text("Descripción completa *", color=TEXT, size=12), desc_completa_field], expand=True, spacing=3),
                ]),
                ft.Text("Características *", color=TEXT, size=12),
                caract1, caract2, caract3,
                ft.Row([
                    ft.Column([ft.Text("Capacidad *", color=TEXT, size=12), capacidad_field], expand=True, spacing=3),
                    ft.Column([ft.Text("Precio *", color=TEXT, size=12), precio_field], expand=True, spacing=3),
                ]),
                ft.Text("Servicios que ofrece", color=TEXT, size=12),
                ft.Row(servicio_fields, wrap=True),
                ft.Text("Recomendaciones para visitantes", color=TEXT, size=12),
                ft.Row(recomendacion_fields, wrap=True),
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
            ],
            spacing=8,
        ),
        bgcolor=CARD, border_radius=10, border=ft.border.all(1, BORDER), padding=18,
    )

    imagen_box = ft.Container(
        content=ft.Column(
            [
                ft.Row([ft.Icon(ft.Icons.CAMERA_ALT_OUTLINED, color=TEXT), ft.Text("Imagen de la experiencia", color=TEXT, weight=ft.FontWeight.BOLD)]),
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
                ft.Text("Nombre:", color=TEXT, size=12),
                ft.Text("Categoría:", color=TEXT, size=12),
                ft.Text("Dirección:", color=TEXT, size=12),
                ft.Text("Capacidad:", color=TEXT, size=12),
                ft.Text("Precio:", color=TEXT, size=12),
            ],
            spacing=6,
        ),
        bgcolor=CARD, border_radius=10, border=ft.border.all(1, BORDER), padding=18, width=300,
    )

    encabezado = ft.Column(
        [
            ft.Row([ft.IconButton(ft.Icons.ARROW_BACK, icon_color=GOLD, on_click=lambda e: page.go("/admin/entretenimiento")),
                    ft.Text("Gestión de entretenimiento", color=GOLD, size=22, weight=ft.FontWeight.BOLD)]),
            ft.Text(f"Entretenimiento > {'Agregar entretenimiento' if modo == 'agregar' else 'Editar entretenimiento'}", color=MUTED, size=12),
        ],
        spacing=2,
    )

    botones = ft.Row(
        [
            ft.OutlinedButton("Cancelar", style=ft.ButtonStyle(color=TEXT), on_click=lambda e: page.go("/admin/entretenimiento")),
            ft.Row([
                ft.OutlinedButton("Ver entretenimiento", style=ft.ButtonStyle(color=TEXT),
                                  on_click=lambda e: page.go("/admin/entretenimiento/ver")),
                ft.OutlinedButton("Guardar borrador", style=ft.ButtonStyle(color=TEXT)),
                ft.ElevatedButton("Guardar" if modo == "agregar" else "Guardar cambios",
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
                    ft.Column([info_entretenimiento, info_responsable, descripcion, redes], expand=True, spacing=15),
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
        route="/admin/entretenimiento/agregar" if modo == "agregar" else "/admin/entretenimiento/editar",
        bgcolor=BG, padding=0,
        controls=[ft.Row([_sidebar(page), ft.Container(content=contenido, padding=25, expand=True)],
                          expand=True, vertical_alignment=ft.CrossAxisAlignment.START)],
    )