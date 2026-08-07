import re

import flet as ft

from dao.establecimiento_dao import EstablecimientoDAO
from dao.categoria_dao import CategoriaDAO
from dao.imagen_dao import ImagenDAO
from models.establecimiento import Establecimiento
from models.imagen import Imagen
from services.cloudinary_service import subir_imagen

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
                ft.Container(
                    content=ft.Row([ft.Icon(ft.Icons.STOREFRONT_OUTLINED, color=GOLD, size=18), ft.Text("Gestión Estable.", color=GOLD)]),
                    bgcolor=CARD, border_radius=6, padding=ft.padding.symmetric(horizontal=15, vertical=10),
                ),
                item(ft.Icons.CELEBRATION_OUTLINED, "Gestión Entre.", "/admin/entretenimiento"),
                item(ft.Icons.CATEGORY_OUTLINED, "Gestión Cat.", "/admin/categorias"),
                ft.Divider(color=BORDER),
                item(ft.Icons.STOREFRONT, "Establecimientos", "/establecimientos"),
                item(ft.Icons.EVENT, "Eventos", "/eventos"),
                item(ft.Icons.STAR_BORDER, "Entretenimiento", "/entretenimiento"),
                ft.Container(expand=True),
                item(ft.Icons.SETTINGS_OUTLINED, "Configuración", "/configuracion"),
                ft.Divider(color=BORDER),
                ft.Container(
                    content=ft.Row([ft.Icon(ft.Icons.LOGOUT, color=TEXT, size=18), ft.Text("Cerrar sesión", color=TEXT)]),
                    padding=ft.padding.symmetric(horizontal=15, vertical=10), on_click=cerrar_sesion,
                ),
            ],
            expand=True,
        ),
    )


def _producto_box(idx) -> ft.Container:
    return ft.Container(
        content=ft.Column(
            [
                ft.Container(bgcolor="#DDDDDD", height=50, alignment=ft.alignment.center,
                             content=ft.Icon(ft.Icons.IMAGE_OUTLINED, color="#666")),
                ft.TextField(hint_text="Nombre producto", bgcolor=BG, border_color=BORDER, color=TEXT, text_size=11),
                ft.TextField(hint_text="Escribe una descripción muy corta...", bgcolor=BG, border_color=BORDER,
                             color=TEXT, text_size=10),
                ft.TextField(hint_text="$00.00", bgcolor=BG, border_color=BORDER, color=TEXT, text_size=11),
            ],
            spacing=4,
        ),
        bgcolor=CARD, border=ft.border.all(1, BORDER), border_radius=8, padding=8, width=140,
    )


def establecimiento_form_view(page: ft.Page, modo: str = "agregar") -> ft.View:

    dao = EstablecimientoDAO()
    ex = None
    if modo == "editar":
        id_sel = page.app_state.get("establecimiento_sel")
        try:
            ex = next((e for e in dao.obtener_todo() if e.id == id_sel), None)
        except Exception:
            ex = None

    nombre_field = ft.TextField(hint_text="Ej. 4 Elementos", bgcolor=BG, border_color=BORDER, color=TEXT,
                                 value=getattr(ex, "nombre_establecimiento", ""))
    try:
        categorias_registradas = CategoriaDAO().obtener_todo()
    except Exception:
        categorias_registradas = []
    opciones_categoria = [ft.dropdown.Option(key=str(c.id), text=c.nombre) for c in categorias_registradas
                          if str(getattr(c, "tipo_categoria", "")).strip().lower() in ("establecimientos", "establecimiento")]
    if not opciones_categoria:
        opciones_categoria = [ft.dropdown.Option(key=str(c.id), text=c.nombre) for c in categorias_registradas]

    _categoria_existente = next((c for c in categorias_registradas if c.nombre == getattr(ex, "categoria", None)), None) if ex else None

    categoria_field = ft.Dropdown(hint_text="Selecciona una categoria", bgcolor=BG, border_color=BORDER, color=TEXT,
                                   options=opciones_categoria,
                                   value=str(_categoria_existente.id) if _categoria_existente else None)
    hora_inicio_field = ft.TextField(hint_text="Ej. 10:00 am", bgcolor=BG, border_color=BORDER, color=TEXT,
                                      value=str(getattr(ex, "horario_inicio", "")))
    hora_fin_field = ft.TextField(hint_text="Ej. 02:00 pm", bgcolor=BG, border_color=BORDER, color=TEXT,
                                   value=str(getattr(ex, "horario_fin", "")))
    direccion_field = ft.TextField(hint_text="Ej. Calle 5Pte. #123 Huamantla Tlaxcala",
                                    bgcolor=BG, border_color=BORDER, color=TEXT, value=getattr(ex, "direccion", ""))

    _mapa_previo = getattr(ex, "mapa", "") or ""
    _lat_previa, _lng_previa = "", ""
    if "," in str(_mapa_previo):
        partes = str(_mapa_previo).split(",", 1)
        _lat_previa, _lng_previa = partes[0].strip(), partes[1].strip()

    latitud_field = ft.TextField(hint_text="Ej. 19.3153", bgcolor=BG, border_color=BORDER, color=TEXT,
                                  value=_lat_previa, width=180)
    longitud_field = ft.TextField(hint_text="Ej. -97.9219", bgcolor=BG, border_color=BORDER, color=TEXT,
                                   value=_lng_previa, width=180)

    propietario_field = ft.TextField(hint_text="Ej. Jose Luis Ortiz Huerta", bgcolor=BG, border_color=BORDER, color=TEXT,
                                      value=getattr(ex, "nombre_propietario", ""))
    edad_field = ft.TextField(hint_text="Ej. 26", bgcolor=BG, border_color=BORDER, color=TEXT,
                               value=str(getattr(ex, "edad", "")))
    telefono_field = ft.TextField(hint_text="Ej. 247 124 2456", bgcolor=BG, border_color=BORDER, color=TEXT,
                                   value=str(getattr(ex, "telefono", "")))
    correo_field = ft.TextField(hint_text="Ej. contacto@gmail.com", bgcolor=BG, border_color=BORDER, color=TEXT,
                                 value=getattr(ex, "correo", ""))

    desc_corta_field = ft.TextField(hint_text="Cuéntanos sobre el establecimiento...", multiline=True, min_lines=3,
                                     bgcolor=BG, border_color=BORDER, color=TEXT,
                                     value=getattr(ex, "descripcion_corta", ""))
    desc_completa_field = ft.TextField(hint_text="Describe con detalle el establecimiento...", multiline=True, min_lines=3,
                                        bgcolor=BG, border_color=BORDER, color=TEXT,
                                        value=getattr(ex, "descripcion_Completa", ""))
    caract1 = ft.TextField(hint_text="Característica de el establecimiento...", bgcolor=BG, border_color=BORDER, color=TEXT,
                            value=getattr(ex, "caracteristica_1", ""))
    caract2 = ft.TextField(hint_text="Característica de el establecimiento...", bgcolor=BG, border_color=BORDER, color=TEXT,
                            value=getattr(ex, "caracteristica_2", ""))
    caract3 = ft.TextField(hint_text="Característica de el establecimiento...", bgcolor=BG, border_color=BORDER, color=TEXT,
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
    servicios_field = ft.TextField(hint_text="Que servicios ofrece...", bgcolor=BG, border_color=BORDER, color=TEXT,
                                    value=getattr(ex, "servicios", ""))
    rango_field = ft.TextField(hint_text="$200 - $400", bgcolor=BG, border_color=BORDER, color=TEXT,
                                value=getattr(ex, "rango_precios", ""))

    mensaje = ft.Text("", color=ft.Colors.RED_300)

    def _solo_digitos(texto):
        """Limpia espacios/guiones de un teléfono. Regresa texto (para columnas varchar)."""
        limpio = re.sub(r"[^0-9]", "", texto or "")
        return limpio or None

    # --- Imagen principal (Cloudinary) ---
    imagen_subida = {"url": getattr(ex, "imagen", None) if ex else None, "public_id": None}
    vista_previa = ft.Image(src=imagen_subida["url"], width=60, height=60, fit=ft.ImageFit.COVER,
                             border_radius=6, visible=bool(imagen_subida["url"]))
    mensaje_imagen = ft.Text("", size=11, color=MUTED)

    def archivo_seleccionado(e: ft.FilePickerResultEvent):
        if not e.files:
            return
        ruta_local = e.files[0].path
        mensaje_imagen.value = "Subiendo imagen..."
        mensaje_imagen.color = MUTED
        page.update()
        try:
            resultado = subir_imagen(ruta_local, carpeta="ruta_magica/establecimientos")
            imagen_subida["url"] = resultado["url"]
            imagen_subida["public_id"] = resultado["public_id"]
            vista_previa.src = resultado["url"]
            vista_previa.visible = True
            mensaje_imagen.value = "Imagen subida correctamente."
            mensaje_imagen.color = BTN_GREEN
        except Exception as ex_img:
            mensaje_imagen.value = f"No se pudo subir la imagen: {ex_img}"
            mensaje_imagen.color = ft.Colors.RED_300
        page.update()

    file_picker = ft.FilePicker(on_result=archivo_seleccionado)
    page.overlay.append(file_picker)

    def guardar(e):
        if not nombre_field.value or not categoria_field.value or not direccion_field.value:
            mensaje.value = "Completa los campos obligatorios de Información del establecimiento."
            page.update()
            return
        try:
            mapa_valor = f"{latitud_field.value},{longitud_field.value}" if latitud_field.value and longitud_field.value else ""

            if modo == "agregar":
                nuevo_id = dao.obtener_ultimo_id() + 1
                est = Establecimiento(
                    nuevo_id, nombre_field.value, int(categoria_field.value), hora_inicio_field.value, hora_fin_field.value,
                    direccion_field.value, mapa_valor, propietario_field.value, edad_field.value, _solo_digitos(telefono_field.value),
                    correo_field.value, desc_corta_field.value, desc_completa_field.value,
                    caract1.value, caract2.value, caract3.value, instagram_field.value, facebook_field.value,
                    web_field.value, estado_field.value, servicios_field.value, rango_field.value, {},
                )
                dao.insertar(est)
                id_guardado = nuevo_id
            else:
                est = Establecimiento(
                    ex.id, nombre_field.value, int(categoria_field.value), hora_inicio_field.value, hora_fin_field.value,
                    direccion_field.value, mapa_valor, propietario_field.value, edad_field.value, _solo_digitos(telefono_field.value),
                    correo_field.value, desc_corta_field.value, desc_completa_field.value,
                    caract1.value, caract2.value, caract3.value, instagram_field.value, facebook_field.value,
                    web_field.value, estado_field.value, servicios_field.value, rango_field.value, {},
                )
                dao.actualizar(est)
                id_guardado = ex.id

            # Si se subió una imagen a Cloudinary, la registramos en la tabla imagenes
            if imagen_subida["url"]:
                imagen_dao = ImagenDAO()
                nuevo_id_imagen = imagen_dao.obtener_ultimo_id() + 1
                imagen_dao.insertar(Imagen(
                    nuevo_id_imagen, id_guardado, None, None,
                    imagen_subida["url"], imagen_subida["public_id"],
                ))

            page.go("/admin/establecimientos")
        except Exception as ex2:
            mensaje.value = f"Error al guardar: {ex2}"
            page.update()

    info_establecimiento = ft.Container(
        content=ft.Column(
            [
                ft.Row([ft.Icon(ft.Icons.STOREFRONT_OUTLINED, color=TEXT), ft.Text("Información del establecimiento", color=TEXT, weight=ft.FontWeight.BOLD)]),
                ft.Row([
                    ft.Column([ft.Text("Nombre del establecimiento*", color=TEXT, size=12), nombre_field], expand=True, spacing=3),
                    ft.Column([ft.Text("Categoría *", color=TEXT, size=12), categoria_field], expand=True, spacing=3),
                ]),
                ft.Row([
                    ft.Column([ft.Text("Horario de atención*", color=TEXT, size=12),
                               ft.Row([hora_inicio_field, ft.Text("-", color=TEXT), hora_fin_field])], expand=True, spacing=3),
                ]),
                ft.Column([ft.Text("Dirección*", color=TEXT, size=12), direccion_field], spacing=3),
                ft.Text("Coordenadas (opcional, mientras no hay selector de mapa)", color=MUTED, size=11),
                ft.Row([
                    ft.Column([ft.Text("Latitud", color=TEXT, size=12), latitud_field], spacing=3),
                    ft.Column([ft.Text("Longitud", color=TEXT, size=12), longitud_field], spacing=3),
                ]),
            ],
            spacing=8,
        ),
        bgcolor=CARD, border_radius=10, border=ft.border.all(1, BORDER), padding=18,
    )

    info_propietario = ft.Container(
        content=ft.Column(
            [
                ft.Row([ft.Icon(ft.Icons.PERSON_OUTLINE, color=TEXT), ft.Text("Información del propietario", color=TEXT, weight=ft.FontWeight.BOLD)]),
                ft.Row([
                    ft.Column([ft.Text("Nombre del propietario *", color=TEXT, size=12), propietario_field], expand=True, spacing=3),
                    ft.Column([ft.Text("Edad *", color=TEXT, size=12), edad_field], width=100, spacing=3),
                ]),
                ft.Row([
                    ft.Column([ft.Text("Teléfono *", color=TEXT, size=12), telefono_field], expand=True, spacing=3),
                    ft.Column([ft.Text("Correo eléctronico *", color=TEXT, size=12), correo_field], expand=True, spacing=3),
                ]),
            ],
            spacing=8,
        ),
        bgcolor=CARD, border_radius=10, border=ft.border.all(1, BORDER), padding=18,
    )

    descripcion = ft.Container(
        content=ft.Column(
            [
                ft.Row([ft.Icon(ft.Icons.DESCRIPTION_OUTLINED, color=TEXT), ft.Text("Descripción del establecimiento", color=TEXT, weight=ft.FontWeight.BOLD)]),
                ft.Row([
                    ft.Column([ft.Text("Descripción corta *", color=TEXT, size=12), desc_corta_field], expand=True, spacing=3),
                    ft.Column([ft.Text("Descripción completa *", color=TEXT, size=12), desc_completa_field], expand=True, spacing=3),
                ]),
                ft.Text("Características del establecimiento*", color=TEXT, size=12),
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
                    ft.Column([ft.Text("Documentos del establecimiento *\nPDF, JPG o PNG (Máx. 5mb)", color=MUTED, size=11),
                               ft.OutlinedButton("Subir archivo", icon=ft.Icons.UPLOAD_FILE, style=ft.ButtonStyle(color=TEXT))]),
                    ft.Column([ft.Text("Identificación oficial del propietario*\nPDF, JPG o PNG (Máx. 5mb)", color=MUTED, size=11),
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
                ft.Row([
                    ft.Column([ft.Text("Servicios que ofrece *", color=TEXT, size=12), servicios_field], expand=True, spacing=3),
                    ft.Column([ft.Text("Rango de precios *", color=TEXT, size=12), rango_field], expand=True, spacing=3),
                ]),
                ft.Text("Productos a ofrecer * — Titulo (Ej. Menu)", color=TEXT, size=12),
                ft.Row([_producto_box(i) for i in range(4)], wrap=True, spacing=10),
            ],
            spacing=8,
        ),
        bgcolor=CARD, border_radius=10, border=ft.border.all(1, BORDER), padding=18,
    )

    imagen_box = ft.Container(
        content=ft.Column(
            [
                ft.Row([ft.Icon(ft.Icons.CAMERA_ALT_OUTLINED, color=TEXT), ft.Text("Imagen del establecimiento", color=TEXT, weight=ft.FontWeight.BOLD)]),
                ft.Container(
                    content=ft.Column(
                        [ft.Icon(ft.Icons.CLOUD_UPLOAD_OUTLINED, size=35, color=TEXT),
                         ft.Text("Subir imagen principal", color=TEXT, size=12),
                         ft.Text("JPG, PNG o WEB (máx. 5MB)", color=MUTED, size=10),
                         ft.ElevatedButton("Seleccionar archivo", style=ft.ButtonStyle(bgcolor=GOLD, color=BG),
                                           on_click=lambda e: file_picker.pick_files(
                                               allow_multiple=False, file_type=ft.FilePickerFileType.IMAGE)),
                         mensaje_imagen],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    bgcolor=BG, border=ft.border.all(1, BORDER), border_radius=10, padding=15,
                    alignment=ft.alignment.center, height=170,
                ),
                ft.Row([vista_previa] + [ft.Container(bgcolor="#DDDDDD", width=60, height=60, border_radius=6) for _ in range(2)]),
            ],
            spacing=10,
        ),
        bgcolor=CARD, border_radius=10, border=ft.border.all(1, BORDER), padding=18, width=300,
    )

    resumen_box = ft.Container(
        content=ft.Column(
            [
                ft.Row([ft.Icon(ft.Icons.DESCRIPTION_OUTLINED, color=TEXT), ft.Text("Resumen de la información", color=TEXT, weight=ft.FontWeight.BOLD)]),
                ft.Text("Nombre del establecimiento:", color=TEXT, size=12),
                ft.Text("Categoría:", color=TEXT, size=12),
                ft.Text("Horario de atención:", color=TEXT, size=12),
                ft.Text("Dirección:", color=TEXT, size=12),
                ft.Text("Nombre del propietario:", color=TEXT, size=12),
                ft.Text("Servicios que ofrece:", color=TEXT, size=12),
                ft.Text("Rango de precios:", color=TEXT, size=12),
                ft.Text("Productos a ofrecer:", color=TEXT, size=12),
            ],
            spacing=6,
        ),
        bgcolor=CARD, border_radius=10, border=ft.border.all(1, BORDER), padding=18, width=300,
    )

    encabezado = ft.Column(
        [
            ft.Row([ft.IconButton(ft.Icons.ARROW_BACK, icon_color=GOLD, on_click=lambda e: page.go("/admin/establecimientos")),
                    ft.Text("Gestión de Establecimientos", color=GOLD, size=22, weight=ft.FontWeight.BOLD)]),
            ft.Text(f"Eventos > {'Agregar establecimiento' if modo == 'agregar' else 'Editar establecimiento'}", color=MUTED, size=12),
        ],
        spacing=2,
    )

    botones = ft.Row(
        [
            ft.OutlinedButton("Cancelar", style=ft.ButtonStyle(color=TEXT), on_click=lambda e: page.go("/admin/establecimientos")),
            ft.Row([
                ft.OutlinedButton("Ver evento", style=ft.ButtonStyle(color=TEXT),
                                  on_click=lambda e: page.go("/admin/establecimientos/ver")),
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
                    ft.Column([info_establecimiento, info_propietario, descripcion, redes, adicional], expand=True, spacing=15),
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
        route="/admin/establecimientos/agregar" if modo == "agregar" else "/admin/establecimientos/editar",
        bgcolor=BG, padding=0,
        controls=[ft.Row([_sidebar(page), ft.Container(content=contenido, padding=25, expand=True)],
                          expand=True, vertical_alignment=ft.CrossAxisAlignment.START)],
    )